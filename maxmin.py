from common import Cluster, State, assign_points_to_nearest_clusters


def maxmin_clustering(points):
    states = []

    first_centroid = points[0]
    second_centroid = max_distance_point(first_centroid, points)
    clusters = [Cluster(centroid=first_centroid), Cluster(centroid=second_centroid)]

    assign_points_to_nearest_clusters(points, clusters)

    candidate, candidate_distance = candidate_from_clusters(clusters)
    average_distance = average_distance_between_clusters(clusters)
    while 2 * candidate_distance > average_distance:
        states.append(State(clusters))
        clusters.append(Cluster(centroid=candidate))
        assign_points_to_nearest_clusters(points, clusters)
        candidate, candidate_distance = candidate_from_clusters(clusters)
        average_distance = average_distance_between_clusters(clusters)

    return states


def max_distance_point(first_centroid, points):
    max_distance = 0
    max_point = None
    for point in points:
        distance = point.distance(first_centroid)
        if distance > max_distance:
            max_distance = distance
            max_point = point
    return max_point


def candidate_from_clusters(clusters):
    max_distance = 0
    max_point = None
    for cluster in clusters:
        point, distance = candidate_from_cluster(cluster)
        if distance > max_distance:
            max_distance = distance
            max_point = point

    return max_point, max_distance


def candidate_from_cluster(cluster):
    max_distance = 0
    max_point = None
    for point in cluster.points:
        distance = point.distance(cluster.centroid)
        if distance > max_distance:
            max_distance = distance
            max_point = point

    return max_point, max_distance


def average_distance_between_clusters(clusters):
    sum = 0
    count = 0
    for i in range(len(clusters)):
        for j in range(i + 1, len(clusters)):
            sum += clusters[i].centroid.distance(clusters[j].centroid)
            count += 1
    return sum / count
