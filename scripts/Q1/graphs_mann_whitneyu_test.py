from datetime import datetime
import pandas as pd
from mann_whitneyu_test import mannwhitneyu_test, display_result

DEFAULT_FILE_NAME = "results/graphs_metrics.csv"
OUTPUT_FILE_PREFIX = "results/graphs_mannwhitneyu_test"

def graphs_mann_whitneyu_test():
    graph_not_normal_distribution_metrics = [
            ["max_depth", "FHIR", "less", "OpenEHR"],
            ["max_depth", "FHIR", "two-sided", "OpenEHR"],
        ]
    
    test_results = []
    for metric, key_value1, mode, key_value2 in graph_not_normal_distribution_metrics:
        result = mannwhitneyu_test("standard", key_value1, key_value2, metric, mode, DEFAULT_FILE_NAME)
        test_results.append(result)
        display_result(result)
            
    df = pd.DataFrame(test_results)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = f"{OUTPUT_FILE_PREFIX}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"Zapisano wyniki testu istotności do pliku {filename}")

if __name__ == "__main__":
    graphs_mann_whitneyu_test()