import numpy as np
# from dtaidistance import distance
from dtaidistance import dtw
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score


def cluster_temperature_trajectories_gmm(trajectories, k_min=2, k_max=5, random_state=42):
    """
    Cluster trajectories using:
      - DTW distance matrix
      - Row-wise standardized distance vectors as features
      - Gaussian Mixture Model
      - Choose k by lowest BIC

    Returns:
      (final_labels, optimal_clusters, silhouette_at_optimal_or_nan)
    """
    trajectories = [np.asarray(t, dtype=float).ravel() for t in trajectories]
    n = len(trajectories)
    if n < 2:
        raise ValueError("Need at least 2 trajectories for clustering.")

    # dist_matrix = np.asarray(distance.matrix(trajectories), dtype=float)
    dist_matrix = np.asarray(dtw.distance_matrix(trajectories), dtype=float)
    mean = dist_matrix.mean()
    std = dist_matrix.std()
    X = (dist_matrix - mean) / (std if std != 0 else 1.0)

    bic_scores = []
    sil_scores = []
    labels_list = []

    for n_clusters in range(k_min, min(k_max, n - 1) + 1):
        gmm = GaussianMixture(n_components=n_clusters, covariance_type="full", random_state=random_state)
        labels = gmm.fit_predict(X)
        labels_list.append(labels)

        bic_scores.append(gmm.bic(X))

        sil = np.nan
        n_labels = len(set(labels.tolist()))
        if 1 < n_labels < n:
            sil = silhouette_score(X, labels)
        sil_scores.append(sil)

    if not bic_scores:
        raise ValueError("No feasible k in the given range for the number of trajectories.")

    best_idx = int(np.argmin(bic_scores))
    optimal_clusters = k_min + best_idx
    final_labels = labels_list[best_idx]
    final_sil = sil_scores[best_idx]

    return final_labels, optimal_clusters, final_sil
