import json
import requests
from openehr_conf import OPENEHR_SERVER

def create_ehr():
    ehr_url = f'{OPENEHR_SERVER}ehrbase/rest/openehr/v1/ehr'
    ehr_headers = {
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }

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
            "_type": "PARTY_SELF"
        },
        "is_queryable": True,
        "is_modifiable": True,
        "_type": "EHR_STATUS"
    }

    ehr_response = requests.post(ehr_url, headers=ehr_headers, json=ehr_body)
    if ehr_response.status_code == 201:
        response_json = json.loads(ehr_response.text)
        ehr_id = response_json['ehr_id']['value']
        return ehr_id
    raise Exception("Failed to create EHR")
