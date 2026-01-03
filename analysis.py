import numpy as np
import pandas as pd


def analyze_coagulation_by_phenotype(data: pd.DataFrame, patient_ids, labels: np.ndarray) -> pd.DataFrame:
    """
    Summarize coagulation parameters by phenotype (cluster label).

    IMPORTANT:
      - labels are per PATIENT (same order as patient_ids)
      - data is long-form (multiple rows per patient)
      - We map labels back to rows using patient_id.

    Expected columns (if present they will be summarized):
      platelet, platelet_slope, pt_ratio, d_dimer, mortality

    Returns a DataFrame indexed by phenotype.
    """
    df = data.copy()
    if "patient_id" not in df.columns:
        raise ValueError("data must contain 'patient_id' column.")

    label_map = dict(zip(patient_ids, labels))
    df["phenotype"] = df["patient_id"].map(label_map)

    results = {}
    phenotypes = [p for p in pd.Series(labels).dropna().unique().tolist()]

    for phenotype in phenotypes:
        subset = df[df["phenotype"] == phenotype]
        results[phenotype] = {
            "n_patients": subset["patient_id"].nunique(),
            "platelet_count": subset["platelet"].mean() if "platelet" in subset.columns else np.nan,
            "platelet_slope": subset["platelet_slope"].mean() if "platelet_slope" in subset.columns else np.nan,
            "pt_ratio": subset["pt_ratio"].mean() if "pt_ratio" in subset.columns else np.nan,
            "d_dimer": subset["d_dimer"].mean() if "d_dimer" in subset.columns else np.nan,
            "mortality_rate": subset["mortality"].mean() if "mortality" in subset.columns else np.nan,
        }

    out = pd.DataFrame.from_dict(results, orient="index")
    out.index.name = "phenotype"
    return out
