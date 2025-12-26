import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def plot_temperature_trajectories(processed_data, labels, method="GMM", save_path=None):
    processed_data = processed_data.copy()
    processed_data["phenotype"] = labels
    plt.figure(figsize=(10, 6))
    for phenotype in np.unique(labels):
        subset = processed_data[processed_data["phenotype"] == phenotype]
        for pid in subset["patient_id"].unique():
            trajectory = subset[subset["patient_id"] == pid]["temp_interpolated"].values
            plt.plot(range(len(trajectory)), trajectory, alpha=0.3, label=f"Phenotype {phenotype}" if pid == subset["patient_id"].unique()[0] else "")
    plt.xlabel("Time Index")
    plt.ylabel("Normalized Temperature")
    plt.title(f"Temperature Trajectories ({method} Clustering)")
    plt.legend()
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.close()


def plot_coagulation_analysis(analysis_df, method="GMM", save_path=None):
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    sns.barplot(data=analysis_df.reset_index().melt(id_vars="index"), x="index", y="value", hue="variable", ax=ax)
    ax.set_xlabel("Phenotype")
    ax.set_ylabel("Value")
    ax.set_title(f"Coagulation Parameters ({method} Clustering)")
    plt.xticks(rotation=45)
    plt.legend(title="Parameter", bbox_to_anchor=(1.05, 1), loc="upper left")
    if save_path:
        plt.tight_layout()
        plt.savefig(save_path, dpi=300)

    plt.close()
