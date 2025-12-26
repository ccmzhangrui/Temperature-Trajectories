import pandas as pd
import numpy as np


def generate_synthetic_sepsis_data(num_patients=50, num_timepoints=12, seed=42):
    np.random.seed(seed)
    rows = []
    for pid in range(1, num_patients + 1):
        base_temp = np.random.normal(37, 0.3)
        temps = base_temp + np.random.normal(0, 0.5, num_timepoints)
        platelet = np.random.randint(100, 300)
        pt_ratio = np.random.normal(1.0, 0.1)
        d_dimer = np.random.normal(1.5, 0.5)
        mortality = np.random.choice([0, 1])
        platelet_slope = np.random.normal(0, 0.05)
        for t in temps:
            rows.append({
                "patient_id": pid,
                "temperature": t,
                "platelet": platelet,
                "pt_ratio": pt_ratio,
                "d_dimer": d_dimer,
                "mortality": mortality,
                "platelet_slope": platelet_slope
            })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = generate_synthetic_sepsis_data()
    df.to_csv("data/sepsis_data.csv", index=False)
    print("Synthetic dataset generated at data/sepsis_data.csv")
