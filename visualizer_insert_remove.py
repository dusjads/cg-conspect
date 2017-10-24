from random import randint
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import interact, interactive, IntSlider
from IPython.display import display
from random import random

fig = plt.figure(figsize=(6, 6))
ax1 = plt.subplot(111, aspect='equal')
q, = ax1.plot([10], [10], 'o', color='yellow')


def generatePoints(n, N):
    points = {(randint(0, n), randint(0, n)) for i in range(N)}
    while len(points) < N:
        points |= {(randint(0, n), randint(0, n))}
    return list(list(x) for x in points)


def redrawClosest(q, points, ax1):
    def nn(q, points):
        def dist(x):
            return (x[0] - q[0]) * (x[0] - q[0]) + (x[1] - q[1]) * (x[1] - q[1])

        return sorted(points, key=dist)[0]

    if redrawClosest.closestPoint is not None:
        redrawClosest.closestPoint.remove()
    closest = nn((q.get_xdata()[0], q.get_ydata()[0]), points)
    redrawClosest.closestPoint, = ax1.plot([closest[0]], [closest[1]], 'o', color='blue')


redrawClosest.closestPoint = None


def printPoints(fig, ax1, q, points, redraw=True):
    if printPoints.prevEdges is not None:
        for x in printPoints.prevEdges:
            x.remove()
        printPoints.prevEdges = None
    if printPoints.prevPoints is not None:
        printPoints.prevPoints.remove()

    color = 'red'

    if (len(points) == 3):
        printPoints.prevEdges = ax1.triplot(points[:, 0], points[:, 1], np.array([[0, 1, 2]]), color=color)
    if (len(points) >= 4):
        tri = Delaunay(points)
        printPoints.prevEdges = ax1.triplot(points[:, 0], points[:, 1], tri.simplices.copy(), color=color)
    printPoints.prevPoints, = ax1.plot(points[:, 0], points[:, 1], 'o', color=color)

    redrawClosest(q, points, ax1)

    if redraw:
        display(fig)
    ax1.set_xlim(0, 20)
    ax1.set_ylim(0, 20)


printPoints.prevPoints = printPoints.prevEdges = None


def onRelease(event):
    global q, points, ax1
    if q is not None:
        q.remove()
    q, = ax1.plot([event.xdata], [event.ydata], 'o', color='yellow')
    points.append([event.xdata, event.ydata])
    printPoints(fig, ax1, q, points)
    display(fig)


def redrawPoints(redraw = True):
    if redraw:
        printPoints(fig, ax1, q, points, redraw)

def visualize():
    global fig, ax1, q
    fig.canvas.mpl_connect('button_release_event', onRelease)

    ax1.clear()

    q, = ax1.plot([10], [10], 'o', color='yellow')

    points = generatePoints(20, 20)
    printPoints(fig, ax1, q, points)  # printing gray imprint

    # ax1.text(2, 2, len(levels))

    #display(interactive(printPoints, (fig, ax1, q, points)))
    printPoints(fig, ax1, q, points)
