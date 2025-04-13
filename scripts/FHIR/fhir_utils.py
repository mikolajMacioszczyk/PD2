import json
import os
import urllib

import requests
from fhir_conf import FHIR_SERVER, VERBOSE, DATA_DIRECTORY_PATH

def _get_full_path(medical_document_type, relative_path):
    return os.path.join(DATA_DIRECTORY_PATH, medical_document_type, "FHIR", "input", relative_path)

def get_bundle(resource_name, resource_id, additional_resources):
    full_bundle = get_resource(resource_name, resource_id)
    if full_bundle:
        for resource in additional_resources:
            resource_bundle = get_resource(resource['name'], resource['id'])
            full_bundle['entry'].append(resource_bundle['entry'][0])
    return full_bundle

def get_resource(resource_type, resource_id):
    url = f"{FHIR_SERVER}/{resource_type}"

    params = {
        "_id": resource_id,
        "_include": "*"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        return None

def load_fhir_resource(medical_document_type, file_path, resource_class, is_full_path = False):
    full_path = file_path if is_full_path else _get_full_path(medical_document_type, file_path)
    with open(full_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return resource_class.model_validate(data)

def load_resources_from_dictionary(medical_document_type, dictionary_path, resource_class):
    full_dictionary_path = _get_full_path(medical_document_type, dictionary_path)
    resources_files = [os.path.join(full_dictionary_path, f) for f in os.listdir(full_dictionary_path) if os.path.isfile(os.path.join(full_dictionary_path, f)) and f.endswith(".json")]
    return [load_fhir_resource(medical_document_type, resource_file, resource_class, is_full_path=True) for resource_file in resources_files]

def post_resource(resource, verbose = VERBOSE):
    resource_type = resource.__class__.__name__
    url = f"{FHIR_SERVER}/{resource_type}"

    if verbose:
        print(f"Posting {resource_type} to {url}")
        print("Request payload:")
        print(resource.json(indent=2))
    
    response = requests.post(
        url,
        headers={"Content-Type": "application/fhir+json"},
        data=resource.json()
    )
    
    if response.status_code == 201:
        if verbose:
            print(f"Response status code: {response.status_code}")
            print("Response headers:")
            print(response.headers)
            try:
                print("Response body:")
                print(response.json())
            except Exception:
                print(response.text)
                
        location = response.headers.get("Location", "")
        resource_id = None
        if location:
            parts = location.strip("/").split("/")
            try:
                idx = parts.index("_history")
                resource_id = parts[idx - 1]
            except ValueError:
                if len(parts) >= 2:
                    resource_id = parts[-2]
        
        return resource_id
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
    
def create_or_get_by_identifier(resource, identifier_system, verbose = VERBOSE):
    resource_type = resource.__class__.__name__
    
    identifier_value = next((
        identifier for identifier in resource.identifier
        if identifier.system == identifier_system
    ), None)

    if identifier_value is None:
        raise Exception(f"identifier with system {identifier_system} not found")

    encoded_identifier = urllib.parse.quote_plus(
        f"{identifier_value.system}|{identifier_value.value}"
    )
    url = f"{FHIR_SERVER}/{resource_type}?identifier={encoded_identifier}"

    if verbose:
        print(f"Putting {resource_type} to {url}")
        print("Request payload:")
        print(resource.json(indent=2))

    response = requests.put(
        url,
        headers={"Content-Type": "application/fhir+json"},
        data=resource.json(indent=None)
    )

    if response.status_code in (200, 201):
        if verbose:
            print(f"Response status code: {response.status_code}")
            print("Response headers:")
            print(response.headers)
            try:
                print("Response body:")
                print(response.json())
            except Exception:
                print(response.text)

        location = response.headers.get("Location") or response.headers.get("Content-Location", "")
        resource_id = None
        if location:
            parts = location.strip("/").split("/")
            try:
                idx = parts.index("_history")
                resource_id = parts[idx - 1]
            except ValueError:
                if len(parts) >= 2:
                    resource_id = parts[-2]
        
        return resource_id
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")