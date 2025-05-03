import json
import os
import requests
import urllib
from openehr_conf import OPENEHR_SERVER, VERBOSE

BASE_URL = f"{OPENEHR_SERVER}ehrbase/rest/openehr/v1"
NAMESPACE = "PESEL"

def save_composition_response(composition_response, filename):
    if not os.path.exists("results"):
        os.makedirs("results")

    with open(f"results/{filename}", "w", encoding="utf-8") as f:
        json.dump(composition_response, f, indent=2, ensure_ascii=False)

ehr_headers = {
    'Content-Type': 'application/json',
    "Accept": "application/json",
    'Prefer': 'return=representation'
}

def find_ehr_by_subject_id(pesel, verbose=VERBOSE):

    AQL_QUERY = f"""
    SELECT
        e/ehr_id/value
    FROM
        EHR e
    WHERE
        e/ehr_status/subject/external_ref/id/value = '{pesel}'
    """

    response = requests.post(
        f"{BASE_URL}/query/aql",
        headers=ehr_headers,
        json={"q": AQL_QUERY}
    )

    if response.status_code == 200:
        if verbose:
            print(f"Get EHR request succeded. Response: {response.json()}")
        result_set = response.json().get("rows", [])
        if result_set:
            ehr_id = result_set[0][0]
            return ehr_id
        elif verbose:
            print(f"Not found EHR identified by provided pesel")
    elif verbose:
        print(f"Get EHR request failed with code {response.status_code} and message {response.text}")
    return None

def get_latest_ehr_composition_id(ehr_id, verbose=VERBOSE):
    AQL_QUERY = f"""
    SELECT 
        c/uid/value AS uid, 
        c/name/value AS name, 
        c/context/start_time/value AS time_created 
    FROM 
        EHR e CONTAINS COMPOSITION c 
    WHERE 
        e/ehr_id/value = '{ehr_id}' 
    ORDER BY 
        c/context/start_time/value DESC 
    LIMIT 1
    """

    response = requests.post(
        f"{BASE_URL}/query/aql",
        headers=ehr_headers,
        json={"q": AQL_QUERY}
    )

    if response.status_code == 200:
        if verbose:
            print(f"Get EHR request succeded. Response: {response.json()}")
        result_set = response.json().get("rows", [])
        if result_set:
            composition_id = result_set[0][0]
            return composition_id
        elif verbose:
            print(f"Failed to get latest composition")
    elif verbose:
        print(f"Get EHR compositions request failed with code {response.status_code} and message {response.text}")
    return None
    
def get_composition_details(ehr_id, composition_id, verbose=VERBOSE):
    encoded_identifier = urllib.parse.quote_plus(composition_id)
    response = requests.get(
        f"{BASE_URL}/ehr/{ehr_id}/composition/{encoded_identifier}",
        headers=ehr_headers
    )

    if response.status_code == 200:
        if verbose:
            print(f"Get EHR request succeded. Response: {response.json()}")
        return response.json()
    elif verbose:
        print(f"Get EHR composition request failed with code {response.status_code} and message {response.text}")
    return None
    
