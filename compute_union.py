"""
Author:
Rena Repenning
renarepenning@gmail.com

Contributor:
Emily Powers
epowers3@tulane.edu
"""

# TODO: need to take union of all intervals
# compare these two with the items we have in the list
# [(mycb.start_p, mycb.end_p)]

from operator import invert


def compute_union(intervals, mycb):
    print("--my cbs: ", mycb, "  --intervals: ", intervals)
    Sx, Ex = mycb
    flag = ""
    new_interval = (-1, -1)

    # entirely before
    if Sx > intervals[len(intervals)-1][1]:
        intervals += [(mycb)]
        return intervals
    # entirely after
    elif Ex < intervals[0][0]:
        intervals = [(mycb)] + intervals
        return intervals

    #to remove
    inside_intervals = []
    
    for i in range(len(intervals)):
        if Sx <= intervals[i][0]:
            #add smaller interval to list to remove
            inside_intervals.append(intervals[i])  
            #check if Ex covers more than current interval
            if Ex <= intervals[i][1]:
                #readjust the new interval to include Sx 
                new_interval = (Sx, intervals[i][1])
                break
        elif Sx <= intervals[i][1]:
            #reset starting index to be min in interval
            Sx = intervals[i][0]
            inside_intervals.append(intervals[i])

    print("to remove:", inside_intervals)
    print("new interval=", new_interval)

    new = [i for i in intervals if i not in inside_intervals]
    new.append(new_interval)
    
    return new


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
print("final = ", compute_union(c[0], c[1]))
