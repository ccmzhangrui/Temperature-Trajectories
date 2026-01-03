import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def plot_temperature_trajectories(processed_data, patient_ids, labels, method="GMM", save_path=None):
    """
    Plot normalized/interpolated temperature trajectories per patient, colored by phenotype.

    processed_data must contain:
      - patient_id
      - temp_interpolated

    labels are per-patient in the same order as patient_ids.
    """
    df = processed_data.copy()
    if "patient_id" not in df.columns or "temp_interpolated" not in df.columns:
        raise ValueError("processed_data must contain 'patient_id' and 'temp_interpolated'.")

    label_map = dict(zip(patient_ids, labels))
    df["phenotype"] = df["patient_id"].map(label_map)

    plt.figure(figsize=(10, 6))

    phenotypes = sorted([p for p in df["phenotype"].dropna().unique().tolist()])
    for phenotype in phenotypes:
        subset = df[df["phenotype"] == phenotype]
        pids = subset["patient_id"].unique()

        first = True
        for pid in pids:
            trajectory = subset[subset["patient_id"] == pid]["temp_interpolated"].astype(float).to_numpy()
            plt.plot(
                range(len(trajectory)),
                trajectory,
                alpha=0.3,
                linewidth=1.0,
                label=f"Phenotype {phenotype}" if first else "",
            )
            first = False

    plt.xlabel("Time Index")
    plt.ylabel("Normalized Temperature")
    plt.title(f"Temperature Trajectories ({method} Clustering)")
    plt.legend()

    if save_path:
        plt.tight_layout()
        plt.savefig(save_path, dpi=300)
        plt.close()
    else:
        plt.show()


def plot_coagulation_analysis(analysis_df, method="GMM", save_path=None):
    """
    Plot phenotype-level bar charts of coagulation parameters.
    Accepts analysis_df indexed by phenotype (or with 'phenotype' column).
    """
    df = analysis_df.copy()
    if "phenotype" not in df.columns:
        df = df.reset_index()

    plot_df = df.melt(id_vars="phenotype", var_name="variable", value_name="value")

    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    sns.barplot(data=plot_df, x="phenotype", y="value", hue="variable", ax=ax)

    ax.set_xlabel("Phenotype")
    ax.set_ylabel("Value")
    ax.set_title(f"Coagulation Parameters ({method} Clustering)")

    plt.xticks(rotation=45)
    ax.legend(title="Parameter", bbox_to_anchor=(1.05, 1), loc="upper left")

    if save_path:
        plt.tight_layout()
        plt.savefig(save_path, dpi=300)
        plt.close()
    else:
        plt.show()
