from datetime import datetime
import pandas as pd
from welch_test import welch_test, display_result

DEFAULT_FILE_NAME = "results/file_statistics.csv"
OUTPUT_FILE_PREFIX = "results/file_welch_test"

if __name__ == "__main__":
    # TODO: Not avg_path_len - OpenEHR_JSON
    # TODO: Verify is one side
    file_normal_distribution_metrics = [
            ["size_bytes", True, "FHIR_JSON", "OpenEHR_FLAT"], 
            ["size_bytes", True, "FHIR_JSON", "OpenEHR_JSON"], 
            ["size_bytes", False, "FHIR_JSON", "OpenEHR_FLAT"], 
            ["size_bytes", False, "FHIR_JSON", "OpenEHR_JSON"],
            ["unique_keys", True, "FHIR_JSON", "OpenEHR_FLAT"], 
            ["unique_keys", True, "FHIR_JSON", "OpenEHR_JSON"], 
            ["unique_keys", False, "FHIR_JSON", "OpenEHR_FLAT"], 
            ["unique_keys", False, "FHIR_JSON", "OpenEHR_JSON"],
            ["avg_path_len", True, "FHIR_JSON", "OpenEHR_FLAT"], 
            ["avg_path_len", False, "FHIR_JSON", "OpenEHR_FLAT"], 
        ]
    
    test_results = []
    for metric, is_one_side, key_value1, key_value2 in file_normal_distribution_metrics:
        result = welch_test("standard_format", key_value1, key_value2, metric, is_one_side, DEFAULT_FILE_NAME)
        test_results.append(result)
        display_result(result)
            
    df = pd.DataFrame(test_results)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = f"{OUTPUT_FILE_PREFIX}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"Zapisano wyniki testu istotności do pliku {filename}")