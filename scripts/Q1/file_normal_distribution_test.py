from datetime import datetime
import pandas as pd
from shapiro_test import display_result, normal_distribution_test

DEFAULT_FILE_NAME = "results/file_statistics.csv"
OUTPUT_FILE_PREFIX = "results/file_normal_distribution_test"

def file_normal_distribution_test():
    keys = ["FHIR_JSON", "OpenEHR_FLAT", "OpenEHR_JSON"]
    file_metrics = [
        "size_bytes", "unique_keys", "avg_path_len"
        ]
    
    test_results = []
    for key in keys:
        for metric in file_metrics:
            result = normal_distribution_test("standard_format", key, metric, DEFAULT_FILE_NAME)
            test_results.append(result)
            display_result(result)
    
    df = pd.DataFrame(test_results)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = f"{OUTPUT_FILE_PREFIX}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"Zapisano wyniki testu normalności do pliku {filename}")

if __name__ == "__main__":
    file_normal_distribution_test()