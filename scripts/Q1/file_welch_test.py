from datetime import datetime
import pandas as pd
from welch_test import welch_test, display_result

DEFAULT_FILE_NAME = "results/file_statistics.csv"
OUTPUT_FILE_PREFIX = "results/file_welch_test"

if __name__ == "__main__":
    file_normal_distribution_metrics = [
        ["size_bytes", "FHIR_JSON", "less", "OpenEHR_FLAT"],

        ["size_bytes", "FHIR_JSON", "less", "OpenEHR_JSON"], 

        ["unique_keys", "FHIR_JSON", "less", "OpenEHR_FLAT"], 
        ["unique_keys", "FHIR_JSON", "greater", "OpenEHR_FLAT"], 
        ["unique_keys", "FHIR_JSON", "two-sided", "OpenEHR_FLAT"], 

        ["unique_keys", "FHIR_JSON", "greater", "OpenEHR_JSON"], 

        ["avg_path_len", "FHIR_JSON", "greater", "OpenEHR_FLAT"], 

        ["avg_path_len", "FHIR_JSON", "less", "OpenEHR_JSON"], 
    ]

    
    test_results = []
    for metric, key_value1, mode, key_value2 in file_normal_distribution_metrics:
        result = welch_test("standard_format", key_value1, key_value2, metric, mode, DEFAULT_FILE_NAME)
        test_results.append(result)
        display_result(result)
            
    df = pd.DataFrame(test_results)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = f"{OUTPUT_FILE_PREFIX}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"Zapisano wyniki testu istotności do pliku {filename}")