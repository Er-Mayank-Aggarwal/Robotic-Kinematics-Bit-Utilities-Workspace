import matplotlib.pyplot as plt

def plot_circle_points(xc, yc, x, y):
    points = [
        (xc + x, yc + y),
        (xc - x, yc + y),
        (xc + x, yc - y),
        (xc - x, yc - y),
        (xc + y, yc + x),
        (xc - y, yc + x),
        (xc + y, yc - x),
        (xc - y, yc - x),
    ]
    return points


def midpoint_circle(r, xc=0, yc=0):
    x = 0
    y = r
    p = 1 - r

    all_points = []

    while x <= y:
        all_points += plot_circle_points(xc, yc, x, y)

        if p < 0:
            x += 1
            p = p + 2*x + 1
        else:
            x += 1
            y -= 1
            p = p + 2*x - 2*y + 1

    return all_points


# Example
pts = midpoint_circle(10)

xs = [p[0] for p in pts]
ys = [p[1] for p in pts]

plt.scatter(xs, ys, s=10)
plt.axis('equal')
plt.grid()
plt.title("Midpoint Circle Algorithm")
plt.show()