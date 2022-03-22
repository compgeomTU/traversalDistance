# Last edited: 2022-03-17
# Author: Erfan Hosseini Sereshgi - Tulane University

import math

def find_ellipse_max_min_points(line1, line2, epsilon):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b): # Find det given two vectors
        return a[0] * b[1] - a[1] * b[0]

    def slope(x1, y1, x2, y2): # Find line slope given two points
        if x2 == x1: 
            return math.inf
        return (y2 - y1)/(x2 - x1)
    
    def vector(x1, y1, x2, y2): # Find vector given two points
        return (y2 - y1, x2 - x1)

    def length(v):
        return math.sqrt(v[0]**2 + v[1]**2)

    def fraction_of_segment(p1, p2, p):
        return (length(vector(*p1, *p)) / length(vector(*p1, *p2)))     

    def distance_between_two_parallel_lines(line1, line2):
        # Find the distance between line1 and an end-point of line2
        a = line1[0][1] - line1[1][1]
        b = line1[1][0] - line1[0][0]
        c = line1[0][0] * line1[1][1] - line1[1][0] * line1[0][1]
        x = line2[0][0]
        y = line2[0][1]
        return abs((a * x + b * y + c)) / (math.sqrt(a * a + b * b))

    def circle_line_segment_intersection(p1x, p1y, p2x, p2y, cx, cy, r, full_line=False, tangent_tol=1e-9):
        # Find the intersection of a circle and a line segment
        
        (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
        dx, dy = (x2 - x1), (y2 - y1)
        dr = (dx ** 2 + dy ** 2) ** .5
        big_d = x1 * y2 - x2 * y1
        discriminant = r ** 2 * dr ** 2 - big_d ** 2

        if discriminant < 0:  # No intersection between circle and line
            return []
        else:  # There may be 0, 1, or 2 intersections with the segment
            intersections = [
                (cx + (big_d * dy + sign * (-1 if dy < 0 else 1) * dx * discriminant ** .5) / dr ** 2,cy + (-big_d * dx + sign * abs(dy) * discriminant**.5) / dr ** 2)
                for sign in ((1, -1) if dy < 0 else (-1, 1))]  # This makes sure the order along the segment is correct
            if not full_line:  # If only considering the segment, filter out intersections that do not fall within the segment
                fraction_along_segment = [(xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy for xi, yi in intersections]
                intersections = [pt for pt, frac in zip(intersections, fraction_along_segment) if 0 <= frac <= 1]
            if len(intersections) == 2 and abs(discriminant) <= tangent_tol:  # If line is tangent to circle, return just one point (as both intersections have same location)
                return [intersections[0]]
            else:
                return intersections   

    div = det(xdiff, ydiff)
    if div == 0: #lines do not intersect
       distance = distance_between_two_parallel_lines(line1, line2) # distance between two parallel lines
       point1 = circle_line_segment_intersection(line1[0][0], line1[0][1], line1[1][0], line1[1][1], line2[0][0], line2[0][1], epsilon, full_line=False, tangent_tol=1e-9)
       point2 = circle_line_segment_intersection(line1[0][0], line1[0][1], line1[1][0], line1[1][1], line2[1][0], line2[1][1], epsilon, full_line=False, tangent_tol=1e-9)
       point3 = circle_line_segment_intersection(line2[0][0], line2[0][1], line2[1][0], line2[1][1], line1[0][0], line1[0][1], epsilon, full_line=False, tangent_tol=1e-9)
       point4 = circle_line_segment_intersection(line2[0][0], line2[0][1], line2[1][0], line2[1][1], line1[1][0], line1[1][1], epsilon, full_line=False, tangent_tol=1e-9)
       point1_normalized = fraction_of_segment(*line1, point1[0])
       point2_normalized = fraction_of_segment(*line1, point2[0])
       point3_normalized = fraction_of_segment(*line2, point3[0])
       point4_normalized = fraction_of_segment(*line2, point4[0])
       return point1,point2,point3,point4 # max and min points

    d = (det(*line1), det(*line2))
    inter_x = det(d, xdiff) / div
    inter_y = det(d, ydiff) / div

    print("intersection point: ", inter_x, inter_y)

    v1 = vector(line1[0][0], line1[0][1], line1[1][0], line1[1][1])
    v2 = vector(line2[0][0], line2[0][1], line2[1][0], line2[1][1])

    cos_alpha = (v1[0] * v2[0] + v1[1] * v2[1]) / (math.sqrt(v1[0] ** 2 + v1[1] ** 2) * math.sqrt(v2[0] ** 2 + v2[1] ** 2))
    sin_alpha = math.sqrt(1-cos_alpha ** 2)
    d = epsilon / sin_alpha

    m1 = slope(line1[0][0], line1[0][1], line1[1][0], line1[1][1])
    m2 = slope(line2[0][0], line2[0][1], line2[1][0], line2[1][1])

    print("m1: ",m1)
    print("m2: ",m2)

    # line 1
    if m1 == math.inf:
        if inter_y + d > max(line1[0][1], line1[1][1]):
            max1 = (inter_x, max(line1[0][1], line1[1][1]))
        else:
            max1 = (inter_x,inter_y + d)
        if inter_y - d < min(line1[0][1], line1[1][1]):
            min1 = (inter_x, min(line1[0][1], line1[1][1]))
        else:
            min1 = (inter_x,inter_y - d)
    else:
        x1 = d / math.sqrt(m1 * m1 + 1)
        y1 = m1 * x1
        if inter_x + x1 > max(line1[0][0], line1[1][0]):
            if line1[0][0] > line1[1][0]:
                max1 = (line1[0][0], line1[0][1])
            else:
                max1 = (line1[1][0], line1[1][1])
        else:
            max1 = (inter_x + x1,inter_y + y1)
        
        if inter_x - x1 < min(line1[0][0], line1[1][0]):
            if line1[0][0] < line1[1][0]:
                min1 = (line1[0][0], line1[0][1])
            else:
                min1 = (line1[1][0], line1[1][1])
        else:
            min1 = (inter_x - x1,inter_y - y1)

    # line 2
    if m2 == math.inf:
        if inter_y + d > max(line2[0][1], line2[1][1]):
            max2 = (inter_x, max(line2[0][1], line2[1][1]))
        else:
            max2 = (inter_x, inter_y+d)
        if inter_y - d < min(line2[0][1], line2[1][1]):
            min2 = (inter_x, min(line2[0][1], line2[1][1]))
        else:
            min2 = (inter_x, inter_y - d)
    else:
        x2 = d / math.sqrt(m2 * m2 + 1)
        y2 = m2 * x2
        if inter_x + x2 > max(line2[0][0], line2[1][0]):
            if line2[0][0] > line2[1][0]:
                max2 = (line2[0][0], line2[0][1])
            else:
                max2 = (line2[1][0], line2[1][1])
        else:
            max2 = (inter_x + x2, inter_y + y2)
        if inter_x - x2 < min(line2[0][0], line2[1][0]):
            if line2[0][0] < line2[1][0]:
                min2 = (line2[0][0], line2[0][1])
            else:
                min2 = (line2[1][0], line2[1][1])
        else:
            min2 = (inter_x - x2, inter_y - y2)

    min1_normalized = fraction_of_segment(*line1, min1)
    max1_normalized = fraction_of_segment(*line1, max1)
    min2_normalized = fraction_of_segment(*line2, min2)
    max2_normalized = fraction_of_segment(*line2, max2)

    return min1_normalized, min2_normalized, max1_normalized, max2_normalized


#test 

line1 = [[0, 0],[0, 3]]
line2 = [[1, -2],[2, 3]]
epsilon = 1
print(line1)
print(line2)
print(find_ellipse_max_min_points(line1, line2, epsilon))
