
# TODO: need to take union of all intervals
# compare these two with the items we have in the list
#[(mycb.start_p, mycb.end_p)]

def compute_union(intervals, mycb):
    Sx, Ex = mycb
    print(mycb)
    print(intervals)
    for i in range(len(intervals)):
        """check space before and in next interval"""
        if Sx <= intervals[i][0]:
            # change the current interval to start at Sx
            intervals[i] = (Sx, intervals[i][1])
            break  # and now find what we do with the larger
        elif Sx <= intervals[i][1]:
            # sx is in the middle of an interval
            # Sx becomes absorbed into this interval and then we look at the end
            Sx = intervals[i][0]
            break
        else:
            print("on to next interval")

    for x in range(i, len(intervals), -1):
        if Ex >= intervals[x][1]:
            intervals[x] = (intervals[x][0], Ex)
            break
        elif Ex > intervals[i][0]:
            # absorbed into inverval
            Ex = intervals[i][0]
            break

    print(intervals)
    # return intervals


# assume current intervals are sorted
case1 = [(0, .1), (.2, .5), (.8, 1)], (.6, .7)
case2 = [(0, .1), (.2, .5), (.7, .9)], (.6, .8)
case3 = [(0, .1), (.2, .7),  (.8, .9)], (.6, .9)

c = case3
compute_union(c[0], c[1])
