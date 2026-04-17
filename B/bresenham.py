"""
Bresenham is a straight line drawing algorithm using integer calculation.
Not using floating point (slow)

It is an incremental scan conversion algorithm used to draw a straight line using only integer arithmetic by choosing the nearest pixel at each step

We start with two points A (x0,y0) and B (x1,y1) forming a straight line.

The distance x1-x0 is Dx 
and y1-y0 is Dy


def drawLine(x0,y0,x1,y1):
    dx = x1-x0
    dy = y1-y0
    step = max(abs(dx),abs(dy))

    if step != 0:
        stepX = dx/step
        stepY = dy/step

        for i in range(step+1):
            putPixel(round(x0 + i + stepX), round(y0 + i + stepY))


    DISADVANTAGE ABOVE: It uses float while we have pixel in integer forms.
                        thus high processing time, slowing down performance.
****************************************************************************************                    


In brasenhem, X will always increase but whether y will be y or y+1 we need to decide
so let there be three variables 
    y (actual point)
    yk and y(k)+1
    here d1 = y-yk
         d2 = y(k)+1 - y

    if d1-d2 < 0 (closer to d1) => yk
    d1-d2>0 closer to d2        => y (k+1)



    y = mx + c
    d1 = mx + c - yk
    d2 = y(k)+1 - mx -c
    d1 - d2 = mx + c - yk - y(k)-1 + mx + c
    d1 - d2 = 2mx + 2c -2yk -1
    to eliminate m we know m = dy/dx
    multipy both sides by dx

    (d1-d2)dx = 2dyx + 2cdx - 2(yk)dx -dx

    here 2cdx - dx is constant so 
    and (d1-d2)dx = P

    P = 2dyx -2ykdx
    P(next) = 2*dy*x(next) - 2*dx*yk(next)

    P(next) - P 


a decision parameter (p)
 if p < 0 :
        chose E(x+1,y)
        P = P + 2dy
if p >= 0 :
        chose E(x+1,y+1)
        P = P + 2dy - 2dx


plotLine(x0,y0,x1,y1)
    dx =x1-x0
    dy = y1-y0
    P = 2*dy -dx
    y=y0

    for x from x0 to x1
        plot(x,y)
        if D > 0
            y+=1
            P = P - 2*dx
        end if
        P = P + 2*dy
"""

import matplotlib.pyplot as plt

def bresenham(x0,y0,x1,y1):
    points = []

    dx = abs(x1-x0)
    dy = abs(y1-y0)

    x,y = x0,y0
    sx = 1 if x1 > x0 else -1
    sy = 1 if y1 > y0 else -1


    # decision parameter p
    p = 2*dy - dx

    for _ in range(dx+1):
        points.append((x,y))
        if p < 0 :
            x = x + sx
            p = p + 2*dy
        else:
            x = x + sx
            y = y + sy
            p = p + 2*dy - 2*dx
    return points


x0,y0=2,3
x1,y1 = 15,10

pts =bresenham(x0,y0,x1,y1)
# Plot
xs = [p[0] for p in pts]
ys = [p[1] for p in pts]

plt.plot(xs, ys, 'ro-')
plt.grid()
plt.axis('equal')
plt.title("Bresenham Line Drawing Algorithm")
plt.show()