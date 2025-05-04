import json
import os
import requests

from fhir_conf import FHIR_SERVER, VERBOSE


def send_batch_request(bundle):
    headers = {"Content-Type": "application/fhir+json"}
    r = requests.post(FHIR_SERVER, headers=headers, json=bundle)
    r.raise_for_status()
    return r.json()

def get_resource(resource_type, resource_id, include=None, elements=None):
    url = f"{FHIR_SERVER}/{resource_type}"

    params = {
        "_id": resource_id
    }

    if include:
        params["_include"] = include

    if elements:
        params["_elements"] = elements

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        return None
    
def get_resource_by_ref(resource_type, ref_name, ref_value, include=None, elements=None):
    url = f"{FHIR_SERVER}/{resource_type}"

    params = {
        ref_name: ref_value
    }

    if include:
        params["_include"] = include

    if elements:
        params["_elements"] = elements

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        return None


def save_batch_response(batch_response, filename):
    if not os.path.exists("results"):
        os.makedirs("results")
        
    with open(f"results/{filename}", "w", encoding="utf-8") as f:
        json.dump(batch_response, f, indent=2, ensure_ascii=False)

IDENTIFIER_SYSTEM = "urn:oid:2.16.840.1.113883.3.4424.1.1.616"
def get_patient_id_by_pesel(identifier_value, verbose = VERBOSE):
    search_url = f"{FHIR_SERVER}/Patient"
    params = {
        "identifier": f"{IDENTIFIER_SYSTEM}|{identifier_value}"
    }

    response = requests.get(search_url, params=params)

    if response.status_code == 200:
        bundle = response.json()
        entries = bundle.get("entry", [])
        
        if entries:
            if verbose:
                print(f"Found {len(entries)} Patient(s):")
            for entry in entries:
                patient_id = entry["resource"]['id']
                if verbose:
                    print(f"Patient Id = {patient_id}")
                return patient_id
        else:
            if verbose:
                print("No patients found with that identifier.")
            return None
    else:
        print(f"Error: {response.status_code}")
        raise Exception(response.text)
    
def get_latest_resource_id_by_patient(resource_type, property_name, patient_id):
    url = f"{FHIR_SERVER}/{resource_type}"
    params = {
        property_name: f"Patient/{patient_id}",
        "_sort": "-_lastUpdated",
        "_count": 1
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        bundle = response.json()
        entries = bundle.get("entry", [])

        if not entries:
            raise Exception("No resources found.")
        else:
            return entries[0]["resource"]['id']
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")
