from datetime import datetime
import pandas as pd
from scipy.stats import shapiro

USERS_NUMBER = 100
OUTPUT_FILE_PREFIX = "normal_distribution_test"
P_VALUE_TRESHOLD = 0.05

def normal_distribution_test(standard, metric, file_name, simple_data_requests):
    df = pd.read_csv(file_name)
    if simple_data_requests:
        df_request_type = df[~df["Name"].str.contains('full')]
    else:
        df_request_type = df[df["Name"].str.contains('full')]
    df_request_type_metric = df_request_type[metric]

    # Test Shapiro-Wilka
    stat, p = shapiro(df_request_type_metric.tolist())

    return {
        "standard": standard,
        "simple_data_requests": simple_data_requests,
        "metric": metric,
        "w_statistic": stat,
        "p_value": p,
        # Tries to prove that is not normal
        "is_normal": p > P_VALUE_TRESHOLD
    }

def display_result(result):
    data_type = "proste" if result['simple_data_requests'] else "złożone"
    print(f"===== {result['standard']} - {result['metric']} - dla zapytań o dane {data_type} ====")
    print("W-statystyka:", result["w_statistic"])
    print("p-wartość:", result["p_value"])
    if result["is_normal"]:
        print(f"Nie ma podstawy by odrzucić hipotezę, że dane mają postać rozkładu normalnego (p > {P_VALUE_TRESHOLD})")
    if not result["is_normal"]:
        print(f"Dane nie mają rozkładu normalnego (p <= {P_VALUE_TRESHOLD})")
    print()

def run_normal_distribution_test():
    standards = ["FHIR", "OpenEHR"]
    metrics = [
        "Median Response Time","Average Response Time","Requests/s"
        ]
    
    test_results = []
    for standard in standards:
        file_path = f"{standard}_{USERS_NUMBER}/stats/performance_tests_{standard.lower()}_stats.csv"

        for metric in metrics:
            result = normal_distribution_test(standard, metric, file_path, simple_data_requests=True)
            test_results.append(result)
            display_result(result)

            result = normal_distribution_test(standard, metric, file_path, simple_data_requests=False)
            test_results.append(result)
            display_result(result)
            
    
    df = pd.DataFrame(test_results)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = f"{OUTPUT_FILE_PREFIX}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"Zapisano wyniki testu normalności do pliku {filename}")

if __name__ == "__main__":
    run_normal_distribution_test()