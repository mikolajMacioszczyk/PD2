from datetime import datetime
import json

import pandas as pd

DATA_DIRECTORY_PATH = "../../data/"
OUTPUT_FILE_PREFIX = "file_statistics.csv"

import json

def get_json_file_size_no_whitespace(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    compact_json = json.dumps(data, separators=(',', ':'))

    json_bytes = compact_json.encode('utf-8')

    return len(json_bytes)

def get_output_file_path(data_path, medical_document, standard, file_name):
    return f"{data_path}{medical_document}/{standard}/output/{file_name}"

def get_output_name(medical_document, standard):
    return f"{medical_document}_{standard}"

def collect_keys(obj, keys_set):
    if isinstance(obj, dict):
        for key, value in obj.items():
            keys_set.add(key)
            collect_keys(value, keys_set)
    elif isinstance(obj, list):
        for item in obj:
            collect_keys(item, keys_set)

def count_unique_keys(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    unique_keys = set()
    collect_keys(data, unique_keys)

    return len(unique_keys)

if __name__ == "__main__":
    input_data = [
        ["recepta", "FHIR", "bundle-recepta-JSON-61.json"],
        ["recepta", "OpenEHR", "composition-recepta-FLAT-b60548d4-c7ab-4860-8bf9-8271c73f7bbc.json"],
        ["skierowanie", "FHIR", "bundle-skierowanie-JSON-126.json"],
        ["skierowanie", "OpenEHR", "composition-skierowanie-FLAT-2fdbe8e3-01b5-4cdb-a2a3-b2327ed06a18.json"],
        ["wyniki_badan", "FHIR", "bundle-wyniki_badan-JSON-50.json"],
        ["wyniki_badan", "OpenEHR", "composition-wyniki_badan-FLAT-235c3c21-badc-495e-a835-08b2dc61b80a.json"],
    ]

    stats_list = []
    for item in input_data:
        file_path = get_output_file_path(DATA_DIRECTORY_PATH, item[0], item[1], item[2])
        size = get_json_file_size_no_whitespace(file_path)
        unique_keys = count_unique_keys(file_path)
        output_name = get_output_name(item[0], item[1])

        final_stats = {}
        final_stats["output_name"] = output_name
        final_stats["medical_document"] = item[0]
        final_stats["standard"] = item[1]
        final_stats["size_bytes"] = size
        final_stats["unique_keys"] = unique_keys

        stats_list.append(final_stats)

    df = pd.DataFrame(stats_list)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = f"{OUTPUT_FILE_PREFIX}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"Zapisano statystyki do pliku {filename}")
