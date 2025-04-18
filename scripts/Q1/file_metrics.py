from datetime import datetime
import json
import os
import pandas as pd
import json

DATA_DIRECTORY_PATH = "../../data/"
OUTPUT_FILE_PREFIX = "file_statistics.csv"

def get_json_files(directory):
    json_files = [f for f in os.listdir(directory) if f.endswith('.json') and os.path.isfile(os.path.join(directory, f))]
    return json_files

def get_json_file_size_no_whitespace(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    compact_json = json.dumps(data, separators=(',', ':'))

    json_bytes = compact_json.encode('utf-8')

    return len(json_bytes)

def get_output_dir_path(data_path, medical_document, standard):
    return f"{data_path}{medical_document}/{standard}/output/"

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
        ["recepta", "FHIR"],
        ["recepta", "OpenEHR"],
        ["skierowanie", "FHIR"],
        ["skierowanie", "OpenEHR"],
        ["wyniki_badan", "FHIR"],
        ["wyniki_badan", "OpenEHR"],
        ["pomiar", "FHIR"],
        ["pomiar", "OpenEHR"],
    ]

    stats_list = []
    for item in input_data:
        for file_name in get_json_files(get_output_dir_path(DATA_DIRECTORY_PATH, item[0], item[1])):
            file_path = get_output_file_path(DATA_DIRECTORY_PATH, item[0], item[1], file_name)
            size = get_json_file_size_no_whitespace(file_path)
            unique_keys = count_unique_keys(file_path)
            output_name = get_output_name(item[0], item[1])

            final_stats = {}
            final_stats["output_name"] = output_name
            final_stats["medical_document"] = item[0]
            final_stats["standard"] = item[1]
            final_stats["file_name"] = file_name
            final_stats["size_bytes"] = size
            final_stats["unique_keys"] = unique_keys

            stats_list.append(final_stats)

    df = pd.DataFrame(stats_list)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = f"{OUTPUT_FILE_PREFIX}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"Zapisano statystyki do pliku {filename}")
