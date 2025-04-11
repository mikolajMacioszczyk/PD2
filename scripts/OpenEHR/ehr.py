import json
import requests
from openehr_conf import OPENEHR_SERVER, VERBOSE

BASE_URL = f"{OPENEHR_SERVER}ehrbase/rest/openehr/v1"
NAMESPACE = "PESEL"

ehr_headers = {
    'Content-Type': 'application/json',
    "Accept": "application/json",
    'Prefer': 'return=representation'
}

def _find_ehr_by_subject_id(pesel, verbose=False):

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
    
def _create_ehr_for_patient(pesel, verbose=False):
    ehr_body = {
        "archetype_node_id": "openEHR-EHR-EHR_STATUS.generic.v1",
        "name": {
            "value": "EHR status"
        },
        "uid": {
            "_type": "OBJECT_VERSION_ID",
            "value": "8849182c-82ad-4088-a07f-48ead4180515::openEHRSys.example.com::1"
        },
        "subject": {
            "_type": "PARTY_SELF",
            "external_ref": {
                "id": {
                    "_type": "GENERIC_ID",
                    "value": pesel,
                    "scheme": "urn:oid:2.16.840.1.113883.3.4424.1.1.616"
                },
                "namespace": NAMESPACE,
                "type": "PERSON"
            }
        },
        "is_queryable": True,
        "is_modifiable": True,
        "_type": "EHR_STATUS"
    }

    url = f"{BASE_URL}/ehr"
    response = requests.post(url, json=ehr_body, headers=ehr_headers)
    if response.status_code == 201:
        response_json = json.loads(response.text)
        ehr_id = response_json['ehr_id']['value']
        if verbose:
            print(f"EHR created for PESEL {pesel}: {ehr_id}")
        return ehr_id
    elif verbose:
        print(f"Failed to create EHR: {response.status_code} – {response.text}")
    return None

def get_or_create_ehr(pesel, verbose=VERBOSE):
    existing_ehr_id = _find_ehr_by_subject_id(pesel, verbose)
    if existing_ehr_id:
        return existing_ehr_id

    new_ehr_id = _create_ehr_for_patient(pesel, verbose)
    if new_ehr_id:
        return new_ehr_id

    raise Exception(f"Cannot create EHR for patient with {pesel}")
