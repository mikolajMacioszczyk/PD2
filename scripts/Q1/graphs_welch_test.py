from datetime import datetime
import pandas as pd
from welch_test import welch_test, display_result

DEFAULT_FILE_NAME = "results/graphs_statistics_2025_04_18_13_42_03.csv"
OUTPUT_FILE_PREFIX = "results/graphs_welch_test"

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
        result = welch_test("standard", "FHIR", "OpenEHR", metric, is_one_side, DEFAULT_FILE_NAME)
        test_results.append(result)
        display_result(result)
            
    df = pd.DataFrame(test_results)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = f"{OUTPUT_FILE_PREFIX}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"Zapisano wyniki testu istotności do pliku {filename}")