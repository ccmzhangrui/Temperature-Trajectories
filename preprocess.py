import pandas as pd


def preprocess_temperature_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize and interpolate temperature trajectories per patient.

    Steps:
      1) Normalize each patient's temperature by the mean of the first 3 measurements.
      2) Interpolate missing values (cubic if possible; fallback to linear).

    Required columns:
      - patient_id
      - temperature

    Optional columns:
      - time (used to order rows per patient)

    Produces:
      - temp_normalized
      - temp_interpolated
    """
    df = df.copy()

    required = {"patient_id", "temperature"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    if "time" in df.columns:
        df = df.sort_values(["patient_id", "time"])
    else:
        df = df.sort_values(["patient_id"])

    def _normalize(s: pd.Series) -> pd.Series:
        baseline = s.head(3).mean()
        if pd.isna(baseline) or baseline == 0:
            baseline = s.mean()
        if pd.isna(baseline) or baseline == 0:
            baseline = 1.0
        return s / baseline

    df["temp_normalized"] = df.groupby("patient_id")["temperature"].transform(_normalize)

    def _interp(s: pd.Series) -> pd.Series:
        try:
            if s.notna().sum() >= 4:
                return s.interpolate(method="cubic", limit_direction="both")
            return s.interpolate(method="linear", limit_direction="both")
        except Exception:
            return s.interpolate(method="linear", limit_direction="both")

    df["temp_interpolated"] = df.groupby("patient_id")["temp_normalized"].transform(_interp)
    return df
