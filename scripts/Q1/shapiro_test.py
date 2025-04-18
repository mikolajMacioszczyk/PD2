from scipy.stats import shapiro
import pandas as pd

P_VALUE_TRESHOLD = 0.05

def normal_distribution_test(key_column, key_value, metric, file_name):
    df = pd.read_csv(file_name)
    df_standard = df[df[key_column] == key_value]
    df_standard_metric = df_standard[metric]

    print(df_standard_metric.tolist())

    # Test Shapiro-Wilka
    stat, p = shapiro(df_standard_metric.tolist())

    return {
        "key_column": key_column,
        "key_value": key_value,
        "metric": metric,
        "w_statistic": stat,
        "p_value": p,
        # Tries to prove that is not normal
        "is_normal": p > P_VALUE_TRESHOLD
    }

def display_result(result):
    print(f"===== {result['key_value']} - {result['metric']} ====")
    print("W-statystyka:", result["w_statistic"])
    print("p-wartość:", result["p_value"])
    if result["is_normal"]:
        print(f"Nie ma podstawy by odrzucić hipotezę, że dane mają postać rozkładu normalnego (p > {P_VALUE_TRESHOLD})")
    if not result["is_normal"]:
        print(f"Dane nie mają rozkładu normalnego (p <= {P_VALUE_TRESHOLD})")
    print()
