from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score

# from dtaidistance import distance
# import dtaidistance.dtw
# distance = dtaidistance.dtw.distance
# dist_matrix = dtaidistance.dtw.distance_matrix


from dtaidistance import dtw


import numpy as np


def cluster_temperature_trajectories_gmm(trajectories):
    """
    Perform GMM clustering on DTW distance matrix of temperature trajectories.
    Returns: final labels, optimal number of clusters, silhouette score of the optimal clustering.
    """

    # Ensure trajectories are list of np.array
    trajectories = [
        np.asarray(t, dtype=float).ravel() for t in trajectories
    ]

    # Calculate DTW distance matrix
    # dist_matrix = distance.matrix(trajectories)
    dist_matrix = dtw.distance_matrix(trajectories)

    # Standardize distance matrix
    dist_matrix_std = (dist_matrix - dist_matrix.mean()) / dist_matrix.std()

    bic_scores = []
    silhouette_scores = []
    optimal_clusters = None
    best_labels = None

    # Try different cluster numbers (e.g., 2~6)
    for n_components in range(2, 7):
        gmm = GaussianMixture(
            n_components=n_components,
            covariance_type="full",
            random_state=42
        )
        labels = gmm.fit_predict(dist_matrix_std)  # Fixed: ft_predict -> fit_predict
        bic_scores.append(gmm.bic(dist_matrix_std))
        silhouette_scores.append(silhouette_score(dist_matrix_std, labels))

        if optimal_clusters is None or bic_scores[-1] < min(bic_scores[:-1] if bic_scores else [float('inf')]):
            optimal_clusters = n_components
            best_labels = labels

    return best_labels, optimal_clusters, silhouette_scores[optimal_clusters - 2]
