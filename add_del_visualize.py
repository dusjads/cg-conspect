from random import randint
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import interact, interactive, IntSlider
from IPython.display import display

fig = plt.figure(figsize=(6, 6))
ax1 = plt.subplot(111, aspect='equal')
q, = ax1.plot([10], [10], 'o', color='yellow')
points = None


def generatePoints(n, N):
    gen_points = {(randint(0, n), randint(0, n)) for i in range(N)}
    while len(gen_points) < N:
        gen_points |= {(randint(0, n), randint(0, n))}
    return list(list(x) for x in gen_points)


def printPoints(fig, ax1, q, points):
    if printPoints.prevEdges is not None:
        for x in printPoints.prevEdges:
            x.remove()
        printPoints.prevEdges = None
    if printPoints.prevPoints is not None:
        printPoints.prevPoints.remove()
    tri = Delaunay(points)
    color = 'red'
    printPoints.prevEdges = ax1.triplot(points[:, 0], points[:, 1], tri.simplices.copy(), color=color)
    printPoints.prevPoints, = ax1.plot(points[:, 0], points[:, 1], 'o', color=color)
    display(fig)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)


def foundAndDel(new_q):
    global points
    #return False
    eps = 0.1
    for p in points:
        if abs(p[0] - new_q[0]) < eps and abs(p[1] - new_q[1]) < eps:
            points.remove(p)
            return True
    return False


def onRelease(event):
    global q, points, ax1
    if q is not None:
        q.remove()
    new_q = [event.xdata, event.ydata];
    if not foundAndDel(new_q):
        points.append(new_q)

    printPoints(fig, ax1, q, np.array(points))
    q, = ax1.plot([event.xdata], [event.ydata], 'o', color='yellow')

    display(fig)


def visualize():
    global fig, q, ax1, points

    fig.canvas.mpl_connect('button_release_event', onRelease)

    printPoints.prevEdges = None
    printPoints.prevPoints = None
    ax1.clear()

    q, = ax1.plot([10], [10], 'o', color='yellow')
    points = generatePoints(10, 10)
    printPoints(fig, ax1, q, np.array(points))



#
def debug():
    global points
    print(points)