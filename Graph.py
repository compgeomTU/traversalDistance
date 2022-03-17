from geojson import LineString, Feature, FeatureCollection
import matplotlib.pyplot as plt
import geojson


class Graph:
    def __init__(self, filename=None):
        self.nodeHash = {}  # [local_id] ->  id
        self.nodeHashReverse = {}
        self.nodes = {}  # id -> [lon,lat]
        self.edges = {}  # id -> [n1, n2]
        self.nodeLink = {}   # id -> list of next node
        self.nodeID = 0
        self.edgeID = 0
        self.edgeHash = {}  # [nid1, nid2] -> edge id
        self.edgeWeight = {}
        self.nodeWeight = {}
        self.edgeInt = {}
        self.deletedNodes = {}
        self.breadcrumbs = {}  # id -> [[lon,lat],[lon,lat], ...]
        if filename is not None:
            with open(filename+"_vertices.txt", 'r') as vf:
                for line in vf:
                    if line == "" or line[0] == " ":
                        continue
                    vertex = line.strip('\n').split(',')
                    self.addNode(int(vertex[0]), float(
                        vertex[1]), float(vertex[2]))
            with open(filename+"_edges.txt", 'r') as ve:
                for line in ve:
                    if line == "" or line[0] == " ":
                        continue
                    edge = line.strip('\n').split(',')
                    self.connectTwoNodes(int(edge[1]), int(edge[2]))

    def addNode(self, nid, lon, lat, nodeweight=0):
        if nid not in self.nodeHash.keys():
            self.nodeHash[nid] = self.nodeID
            self.nodeHashReverse[self.nodeID] = nid
            self.nodes[self.nodeID] = [lon, lat]
            self.nodeLink[self.nodeID] = []
            self.nodeWeight[self.nodeID] = nodeweight
            self.nodeID += 1
        else:
            print("Duplicated Node !!!", nid)
            return self.nodeHash[nid]

        return self.nodeID - 1

    def addEdge(self, nid1, lon1, lat1, nid2, lon2, lat2,  nodeweight1=0, nodeweight2=0, edgeweight=0):

        if nid1 not in self.nodeHash.keys():
            self.nodeHash[nid1] = self.nodeID
            self.nodeHashReverse[self.nodeID] = nid1
            self.nodes[self.nodeID] = [lon1, lat1]
            self.nodeLink[self.nodeID] = []
            self.nodeWeight[self.nodeID] = nodeweight1
            self.nodeID += 1

        if nid2 not in self.nodeHash.keys():
            self.nodeHash[nid2] = self.nodeID
            self.nodeHashReverse[self.nodeID] = nid2
            self.nodes[self.nodeID] = [lon2, lat2]
            self.nodeLink[self.nodeID] = []
            self.nodeWeight[self.nodeID] = nodeweight2
            self.nodeID += 1

        localid1 = self.nodeHash[nid1]
        localid2 = self.nodeHash[nid2]

        if localid1 * 10000000 + localid2 in self.edgeHash.keys():
            print("Duplicated Edge !!!", nid1, nid2)

            return self.edgeHash[(localid1, localid2)]

        self.edges[self.edgeID] = [localid1, localid2]
        self.edgeHash[(localid1, localid2)] = self.edgeID
        self.edgeWeight[self.edgeID] = edgeweight
        self.edgeID += 1

        if localid2 not in self.nodeLink[localid1]:
            self.nodeLink[localid1].append(localid2)

        return self.edgeID - 1

    def connectTwoNodes(self, n1, n2, edgeweight=0):
        lon1 = self.nodes[n1][0]
        lat1 = self.nodes[n1][1]

        lon2 = self.nodes[n2][0]
        lat2 = self.nodes[n2][1]

        nn1 = self.nodeHashReverse[n1]
        nn2 = self.nodeHashReverse[n2]

        return self.addEdge(nn1, lon1, lat1, nn2, lon2, lat2, edgeweight=edgeweight)

    def removeNode(self, nodeid):
        for next_node in self.nodeLink[nodeid]:
            edgeid = self.edgeHash[(nodeid, next_node)]

            del self.edges[edgeid]
            del self.edgeWeight[edgeid]
            del self.edgeHash[(nodeid, next_node)]

        self.deletedNodes[nodeid] = self.nodes[nodeid]
        del self.nodes[nodeid]
        del self.nodeWeight[nodeid]
        del self.nodeLink[nodeid]

    def removeDuplicateEdges(self):
        edges = {}
        c = 0
        for edgeID in self.edges.keys():
            if (self.edges[edgeID][0], self.edges[edgeID][1]) in edges.keys():
                del self.edges[edgeID]
                c += 1
            else:
                edges[(self.edges[edgeID][0], self.edges[edgeID][1])] = edgeID

        for edgeid, edge in edges.items():
            self.edgeHash[(edge[0], edge[1])] = edgeid

        print("Remove", c, "Duplicated Edges")

    def BiDirection(self):
        edgeList = list(self.edges.values())

        for edge in edgeList:
            localid1 = edge[1]
            localid2 = edge[0]

            self.edges[self.edgeID] = [localid1, localid2]
            self.edgeHash[(localid1, localid2)] = self.edgeID
            self.edgeWeight[self.edgeID] = self.edgeWeight[self.edgeHash[(
                localid2, localid1)]]
            self.edgeID += 1

            if localid2 not in self.nodeLink[localid1]:
                self.nodeLink[localid1].append(localid2)

    def getNeighbors(self, nodeid):
        neighbor = {}

        for next_node in self.nodeLink[nodeid]:
            if next_node != nodeid:
                neighbor[next_node] = 1

        return neighbor.keys()

    def getConnectedComponent(self, nodeID):
        node_list = []

        queue = [nodeID]

        while len(queue) > 0:
            n0 = queue.pop(0)
            node_list.append(n0)
            for n in self.nodeLink[n0]:
                if (n not in queue) and (n not in node_list):
                    queue.append(n)

        return node_list

    def removeConnectedComponent(self, size=0):
        node_list = []

        for n in self.nodes.keys():
            if n not in node_list:
                cclist = self.getConnectedComponent(n)

                if len(cclist) < size or size == 0:
                    for nn in cclist:
                        self.removeNode(nn)

                node_list = node_list + cclist

    def Dump2GeoJson(self, filename):

        print("Dump geojson to "+filename)

        myfeature = []

        for edgeId, edge in self.edges.items():
            n1, n2 = edge[0], edge[1]

            lon1 = self.nodes[n1][0]
            lat1 = self.nodes[n1][1]

            lon2 = self.nodes[n2][0]
            lat2 = self.nodes[n2][1]

            myfeature.append(Feature(properties={
                             "id": edgeId, "type": "residential"}, geometry=LineString([(lon1, lat1), (lon2, lat2)])))

        feature_collection = FeatureCollection(myfeature)

        with open(filename, "w") as fout:
            geojson.dump(feature_collection, fout, indent=2)

        print("Done.")

    def Dump2txt(self, filename):

        print("Dump text files to "+filename)
        file1 = open(filename+'_vertices.txt', 'w')
        file2 = open(filename+'_edges.txt', 'w')
        vertices = []

        for edgeId, edge in self.edges.items():
            n1, n2 = edge[0], edge[1]

            lon1 = self.nodes[n1][0]
            lat1 = self.nodes[n1][1]

            lon2 = self.nodes[n2][0]
            lat2 = self.nodes[n2][1]

            if self.nodes[n1] not in vertices:
                vertices.append(self.nodes[n1])
                file1.write(str(n1)+","+str(lon1)+","+str(lat1)+"\n")
            if self.nodes[n2] not in vertices:
                vertices.append(self.nodes[n2])
                file1.write(str(n2)+","+str(lon2)+","+str(lat2)+"\n")
            file2.write(str(edgeId)+","+str(n1)+","+str(n2)+"\n")

        file1.close()
        file2.close()
        print("Done.")

    def Plot2MatPlotLib(self):
        n = list()

        for id, edge in self.edges.items():
            n1_id, n2_id = edge[0], edge[1]
            n1, n2 = self.nodes[n1_id], self.nodes[n2_id]

            if n1 not in n:
                n.append(n1)
            if n2 not in n:
                n.append(n2)

            plt.plot([n1[0], n2[0]], [n1[1], n2[1]],
                     color='dimgray', linewidth=3)

        lons, lats = map(list, zip(*n))

        plt.scatter(lons, lats, s=200, c='dimgray')
        plt.show()
