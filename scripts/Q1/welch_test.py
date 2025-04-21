import pandas as pd
from scipy.stats import ttest_ind

P_VALUE_TRESHOLD = 0.05

def welch_test(key_column, key_value1, key_value2, metric, mode, file_name):
    df = pd.read_csv(file_name)
    metric_1 = df[df[key_column] == key_value1][metric]
    metric_2 = df[df[key_column] == key_value2][metric]

    # Test t-Studenta z korektą Welcha (nierówne wariancje)
    stat, p = ttest_ind(metric_1.tolist(), metric_2.tolist(), equal_var=False, alternative=mode)

    return {
        "key": f"{key_value1}-{key_value2}",
        "metric": metric,
        "statistic": stat,
        "mode": mode,
        "p_value": p,
        # Tries to prove that the difference is statistically significant
        "is_significantly_different": p < P_VALUE_TRESHOLD
    }

def display_result(result):
    print(f"===== {result['key']} {result['metric']} ====")
    print("statystyka:", result["statistic"])
    print("p-wartość:", result["p_value"])
    if result["is_significantly_different"]:
        print(f"Różnica {result['mode']} jednostronna jest statystycznie istotna (p < {P_VALUE_TRESHOLD})")
    if not result["is_significantly_different"]:
        print(f"Różnica {result['mode']} nie jest statystycznie istotna (p ≥ {P_VALUE_TRESHOLD})")
    print()
            