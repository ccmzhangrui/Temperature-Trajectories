import os
import numpy as np
import pandas as pd


def generate_synthetic_sepsis_data(num_patients=50, num_timepoints=12, seed=42) -> pd.DataFrame:
    """
    Generate a synthetic long-form dataset with repeated measurements per patient.
    """
    np.random.seed(seed)
    rows = []

    for pid in range(1, num_patients + 1):
        base_temp = np.random.normal(37, 0.3)
        temps = base_temp + np.random.normal(0, 0.5, num_timepoints)

        platelet = int(np.random.randint(100, 300))
        pt_ratio = float(np.random.normal(1.0, 0.1))
        d_dimer = float(np.random.normal(1.5, 0.5))
        mortality = int(np.random.choice([0, 1]))
        platelet_slope = float(np.random.normal(0, 0.05))

        for ti, t in enumerate(temps):
            rows.append(
                {
                    "patient_id": pid,
                    "time": ti,
                    "temperature": float(t),
                    "platelet": platelet,
                    "pt_ratio": pt_ratio,
                    "d_dimer": d_dimer,
                    "mortality": mortality,
                    "platelet_slope": platelet_slope,
                }
            )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df = generate_synthetic_sepsis_data()
    df.to_csv("data/sepsis_data.csv", index=False)
    print("Synthetic dataset generated at data/sepsis_data.csv")
