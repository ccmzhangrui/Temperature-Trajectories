import numpy as np
from dtw import distance_matrix_fast as distance_matrix  # 修复导入
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score


def cluster_temperature_trajectories_gmm(trajectories):
    # 计算 DTW 距离矩阵
    dist_matrix = distance_matrix(trajectories)
    # 标准化
    dist_matrix_std = (dist_matrix - dist_matrix.mean()) / dist_matrix.std()

    bic_scores, silhouette_scores = [], []
    for n_clusters in range(2, 6):
        gmm = GaussianMixture(n_components=n_clusters, covariance_type='full', random_state=42)
        labels = gmm.fit_predict(dist_matrix_std)
        bic_scores.append(gmm.bic(dist_matrix_std))
        silhouette_scores.append(silhouette_score(dist_matrix_std, labels))

    optimal_clusters = np.argmin(bic_scores) + 2
    gmm_final = GaussianMixture(n_components=optimal_clusters, covariance_type='full',  random_state=42)
    final_labels = gmm_final.fit_predict(dist_matrix_std)
    return final_labels, optimal_clusters, silhouette_scores[optimal_clusters - 2]
