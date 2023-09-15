import math
import random

import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def __copy__(self):
        return Point(self.x, self.y)

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class Cluster:
    def __init__(self, points=None, centroid=None, color=None):
        self.points = points if points is not None else []
        self.centroid = centroid if centroid is not None else Point(0, 0)
        self.color = color if color is not None else np.random.rand(3, )

    def __eq__(self, other):
        if len(self.points) != len(other.points):
            return False
        if self.centroid != other.centroid:
            return False
        for i in range(len(self.points)):
            if self.points[i] != other.points[i]:
                return False
        return True

    def __str__(self):
        return str(self.points)

    def __copy__(self):
        new_cluster = Cluster()
        new_cluster.points = self.points.copy()
        new_cluster.centroid = self.centroid.__copy__()
        new_cluster.color = self.color.copy()
        return new_cluster

    def add_point(self, point):
        self.points.append(point)

    def clear_points(self):
        self.points = []

    def to_x_y(self):
        x = []
        y = []
        for point in self.points:
            x.append(point.x)
            y.append(point.y)
        return x, y

    def calculate_centroid(self):
        x = 0
        y = 0
        for point in self.points:
            x += point.x
            y += point.y
        self.centroid = Point(x / len(self.points), y / len(self.points))


class State:
    def __init__(self, clusters):
        self.clusters = []
        for cluster in clusters:
            self.clusters.append(cluster.__copy__())
        self.centroids = []
        self.points = []
        for cluster in clusters:
            self.centroids.append(cluster.centroid)
            self.points += cluster.points

    def __eq__(self, other):
        if len(self.clusters) != len(other.clusters):
            return False
        for i in range(len(self.clusters)):
            if self.clusters[i] != other.clusters[i]:
                return False
        return True

    def __str__(self):
        string = ''
        for cluster in self.clusters:
            string += str(cluster) + '\n'
        return string

    def show(self, plot):
        for i in range(len(self.clusters)):
            cluster = self.clusters[i]
            x, y = cluster.to_x_y()
            plot.scatter(x, y, color=cluster.color, s=10)

        x = []
        y = []
        for centroid in self.centroids:
            x.append(centroid.x)
            y.append(centroid.y)
        plot.scatter(x, y, s=100, c='k', marker='x')


def random_point(min_x, max_x, min_y, max_y):
    x = random.uniform(min_x, max_x)
    y = random.uniform(min_y, max_y)
    return Point(x, y)


def generate_points(n):
    points = []
    for i in range(n):
        point = random_point(0,n, 0, n)
        points.append(point)
    return points


def assign_points_to_nearest_clusters(points, clusters):
    for cluster in clusters:
        cluster.clear_points()

    for point in points:
        min_distance = float('inf')
        min_cluster = None
        for cluster in clusters:
            distance = point.distance(cluster.centroid)
            if distance < min_distance:
                min_distance = distance
                min_cluster = cluster
        min_cluster.add_point(point)
