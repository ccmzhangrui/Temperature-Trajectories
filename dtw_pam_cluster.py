import numpy as np
from dtw import distance_matrix_fast as distance_matrix  # 修复导入
from pyclustering.cluster.kmedoids import kmedoids
from sklearn.metrics import silhouette_score
import random


def cluster_temperature_trajectories_pam(trajectories):
    # 计算 DTW 距离矩阵
    dist_matrix = distance_matrix(trajectories)
    dist_matrix_std = (dist_matrix - dist_matrix.mean()) / dist_matrix.std()

    best_score = -1
    best_labels = None
    optimal_clusters = None

    for n_clusters in range(2, 6):
        initial_medoids = random.sample(range(len(dist_matrix_std)), n_clusters)
        pam_instance = kmedoids(dist_matrix_std.tolist(), initial_medoids,  data_type='distance_matrix')
        pam_instance.process()
        clusters = pam_instance.get_clusters()

        labels = np.zeros(len(dist_matrix_std), dtype=int)
        for cid, cluster in enumerate(clusters):
            for idx in cluster:
                labels[idx] = cid

        score = silhouette_score(dist_matrix_std, labels, metric='precomputed')

        if score > best_score:
            best_score, best_labels, optimal_clusters = score, labels, n_clusters

    return best_labels, optimal_clusters, best_score
