from datetime import datetime
import pandas as pd
from welch_test import welch_test, display_result

DEFAULT_FILE_NAME = "results/graphs_statistics.csv"
OUTPUT_FILE_PREFIX = "results/graphs_welch_test"

if __name__ == "__main__":
    # TODO: Max depth
    graph_normal_distribution_metrics = [
            # No difference
            ["num_nodes", "FHIR", "less", "OpenEHR"],
            ["num_nodes", "FHIR", "greater", "OpenEHR"],
            ["num_nodes", "FHIR", "two-sided", "OpenEHR"],

            # No difference
            ["num_edges", "FHIR", "less", "OpenEHR"],
            ["num_edges", "FHIR", "greater", "OpenEHR"],
            ["num_edges", "FHIR", "two-sided", "OpenEHR"],

            # No difference
            ["density", "FHIR", "less", "OpenEHR"],
            ["density", "FHIR", "greater", "OpenEHR"],
            ["density", "FHIR", "two-sided", "OpenEHR"],

            # No difference
            ["max_degree", "FHIR", "less", "OpenEHR"],
            ["max_degree", "FHIR", "greater", "OpenEHR"],
            ["max_degree", "FHIR", "two-sided", "OpenEHR"],

            ["average_degree", "FHIR", "greater", "OpenEHR"],
            ["average_degree", "FHIR", "two-sided", "OpenEHR"],

            ["diameter", "FHIR", "less", "OpenEHR"],

            ["avg_path_length", "FHIR", "less", "OpenEHR"],
            ["avg_path_length", "FHIR", "two-sided", "OpenEHR"],

            ["assortativity", "FHIR", "greater", "OpenEHR"],
            ["assortativity", "FHIR", "two-sided", "OpenEHR"],

            ["cycles", "FHIR", "greater", "OpenEHR"],
            ["cycles", "FHIR", "two-sided", "OpenEHR"],

            ["avg_path_from_root", "FHIR", "less", "OpenEHR"],
            ["avg_path_from_root", "FHIR", "two-sided", "OpenEHR"],
        ]
    
    test_results = []
    for metric, key_value1, mode, key_value2 in graph_normal_distribution_metrics:
        result = welch_test("standard", key_value1, key_value2, metric, mode, DEFAULT_FILE_NAME)
        test_results.append(result)
        display_result(result)
            
    df = pd.DataFrame(test_results)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = f"{OUTPUT_FILE_PREFIX}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"Zapisano wyniki testu istotności do pliku {filename}")