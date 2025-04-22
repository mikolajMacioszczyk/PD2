from datetime import datetime
import pandas as pd
from shapiro_test import display_result, normal_distribution_test

DEFAULT_FILE_NAME = "results/graphs_statistics.csv"
OUTPUT_FILE_PREFIX = "results/graphs_normal_distribution_test"

def graphs_normal_distribution_test():
    standards = ["FHIR", "OpenEHR"]
    graph_metrics = [
        "num_nodes","num_edges","density","max_degree","average_degree","diameter",
        "avg_path_length","assortativity","cycles","max_depth","avg_path_from_root"
        ]
    
    test_results = []
    for standard in standards:
        for metric in graph_metrics:
            result = normal_distribution_test("standard", standard, metric, DEFAULT_FILE_NAME)
            test_results.append(result)
            display_result(result)
            
    
    df = pd.DataFrame(test_results)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = f"{OUTPUT_FILE_PREFIX}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"Zapisano wyniki testu normalności do pliku {filename}")

if __name__ == "__main__":
    graphs_normal_distribution_test()