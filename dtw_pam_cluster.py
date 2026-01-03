import numpy as np
import random
# from dtaidistance import distance
from dtaidistance import dtw
from pyclustering.cluster.kmedoids import kmedoids
from sklearn.metrics import silhouette_score


def cluster_temperature_trajectories_pam(trajectories, k_min=2, k_max=5, random_seed=42):
    """
    Cluster trajectories with PAM (k-medoids) using a DTW distance matrix.
    Choose k by highest silhouette score (precomputed distance).

    Returns:
      (best_labels, optimal_clusters, best_score_or_nan)
    """
    rng = random.Random(random_seed)

    trajectories = [np.asarray(t, dtype=float).ravel() for t in trajectories]
    n = len(trajectories)
    if n < 2:
        raise ValueError("Need at least 2 trajectories for clustering.")

    # dist_matrix = np.asarray(distance.matrix(trajectories), dtype=float)
    dist_matrix = np.asarray(dtw.distance_matrix(trajectories), dtype=float)

    best_score = -np.inf
    best_labels = None
    optimal_clusters = None

    for n_clusters in range(k_min, min(k_max, n - 1) + 1):
        initial_medoids = rng.sample(range(n), n_clusters)
        pam = kmedoids(dist_matrix, initial_medoids, data_type="distance_matrix")
        pam.process()

        clusters = pam.get_clusters()
        labels = np.full(n, -1, dtype=int)
        for cid, idxs in enumerate(clusters):
            labels[idxs] = cid

        score = np.nan
        n_labels = len(set(labels.tolist()))
        if -1 not in labels and 1 < n_labels < n:
            score = silhouette_score(dist_matrix, labels, metric="precomputed")

        # Prefer finite silhouette; otherwise keep first feasible solution.
        if np.isfinite(score) and (not np.isfinite(best_score) or score > best_score):
            best_score = score
            best_labels = labels
            optimal_clusters = n_clusters
        elif best_labels is None:
            best_score = score
            best_labels = labels
            optimal_clusters = n_clusters

    return best_labels, optimal_clusters, best_score
