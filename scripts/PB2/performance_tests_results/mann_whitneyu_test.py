from datetime import datetime
import pandas as pd
from scipy.stats import mannwhitneyu

P_VALUE_TRESHOLD = 0.05
USERS_NUMBER = 100
OUTPUT_FILE_PREFIX = "mannwhitneyu_test"

def mannwhitneyu_test(metric, file_name1, mode, file_name2, simple_data_requests):
    df_1 = pd.read_csv(file_name1)
    if simple_data_requests:
        metric_1 = df_1[~df_1["Name"].str.contains('full')][metric]
    else:
        metric_1 = df_1[df_1["Name"].str.contains('full')][metric]

    df_2 = pd.read_csv(file_name2)
    if simple_data_requests:
        metric_2 = df_2[~df_2["Name"].str.contains('full')][metric]
    else:
        metric_2 = df_2[df_2["Name"].str.contains('full')][metric]

    stat, p = mannwhitneyu(metric_1.tolist(), metric_2.tolist(), alternative=mode)

    return {
        "simple_data_requests": simple_data_requests,
        "metric": metric,
        "statistic": round(stat, 5),
        "mode": mode,
        "p_value": round(p, 5),
        # Tries to prove that the difference is statistically significant
        "is_significantly_different": p < P_VALUE_TRESHOLD
    }

def display_result(result):
    data_type = "proste" if result['simple_data_requests'] else "złożone"
    print(f"===== {result['metric']} - dla zapytań o dane {data_type}  ====")
    print("statystyka:", result["statistic"])
    print("p-wartość:", result["p_value"])
    if result["is_significantly_different"]:
        print(f"Różnica {result['mode']} jednostronna jest statystycznie istotna (p < {P_VALUE_TRESHOLD})")
    if not result["is_significantly_different"]:
        print(f"Różnica {result['mode']} nie jest statystycznie istotna (p ≥ {P_VALUE_TRESHOLD})")
    print()

def run_mann_whitneyu_test():
    normal_distribution_metrics = [
            ["Average Response Time", "FHIR", "less", "OpenEHR", True],
            ["Average Response Time", "FHIR", "greater", "OpenEHR", True],
            ["Average Response Time", "FHIR", "two-sided", "OpenEHR", True],

            ["Requests/s", "FHIR", "less", "OpenEHR", True],
            ["Requests/s", "FHIR", "greater", "OpenEHR", True],
            ["Requests/s", "FHIR", "two-sided", "OpenEHR", True],
        ]
    
    test_results = []
    for metric, standard_1, mode, standard_2, simple_data_requests in normal_distribution_metrics:
        file_1 = f"{standard_1}_{USERS_NUMBER}/stats/performance_tests_{standard_1.lower()}_stats.csv"
        file_2 = f"{standard_2}_{USERS_NUMBER}/stats/performance_tests_{standard_2.lower()}_stats.csv"
        result = mannwhitneyu_test(metric, file_1, mode, file_2, simple_data_requests)
        test_results.append(result)
        display_result(result)
            
    df = pd.DataFrame(test_results)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = f"{OUTPUT_FILE_PREFIX}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"Zapisano wyniki testu istotności do pliku {filename}")

if __name__ == "__main__":
    run_mann_whitneyu_test()