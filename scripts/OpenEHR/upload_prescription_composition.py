

import json
import requests
from ehr import get_or_create_ehr
from openehr_conf import OPENEHR_SERVER, DATA_DIRECTORY_PATH

composition_file_name = 'ePrescription-flat.json'
pesel = "80010112345"
composition_file_path = f"{DATA_DIRECTORY_PATH}recepta/OpenEHR/{composition_file_name}"

with open(composition_file_path, "r", encoding="utf-8") as file:
    composition_data = json.load(file)

ehr_id = get_or_create_ehr(pesel)
print(f"EHR ID: {ehr_id}")
template_id = "ePrescription"
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
    else:
        print("'Location' header not found in response.")
else:
    print(f"Failed to create composition. Status Code: {response.status_code}")
    try:
        print("Response:", response.json())
    except Exception:
        print("No JSON body in response.")