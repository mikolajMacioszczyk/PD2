from enum import Enum
import json
import requests
from ehr import get_or_create_ehr
from openehr_conf import OPENEHR_SERVER
from file_output_openehr import save_to_output_file

class COMPOSITION_FORMAT(Enum):
    JSON = "JSON"
    FLAT = "FLAT"
    XML = "XML"
    STRUCTURED = "STRUCTURED"

def get_composition(ehr_id, composition_id, format_type):
    url = f"{OPENEHR_SERVER}ehrbase/rest/openehr/v1/ehr/{ehr_id}/composition/{composition_id}"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    params = {
        "format": format_type
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get composition with id {composition_id} for ehr {ehr_id}. Status code: {response.status_code}. Message: {response.text}")
        return None


def upload_composition(pesel, composition_file_path, template_id):
    with open(composition_file_path, "r", encoding="utf-8") as file:
        composition_data = json.load(file)

    ehr_id = get_or_create_ehr(pesel)
    print(f"EHR ID: {ehr_id}")
    format_type = "FLAT"

    url = f"{OPENEHR_SERVER}ehrbase/rest/openehr/v1/ehr/{ehr_id}/composition"
    params = {
        "templateId": template_id,
        "format": format_type
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, params=params, json=composition_data)

    print(f"Status Code: {response.status_code}")
    if response.status_code == 204:
        location_url = response.headers.get("Location", "")
        if location_url:
            composition_id = location_url.rstrip("/").split("/")[-1]
            print(f"Composition created with ID: {composition_id}")
            return {
                "ehr_id": ehr_id,
                "composition_id": composition_id
            }
        else:
            print("'Location' header not found in response.")
    else:
        print(f"Failed to create composition. Status Code: {response.status_code}")
        try:
            print("Response:", response.json())
        except Exception:
            print("No JSON body in response.")
    return None

def upload_and_save(pesel, composition_file_path, template_id, medical_document_type):
    upload_result = upload_composition(pesel, composition_file_path, template_id)
    if upload_result:
        full_composition = get_composition(upload_result["ehr_id"], upload_result["composition_id"], COMPOSITION_FORMAT.JSON.value)
        if full_composition:
            file_name = f"composition-{medical_document_type}-JSON-{upload_result['composition_id']}.json"
            save_to_output_file(full_composition, medical_document_type, file_name)
            print(f"Saved full composition to {file_name}")

        flat_composition = get_composition(upload_result["ehr_id"], upload_result["composition_id"], COMPOSITION_FORMAT.FLAT.value)
        if flat_composition:
            file_name = f"composition-{medical_document_type}-FLAT-{upload_result['composition_id']}.json"
            save_to_output_file(flat_composition, medical_document_type, file_name)
            print(f"Saved flat composition to {file_name}")