import pandas as pd


def preprocess_temperature_data(df: pd.DataFrame) -> pd.DataFrame:
    # Normalize temperature by baseline of first 3 measurements
    df['temp_normalized'] = df.groupby('patient_id')['temperature'].transform(
        lambda x: x / x.head(3).mean()
    )
    # Interpolate missing values using cubic spline
    df['temp_interpolated'] = df.groupby('patient_id')['temp_normalized'].transform(
        lambda x: x.interpolate(method='cubic')
    )
    return df
