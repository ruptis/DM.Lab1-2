from common import *


def kmeans_clustering(state):
    states = []

    new_state = kmeans_step(state)
    while new_state != state:
        state = new_state
        states.append(state)
        new_state = kmeans_step(state)
    return states


def kmeans_step(state):
    clusters = [cluster.__copy__() for cluster in state.clusters]
    assign_points_to_nearest_clusters(state.points, clusters)

    for cluster in clusters:
        cluster.calculate_centroid()

    return State(clusters)
