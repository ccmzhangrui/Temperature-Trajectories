import os
import shutil
from datetime import datetime

import numpy as np
import pandas as pd

from preprocess import preprocess_temperature_data
from dtw_gmm_cluster import cluster_temperature_trajectories_gmm
from dtw_pam_cluster import cluster_temperature_trajectories_pam
from analysis import analyze_coagulation_by_phenotype
from plot_utils import plot_temperature_trajectories, plot_coagulation_analysis


def safe_copy(src: str, dst: str) -> None:
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)


def build_trajectories(processed_data: pd.DataFrame):
    """
    Build per-patient trajectories from long-form processed_data.

    Returns:
      patient_ids: list
      trajectories: list[np.ndarray]
    """
    if "patient_id" not in processed_data.columns or "temp_interpolated" not in processed_data.columns:
        raise ValueError("processed_data must include 'patient_id' and 'temp_interpolated' columns.")

    grouped = processed_data.groupby("patient_id", sort=False)["temp_interpolated"]

    patient_ids = []
    trajectories = []
    for pid, series in grouped:
        patient_ids.append(pid)
        trajectories.append(np.asarray(series, dtype=float).ravel())

    return patient_ids, trajectories


if __name__ == "__main__":
    os.makedirs("docs", exist_ok=True)
    os.makedirs("history", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    today = datetime.utcnow().strftime("%Y-%m-%d")

    data = pd.read_csv("data/sepsis_data.csv")
    processed_data = preprocess_temperature_data(data)

    patient_ids, trajectories = build_trajectories(processed_data)

    # --- GMM ---
    gmm_labels, gmm_n_clusters, gmm_silhouette = cluster_temperature_trajectories_gmm(trajectories)
    gmm_analysis = analyze_coagulation_by_phenotype(data, patient_ids, gmm_labels)

    plot_temperature_trajectories(
        processed_data, patient_ids, gmm_labels, method="GMM", save_path="docs/gmm_trajectories.png"
    )
    plot_coagulation_analysis(gmm_analysis, method="GMM", save_path="docs/gmm_coagulation.png")

    gmm_analysis.to_csv("results_gmm.csv", index=True)
    safe_copy("docs/gmm_trajectories.png", f"history/{today}_gmm_trajectories.png")
    safe_copy("docs/gmm_coagulation.png", f"history/{today}_gmm_coagulation.png")
    safe_copy("results_gmm.csv", f"history/{today}_results_gmm.csv")

    # --- PAM ---
    pam_labels, pam_n_clusters, pam_silhouette = cluster_temperature_trajectories_pam(trajectories)
    pam_analysis = analyze_coagulation_by_phenotype(data, patient_ids, pam_labels)

    plot_temperature_trajectories(
        processed_data, patient_ids, pam_labels, method="PAM", save_path="docs/pam_trajectories.png"
    )
    plot_coagulation_analysis(pam_analysis, method="PAM", save_path="docs/pam_coagulation.png")

    pam_analysis.to_csv("results_pam.csv", index=True)
    safe_copy("docs/pam_trajectories.png", f"history/{today}_pam_trajectories.png")
    safe_copy("docs/pam_coagulation.png", f"history/{today}_pam_coagulation.png")
    safe_copy("results_pam.csv", f"history/{today}_results_pam.csv")

    print(f"[DONE] GMM: k={gmm_n_clusters}, silhouette={gmm_silhouette} -> results_gmm.csv")
    print(f"[DONE] PAM: k={pam_n_clusters}, silhouette={pam_silhouette} -> results_pam.csv")
