from datetime import datetime
import json
import os
import pandas as pd
import json

DATA_DIRECTORY_PATH = "../../data/"
OUTPUT_FILE_PATH = "results/file_metrics.csv"
GROUPED_OUTPUT_FILE_PATH = "results/file_metrics_grouped.csv"

def extract_paths(data, current_path=""):
    paths = []
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{current_path}.{key}" if current_path else key
            paths.extend(extract_paths(value, new_path))
    elif isinstance(data, list):
        for index, item in enumerate(data):
            new_path = f"{current_path}[{index}]"
            paths.extend(extract_paths(item, new_path))
    else:
        paths.append(current_path)
    return paths

def average_path_length(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    paths = extract_paths(json_data)
    total_length = sum(len(path.split(".")) for path in paths)
    return total_length / len(paths) if paths else 0

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

def calculate_file_metrics():
    input_data = [
        ["recepta", "FHIR"],
        ["recepta", "OpenEHR"],
        ["skierowanie", "FHIR"],
        ["skierowanie", "OpenEHR"],
        ["wyniki_badan", "FHIR"],
        ["wyniki_badan", "OpenEHR"],
        ["pomiar", "FHIR"],
        ["pomiar", "OpenEHR"],
        ["iniekcja", "FHIR"],
        ["iniekcja", "OpenEHR"],
    ]

    stats_list = []
    for item in input_data:
        for file_name in get_json_files(get_output_dir_path(DATA_DIRECTORY_PATH, item[0], item[1])):
            file_path = get_output_file_path(DATA_DIRECTORY_PATH, item[0], item[1], file_name)
            if "FLAT" in file_path:
                format = "FLAT"
            elif "JSON" in file_path:
                format = "JSON"
            else:
                raise Exception(f"Invalid format for path: {file_path}")
            size = get_json_file_size_no_whitespace(file_path)
            unique_keys = count_unique_keys(file_path)
            avg_path_len = round(average_path_length(file_path), 3)
            output_name = get_output_name(item[0], item[1])

            final_stats = {}
            final_stats["output_name"] = output_name
            final_stats["medical_document"] = item[0]
            final_stats["standard"] = item[1]
            final_stats["format"] = format
            final_stats["standard_format"] = f"{item[1]}_{format}"
            final_stats["file_name"] = file_name
            final_stats["size_bytes"] = size
            final_stats["unique_keys"] = unique_keys
            final_stats["avg_path_len"] = avg_path_len

            stats_list.append(final_stats)

    df = pd.DataFrame(stats_list)
    df.to_csv(OUTPUT_FILE_PATH, index=False)
    print(f"Zapisano statystyki do pliku {OUTPUT_FILE_PATH}")

    cols_to_average = [
        "size_bytes", "unique_keys", "avg_path_len"
    ]

    grouped = df.groupby("standard_format")[cols_to_average].agg(["mean", "var"]).reset_index()
    grouped.columns = [
        "standard_format" if col[0] == "standard_format" else f"{'avg_' if col[1]=='mean' else 'var_'}{col[0]}"
        for col in grouped.columns
    ]
    grouped = grouped.round(3)
    grouped.to_csv(GROUPED_OUTPUT_FILE_PATH, index=False)
    print(f"Zapisano statystyki zgrupowane do pliku {GROUPED_OUTPUT_FILE_PATH}")

if __name__ == "__main__":
    calculate_file_metrics()