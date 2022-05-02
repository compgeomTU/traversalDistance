
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

    inside_intervals = []

    for i in range(len(intervals)):
        """check space before and in next interval"""
        if Sx <= intervals[i][0]:
            beginningIndex = i
            # change the current interval to start at Sx
            ### intervals[i] = (Sx, intervals[i][1])
            intervals.append((Sx, intervals[i][1]))
            break  # and now find what we do with the larger
        elif Sx <= intervals[i][1]:
            # sx is in the middle of an interval
            # Sx becomes absorbed into this interval and then we look at the end
            beginningIndex = i
            flag = "inside"
            Sx = intervals[i][0]
            break

    print("beginning index: ", i)

    print("Sx = ", Sx)

    print("len intervals", len(intervals))
    # l = len(intervals)-1
    """for x in range(0, len(intervals), -1):  # THIS DOESNT WORK"""

    for x in [4, 3, 2, 1, 0]:
        print("\nEx=", Ex, end=" ")
        print("intervals[x]=", intervals[x], end=" ")
        if Ex >= intervals[x][1]:
            endIndex = x-1
            # intervals[x] = (intervals[x][0], Ex)
            intervals.append((intervals[x][0], Ex))
            """need to drop one to the right if"""
            # if x+1 < len(intervals):
            #     print("rm'd=", intervals[x+1], end=" ")
            #     intervals = intervals[:-1]
            # # break
        elif Ex >= intervals[x][0]:
            endIndex = x-1
            if flag == "inside":
                ## intervals[x] = (Sx, intervals[x][1])
                intervals.append((Sx, intervals[x][1]))
                # intervals.pop(x-1)
                ## intervals[x-1] = (None)
            else:
                # absorbed into interval
                Ex = intervals[x][0]
            break
    print("\nbeginning index=", beginningIndex, " end index=", endIndex)
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
case9 = [(.01, .1), (.2, .5), (.7, .9)
         ], (.3, .9)
# fails
case8 = [(.01, .1), (.2, .5), (.7, .9)
         ], (.03, .8)  # spans multiple --> needs to drop one smaller

case10 = [(0, .1), (.2, .3), (.4, .5), (.6, .7), (.8, .9)], (.25, .65)


c = case10
print("\nfinal = ", compute_union(c[0], c[1]))
