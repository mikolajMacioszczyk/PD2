import json
import urllib

import requests
from fhir_conf import FHIR_SERVER, VERBOSE

def load_fhir_resource(file_path, resource_class):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return resource_class.model_validate(data)

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