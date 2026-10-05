"""Lightweight straight-line graph representation used by traversal_distance."""

from __future__ import annotations

from pathlib import Path


class Graph:
    """Finite straight-line graph with integer IDs and 2-D vertex coordinates.

    When ``filename`` is supplied, two files are read::

        <filename>_vertices.txt   vertex_id,x,y
        <filename>_edges.txt      edge_id,start_vertex_id,end_vertex_id
    """

    def __init__(self, filename=None):
        self.nodes = {}
        self.edges = {}
        self.nodeLink = {}
        self.edgeHash = {}
        self.numberOfNodes = 0
        self.numberOfEdges = 0
        self.largestEdgeID = -1

        if filename is not None:
            self.read(filename)

    def read(self, filename):
        prefix = str(filename)
        with open(prefix + "_vertices.txt", "r", encoding="utf-8") as vf:
            for line in vf:
                line = line.strip()
                if not line:
                    continue
                vertex_id, x, y = line.split(",")[:3]
                self.addNode(int(vertex_id), float(x), float(y))

        with open(prefix + "_edges.txt", "r", encoding="utf-8") as ef:
            for line in ef:
                line = line.strip()
                if not line:
                    continue
                edge_id, u, v = line.split(",")[:3]
                self.connectTwoNodes(int(edge_id), int(u), int(v))
        return self

    def addNode(self, nid, x, y):
        if nid in self.nodes:
            raise ValueError(f"duplicate node ID {nid}")
        self.nodes[nid] = [float(x), float(y)]
        self.nodeLink[nid] = []
        self.numberOfNodes += 1
        return nid

    def connectTwoNodes(self, eid, n1, n2):
        if eid in self.edges:
            raise ValueError(f"duplicate edge ID {eid}")
        if n1 not in self.nodes or n2 not in self.nodes:
            raise KeyError(f"edge {eid} references unknown node(s): {n1}, {n2}")
        self.edges[eid] = [n1, n2]
        self.edgeHash[(n1, n2)] = eid
        self.edgeHash[(n2, n1)] = eid
        if n2 not in self.nodeLink[n1]:
            self.nodeLink[n1].append(n2)
        if n1 not in self.nodeLink[n2]:
            self.nodeLink[n2].append(n1)
        self.numberOfEdges += 1
        self.largestEdgeID = max(self.largestEdgeID, eid)
        return eid

    @classmethod
    def from_data(cls, nodes, edges):
        graph = cls()
        for nid, point in nodes.items():
            graph.addNode(nid, point[0], point[1])
        for eid, edge in edges.items():
            graph.connectTwoNodes(eid, edge[0], edge[1])
        return graph
