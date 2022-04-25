
# TODO: need to take union of all intervals
# compare these two with the items we have in the list
# [(mycb.start_p, mycb.end_p)]

from operator import invert


def compute_union(intervals, mycb):
    print("--my cbs: ", mycb, "  --intervals: ", intervals)
    Sx, Ex = mycb
    flag = ""

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
            flag = "inside"
            Sx = intervals[i][0]
            break

    print("Sx = ", Sx)

    # print(i, len(intervals))
    l = len(intervals)-1
    print(l)

    # for x in range(0, 2, -1): ## THIS DOESNT WORK
    for x in [2, 1, 0]:
        print("Ex = ", Ex)
        print("intervals[x]", intervals[x])
        if Ex >= intervals[x][1]:
            intervals[x] = (intervals[x][0], Ex)
            """need to drop one to the right if possible"""
            # break
        elif Ex >= intervals[x][0]:
            if flag == "inside":
                intervals[x] = (Sx, intervals[x][1])
                intervals[x-1] = (None)
            else:
                # absorbed into interval
                Ex = intervals[x][0]
            break
        else:
            print("next")

    # print(intervals)
    return intervals


"""assume current intervals are sorted"""
# works
case1 = [(0, .1), (.2, .5), (.8, 1)], (.6, .7)
case2 = [(0, .1), (.2, .5), (.7, .9)], (.6, .8)
case5 = [(.2, .5), (.7, .9)], (.1, .3)
case3 = [(0, .1), (.2, .5)], (.6, .8)
case4 = [(.3, .4), (.6, .8)], (0, .1)
case6 = [(.2, .7),  (.8, .9)], (.6, .75)  # works but not with -1 step
case7 = [(.1, .19), (.2, .5), (.7, .9), (.91, .93)
         ], (.15, .22)  # (.3, .8)  # needs to drop none -- spans two
# fails
case8 = [(.01, .1), (.2, .5), (.7, .9)
         ], (.03, .8)  # spans multiple --> needs to drop one smaller

case9 = [(.01, .1), (.2, .5), (.7, .9)
         ], (.3, .9)


c = case9
print("final = ", compute_union(c[0], c[1]))
