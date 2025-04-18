from datetime import datetime
from scipy.stats import shapiro
import pandas as pd

DEFAULT_FILE_NAME = "results/graphs_statistics_2025_04_18_13_16_02.csv"

P_VALUE_TRESHOLD = 0.05
OUTPUT_FILE_PREFIX = "results/normal_distribution_test"

def normal_distribution_test(standard, metric, file_name = DEFAULT_FILE_NAME):
    df = pd.read_csv(file_name)
    df_standard = df[df["standard"] == standard]
    df_standard_metric = df_standard[metric]

    print(df_standard_metric.tolist())

    # Test Shapiro-Wilka
    stat, p = shapiro(df_standard_metric.tolist())

    return {
        "standard": standard,
        "metric": metric,
        "w_statistic": stat,
        "p_value": p,
        "is_normal": p > P_VALUE_TRESHOLD
    }

def display_result(result):
    print(f"===== {result['standard']} - {result['metric']} ====")
    print("W-statystyka:", result["w_statistic"])
    print("p-wartość:", result["p_value"])
    if result["is_normal"]:
        print("Nie ma podstawy by odrzucić hipotezę, że dane mają postać rozkładu normalnego")
    if not result["is_normal"]:
        print("Dane nie mają rozkładu normalnego")
    print()

if __name__ == "__main__":
    standards = ["FHIR", "OpenEHR"]
    graph_metrics = [
        "num_nodes","num_edges","density","max_degree","average_degree","median_degree","diameter",
        "avg_path_length","assortativity","cycles","max_depth","avg_path_from_root"
        ]
    
    test_results = []
    for standard in standards:
        for metric in graph_metrics:
            result = normal_distribution_test(standard, metric)
            test_results.append(result)
            display_result(result)
            
    
    df = pd.DataFrame(test_results)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = f"{OUTPUT_FILE_PREFIX}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"Zapisano wyniki testu normalności do pliku {filename}")
