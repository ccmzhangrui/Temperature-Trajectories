import os
import pandas as pd
import numpy as np
from datetime import datetime
from preprocess import preprocess_temperature_data
from dtw_gmm_cluster import cluster_temperature_trajectories_gmm
from dtw_pam_cluster import cluster_temperature_trajectories_pam
from analysis import analyze_coagulation_by_phenotype
from plot_utils import plot_temperature_trajectories, plot_coagulation_analysis

if __name__ == "__main__":
    os.makedirs("docs", exist_ok=True)
    os.makedirs("history", exist_ok=True)
    today = datetime.utcnow().strftime("%Y-%m-%d")
    data = pd.read_csv('data/sepsis_data.csv')
    processed_data = preprocess_temperature_data(data)
    trajectories = processed_data.groupby('patient_id')['temp_interpolated'].apply(lambda x: np.array(x)).values

    # --- GMM ---
    gmm_labels, gmm_n_clusters, gmm_silhouette = cluster_temperature_trajectories_gmm(trajectories)
    gmm_analysis = analyze_coagulation_by_phenotype(data, gmm_labels)
    plot_temperature_trajectories(processed_data, gmm_labels, "GMM", "docs/gmm_trajectories.png")
    plot_coagulation_analysis(gmm_analysis, "GMM", "docs/gmm_coagulation.png")
    gmm_analysis.to_csv("results_gmm.csv")
    os.system(f"cp docs/gmm_trajectories.png history/{today}_gmm_trajectories.png")
    os.system(f"cp docs/gmm_coagulation.png history/{today}_gmm_coagulation.png")
    os.system(f"cp results_gmm.csv history/{today}_results_gmm.csv")

    # --- PAM ---
    pam_labels, pam_n_clusters, pam_silhouette = cluster_temperature_trajectories_pam(trajectories)
    pam_analysis = analyze_coagulation_by_phenotype(data, pam_labels)
    plot_temperature_trajectories(processed_data, pam_labels, "PAM", "docs/pam_trajectories.png")
    plot_coagulation_analysis(pam_analysis, "PAM", "docs/pam_coagulation.png")
    pam_analysis.to_csv("results_pam.csv")
    os.system(f"cp docs/pam_trajectories.png history/{today}_pam_trajectories.png")
    os.system(f"cp docs/pam_coagulation.png history/{today}_pam_coagulation.png")
    os.system(f"cp results_pam.csv history/{today}_results_pam.csv")
