import numpy as np
from dtw import distance_matrix
from pyclustering.cluster.kmedoids import kmedoids
from sklearn.metrics import silhouette_score


def cluster_temperature_trajectories_pam(trajectories):
    dist_matrix = distance_matrix(trajectories)
    best_score, best_labels, optimal_clusters = -1, None, None
    for n_clusters in range(2, 6):
        initial_medoids = list(range(n_clusters))
        pam = kmedoids(dist_matrix.tolist(), initial_medoids, data_type='distance_matrix')
        pam.process()
        labels = np.zeros(len(dist_matrix), dtype=int)
        for cluster_id, cluster in enumerate(pam.get_clusters()):
            labels[cluster] = cluster_id
        score = silhouette_score(dist_matrix, labels, metric='precomputed')
        if score > best_score:
            best_score, best_labels, optimal_clusters = score, labels, n_clusters
    return best_labels, optimal_clusters, best_score
