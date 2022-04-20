
# TODO: need to take union of all intervals
# compare these two with the items we have in the list
#[(mycb.start_p, mycb.end_p)]

def compute_union(intervals, mycb):
    print("--my cbs: ", mycb, "  --intervals: ", intervals)
    Sx, Ex = mycb

    # entirely before
    if Sx > intervals[len(intervals)-1][1]:
        intervals += [(mycb)]
        return intervals
    # entirely after
    elif Ex < intervals[0][0]:
        intervals = [(mycb)] + intervals
        return intervals

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

    print("Sx = ", Sx)

    print(i, len(intervals))
    for x in range(0, len(intervals)):
        print("x = ", x)
        print("- ", intervals[x])
        if Ex >= intervals[x][1]:
            intervals[x] = (intervals[x][0], Ex)
            break
        elif Ex > intervals[i][0]:
            # absorbed into inverval
            Ex = intervals[i][0]
            break

    # print(intervals)
    return intervals


# assume current intervals are sorted
case1 = [(0, .1), (.2, .5), (.8, 1)], (.6, .7)  # works
case2 = [(0, .1), (.2, .5), (.7, .9)], (.6, .8)  # works
case3 = [(0, .1), (.2, .5)], (.6, .8)  # works
case4 = [(.3, .4), (.6, .8)], (0, .1)  # works

case5 = [(.2, .7),  (.8, .9)], (.6, .85)

c = case5
print(compute_union(c[0], c[1]))
