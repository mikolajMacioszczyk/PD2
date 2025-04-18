from datetime import datetime
import pandas as pd
from scipy.stats import ttest_ind

DEFAULT_FILE_NAME = "results/graphs_statistics_2025_04_18_13_42_03.csv"
P_VALUE_TRESHOLD = 0.05
OUTPUT_FILE_PREFIX = "results/welch_test"

def welch_test(metric, is_one_side, file_name = DEFAULT_FILE_NAME):
    df = pd.read_csv(file_name)
    metric_fhir = df[df["standard"] == "FHIR"][metric]
    metric_openEHR = df[df["standard"] == "OpenEHR"][metric]

    # Test t-Studenta z korektą Welcha (nierówne wariancje)
    stat, p = ttest_ind(metric_fhir.tolist(), metric_openEHR.tolist(), equal_var=False)

    if is_one_side:
        if stat < 0: 
            p_one_side = p / 2
        else:
            p_one_side = 1 - p / 2

        return {
            "metric": metric,
            "statistic": stat,
            "is_one_side": is_one_side,
            "p_value": p_one_side,
            # Tries to prove that the difference is statistically significant
            "is_significantly_different": p_one_side < P_VALUE_TRESHOLD
        } 
    else:
        return {
            "metric": metric,
            "statistic": stat,
            "is_one_side": is_one_side,
            "p_value": p,
            # Tries to prove that the difference is statistically significant
            "is_significantly_different": p < P_VALUE_TRESHOLD
        }

def display_result(result):
    print(f"===== {result['metric']} ====")
    print("statystyka:", result["statistic"])
    print("p-wartość:", result["p_value"])
    if result["is_significantly_different"]:
        if result["is_one_side"]:
            print(f"Różnica jednostronna jest statystycznie istotna (p < {P_VALUE_TRESHOLD})")
        else:
            print(f"Różnica jest statystycznie istotna (p < {P_VALUE_TRESHOLD})")
    if not result["is_significantly_different"]:
        if result["is_one_side"]:
            print(f"Różnica jednostronna nie jest statystycznie istotna (p ≥ {P_VALUE_TRESHOLD})")
        else:
            print(f"Różnica nie jest statystycznie istotna (p ≥ {P_VALUE_TRESHOLD})")
    print()

if __name__ == "__main__":
    standards = ["FHIR", "OpenEHR"]
    # TODO: Select metrics
    graph_normal_distribution_metrics = [
            ["diameter", True], 
            ["diameter", False], 
            ["avg_path_length", True], 
            ["avg_path_length", False], 
            ["avg_path_from_root", True],
            ["avg_path_from_root", False]
        ]
    
    test_results = []
    for metric, is_one_side in graph_normal_distribution_metrics:
        result = welch_test(metric, is_one_side)
        test_results.append(result)
        display_result(result)
            
    df = pd.DataFrame(test_results)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = f"{OUTPUT_FILE_PREFIX}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"Zapisano wyniki testu istotności do pliku {filename}")
            