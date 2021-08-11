# read in a graph
# read in a curve
# calculate free space
# return something that can be visualized

def calfreespace(x1, y1, x2, y2, xa, ya, start, end):
 #  Input:   A line segment starting in (x1, y1) and ending in (x2,y2) -- the order is important!
 #           A point (xa, ya)
 #  Output:  The two points on the boundary of the free space diagram: start, end
 #           Hopefully start and end lie between 0 and 1  (this should be checked!)

  xdiff, ydiff, root, b, divisor, t1, t2, q;

  xdiff=x2-x1
  ydiff=y2-y1
  divisor =xdiff*xdiff+ydiff*ydiff
  if(divisor==0):
    print("divisor=%lf; x1=%lf, x2=%lf, y1=%lf, y2=%lf\n",divisor,x1,x2,y1,y2)
  b=(xa-x1)*xdiff+(ya-y1)*ydiff
  q=(x1*x1+y1*y1+xa*xa+ya*ya-2*x1*xa-2*y1*ya-ERROR*ERROR)*divisor
  root= b*b-q 
  if(root<0):
    start=end=-1 
    return
  root=sqrt(root)
  t2= (b+root)/divisor
  t1= (b-root)/divisor
  if(t1<0): t1=0
  if(t2<0): t2=0
  if(t1>1): t1=1
  if(t2>1): t2=1
  start=t1
  end=t2
  #make sure black intervals are correctly marked black
  if(start==end):
    start=-1
    end=-1
