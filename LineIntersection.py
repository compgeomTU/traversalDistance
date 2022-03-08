import math

def find_ellipse_max_min_points(line1, line2, epsilon):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b): # Find det given two vectors
        return a[0] * b[1] - a[1] * b[0]

    def slope(x1, y1, x2, y2): # Find line slope given two points
        if x2==x1: 
            return math.inf
        return (y2-y1)/(x2-x1)
    
    def vector(x1, y1, x2, y2):
        return (y2-y1,x2-x1)

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    inter_x = det(d, xdiff) / div
    inter_y = det(d, ydiff) / div

    print("intersection point: ",inter_x,inter_y)

    v1 = vector(line1[0][0], line1[0][1], line1[1][0], line1[1][1])
    v2 = vector(line2[0][0], line2[0][1], line2[1][0], line2[1][1])

    cos_alpha = (v1[0]*v2[0]+v1[1]*v2[1])/(math.sqrt(v1[0]**2 + v1[1]**2)*math.sqrt(v2[0]**2 + v2[1]**2))
    sin_alpha = math.sqrt(1-cos_alpha**2)
    d = epsilon/sin_alpha

    m1 = slope(line1[0][0], line1[0][1], line1[1][0], line1[1][1])
    m2 = slope(line2[0][0], line2[0][1], line2[1][0], line2[1][1])

    print("m1: ",m1)
    print("m2: ",m2)

    # line 1
    if m1 == math.inf:
        if inter_y+d > max(line1[0][1], line1[1][1]):
            max1 = (inter_x, max(line1[0][1], line1[1][1]))
        else:
            max1 = (inter_x,inter_y+d)
        if inter_y-d < min(line1[0][1], line1[1][1]):
            min1 = (inter_x, min(line1[0][1], line1[1][1]))
        else:
            min1 = (inter_x,inter_y-d)
    else:
        x1 = d/math.sqrt(m1*m1+1)
        y1 = m1*x1
        if inter_x+x1 > max(line1[0][0], line1[1][0]):
            if line1[0][0] > line1[1][0]:
                max1 = (line1[0][0], line1[0][1])
            else:
                max1 = (line1[1][0], line1[1][1])
        else:
            max1 = (inter_x+x1,inter_y+y1)
        
        if inter_x-x1 < min(line1[0][0], line1[1][0]):
            if line1[0][0] < line1[1][0]:
                min1 = (line1[0][0], line1[0][1])
            else:
                min1 = (line1[1][0], line1[1][1])
        else:
            min1 = (inter_x-x1,inter_y-y1)

    # line 2
    if m2 == math.inf:
        if inter_y+d > max(line2[0][1], line2[1][1]):
            max2 = (inter_x, max(line2[0][1], line2[1][1]))
        else:
            max2 = (inter_x,inter_y+d)
        if inter_y-d < min(line2[0][1], line2[1][1]):
            min2 = (inter_x, min(line2[0][1], line2[1][1]))
        else:
            min2 = (inter_x,inter_y-d)
    else:
        x2 = d/math.sqrt(m2*m2+1)
        y2 = m2*x2
        if inter_x+x2 > max(line2[0][0], line2[1][0]):
            if line2[0][0] > line2[1][0]:
                max2 = (line2[0][0], line2[0][1])
            else:
                max2 = (line2[1][0], line2[1][1])
        else:
            max2 = (inter_x+x2,inter_y+y2)
        if inter_x-x2 < min(line2[0][0], line2[1][0]):
            if line2[0][0] < line2[1][0]:
                min2 = (line2[0][0], line2[0][1])
            else:
                min2 = (line2[1][0], line2[1][1])
        else:
            min2 = (inter_x-x2,inter_y-y2)


    return min1, min2, max1, max2


#test
#line1 = [[1,0],[-4,3]]
#line2 = [[-2,3],[1,-3]]
#epsilon = 2
#print(find_ellipse_max_min_points(line1, line2, epsilon))
