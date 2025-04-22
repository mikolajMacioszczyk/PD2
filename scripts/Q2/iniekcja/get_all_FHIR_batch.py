import requests
import json
from fhir_conf import FHIR_SERVER

PATIENT_ID = "207"

def create_batch_bundle(patient_id):
    return {
        "resourceType": "Bundle",
        "type": "batch",
        "entry": [
            {
                "request": {
                    "method": "GET",
                    "url": (
                        f"MedicationAdministration"
                        f"?subject=Patient/{patient_id}"
                        f"&_include=MedicationAdministration:medication"
                        f"&_include=MedicationAdministration:subject"
                        f"&_include=MedicationAdministration:performer"
                    )
                }
            },
            {
                "request": {
                    "method": "GET",
                    "url": (
                        f"CarePlan"
                        f"?subject=Patient/{patient_id}"
                        f"&_include=CarePlan:goal"
                    )
                }
            },
            {
                "request": {
                    "method": "GET",
                    "url": (
                        f"AllergyIntolerance"
                        f"?patient=Patient/{patient_id}"
                    )
                }
            }
        ]
    }

def send_batch_request(bundle):
    headers = {"Content-Type": "application/fhir+json"}
    r = requests.post(FHIR_SERVER, headers=headers, json=bundle)
    r.raise_for_status()
    return r.json()
    
batch_bundle = create_batch_bundle(PATIENT_ID)
batch_response = send_batch_request(batch_bundle)

with open("fhir_batch.json", "w", encoding="utf-8") as f:
    json.dump(batch_response, f, indent=2, ensure_ascii=False)

print("Zapisano Bundle z MedicationAdministration i powiązanymi zasobami.")
