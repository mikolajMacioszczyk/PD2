import json
import requests

from fhir_conf import FHIR_SERVER


def send_batch_request(bundle):
    headers = {"Content-Type": "application/fhir+json"}
    r = requests.post(FHIR_SERVER, headers=headers, json=bundle)
    r.raise_for_status()
    return r.json()


def save_batch_response(batch_response, filename):
    with open(f"results/{filename}", "w", encoding="utf-8") as f:
        json.dump(batch_response, f, indent=2, ensure_ascii=False)