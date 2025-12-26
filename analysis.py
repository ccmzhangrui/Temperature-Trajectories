import numpy as np
import pandas as pd


def analyze_coagulation_by_phenotype(data: pd.DataFrame, labels: np.ndarray) -> pd.DataFrame:
    results = {}
    data = data.copy()
    data['phenotype'] = labels
    for phenotype in np.unique(labels):
        subset = data[data['phenotype'] == phenotype]
        results[phenotype] = {
            'platelet_count': subset['platelet'].mean(),
            'platelet_slope': subset['platelet_slope'].mean() if 'platelet_slope' in subset.columns  else np.nan,
            'pt_ratio': subset['pt_ratio'].mean(),
            'd_dimer': subset['d_dimer'].mean(),
            'mortality_rate': subset['mortality'].mean()
        }

    return pd.DataFrame.from_dict(results, orient='index')
