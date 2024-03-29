import numpy as np
import math
import matplotlib.pyplot as plt
import namemapping as nm
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distanceToCenter(self, center):
        return math.sqrt((center.x - self.x) ** 2 + (center.y - self.y) ** 2)


class Rectangle:
    def __init__(self, center, width, height):
        self.center = center
        self.width = width
        self.height = height
        self.west = center.x - width
        self.east = center.x + width
        self.north = center.y - height
        self.south = center.y + height

    def containsPoint(self, point):
        return (self.west <= point.x < self.east and
                self.north <= point.y < self.south)

    def intersects(self, range):
        return not (range.west > self.east or
                    range.east < self.west or
                    range.north > self.south or
                    range.south < self.north)

    def draw(self, ax, c='k', lw=1, **kwargs):
        x1, y1 = self.west, self.north
        x2, y2 = self.east, self.south
        ax.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], c=c, lw=lw, **kwargs)


class QuadTree:
    def __init__(self, boundary, capacity=4):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False

    def insert(self, point):
        # if the point is in the range of current quadTree
        if not self.boundary.containsPoint(point):
            return False

        # if has not reached capcaity
        if len(self.points) < self.capacity:
            self.points.append(point)
            return True

        if not self.divided:
            self.divide()

        if self.nw.insert(point):
            return True
        elif self.ne.insert(point):
            return True
        elif self.sw.insert(point):
            return True
        elif self.se.insert(point):
            return True

        return False

    def queryRange(self, range):
        found_points = []

        if not self.boundary.intersects(range):
            return []

        for point in self.points:
            if range.containsPoint(point):
                found_points.append(point)

        if self.divided:
            found_points.extend(self.nw.queryRange(range))
            found_points.extend(self.ne.queryRange(range))
            found_points.extend(self.sw.queryRange(range))
            found_points.extend(self.se.queryRange(range))

        return found_points

    def queryRadius(self, range, center):
        found_points = []

        if not self.boundary.intersects(range):
            return []

        for point in self.points:
            if range.containsPoint(point) and point.distanceToCenter(center) <= range.width:
                found_points.append(point)

        if self.divided:
            found_points.extend(self.nw.queryRadius(range, center))
            found_points.extend(self.ne.queryRadius(range, center))
            found_points.extend(self.sw.queryRadius(range, center))
            found_points.extend(self.se.queryRadius(range, center))

        return found_points

    def divide(self):
        center_x = self.boundary.center.x
        center_y = self.boundary.center.y
        new_width = self.boundary.width / 2
        new_height = self.boundary.height / 2

        nw = Rectangle(Point(center_x - new_width, center_y - new_height), new_width, new_height)
        self.nw = QuadTree(nw)

        ne = Rectangle(Point(center_x + new_width, center_y - new_height), new_width, new_height)
        self.ne = QuadTree(ne)

        sw = Rectangle(Point(center_x - new_width, center_y + new_height), new_width, new_height)
        self.sw = QuadTree(sw)

        se = Rectangle(Point(center_x + new_width, center_y + new_height), new_width, new_height)
        self.se = QuadTree(se)

        self.divided = True

    def __len__(self):
        count = len(self.points)
        if self.divided:
            count += len(self.nw) + len(self.ne) + len(self.sw) + len(self.se)

        return count

    def draw(self, ax):
        self.boundary.draw(ax)

        if self.divided:
            self.nw.draw(ax)
            self.ne.draw(ax)
            self.se.draw(ax)
            self.sw.draw(ax)
DPI = 72
width, height = 600, 400
N = 1000
xs = np.random.rand(N) * width
ys = np.random.rand(N) * height
points = [Point(xs[i], ys[i]) for i in range(N)]
domain = Rectangle(Point(width/2, height/2), width/2, height/2)
qtree = QuadTree(domain)
for point in points:
    nm.utilmap(point)
    qtree.insert(point)

print('Total points: ', len(qtree))

fig = plt.figure(figsize=(700/DPI, 500/DPI), dpi=DPI)
ax = plt.subplot()
ax.set_xlim(0, width)
ax.set_ylim(0, height)
qtree.draw(ax)


ax.scatter([p.x for p in points], [p.y for p in points], s=4)
ax.set_xticks([])
ax.set_yticks([])

center_x = 300
center_y = 200
range_width = np.random.rand() * min(center_x, width - center_x)
range_height = np.random.rand() * min(center_y, height - center_y)
found_points = []
radius = int(input("Enter the radius you want to search : "))
range = Rectangle(Point(center_x, center_y), radius, radius)
found_points = qtree.queryRadius(range, Point(center_x, center_y))

print('points in range:', len(found_points))

ax.scatter([p.x for p in found_points], [p.y for p in found_points],
            facecolors='none', edgecolors='g', s=32)

range.draw(ax, c='darkviolet', lw=2)

ax.invert_yaxis()
plt.tight_layout()
plt.show()