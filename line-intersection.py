import math

def find_ellipse_max_min_points(line1, line2, epsilon):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b): # Find det given two vectors
        return a[0] * b[1] - a[1] * b[0]

    def slope(x1, y1, x2, y2): # Find line slope given two points:
        return (y2-y1)/(x2-x1)

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    inter_x = det(d, xdiff) / div
    inter_y = det(d, ydiff) / div

    print("intersection point: ",inter_x,inter_y)

    m1 = slope(line1[0][0], line1[0][1], line1[1][0], line1[1][1])
    m2 = slope(line2[0][0], line2[0][1], line2[1][0], line2[1][1])

    print("m1: ",m1)
    print("m2: ",m2)

    if (abs((m1-m2)/(1+(m2*m1)))/(math.pi/2))%2 != 1:
        tan_alpha = abs((m1-m2)/(1+(m2*m1)))
        d = epsilon/tan_alpha # length from intersection point to max/min point on each line
        # line 1
        x1 = d/math.sqrt(m1*m1+1)
        y1 = m1*x1
        max1 = (inter_x+x1,inter_y+y1)
        min1 = (inter_x-x1,inter_y-y1)
        # line 2
        x2 = d/math.sqrt(m2*m2+1)
        y2 = m2*x2
        max2 = (inter_x+x2,inter_y+y2)
        min2 = (inter_x-x2,inter_y-y2)

        return min1, min2, max1, max2
    else:
        raise Exception("The angle is an odd multiply of pi/2 hence no tan and no tan")

#test
line1 = [[1,0],[-4,3]]
line2 = [[-2,3],[1,-3]]
epsilon = 2
print(find_ellipse_max_min_points(line1, line2, epsilon))
