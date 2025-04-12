import json
import os
from fhir_conf import DATA_DIRECTORY_PATH

def save_to_output_file(data, medical_document_type, file_name):
    folder_path = f"{DATA_DIRECTORY_PATH}{medical_document_type}/FHIR/output"
    output_file_path = f"{folder_path}/{file_name}"

    os.makedirs(folder_path, exist_ok=True)
    
    with open(output_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)