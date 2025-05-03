from fhir_utils import save_batch_response, send_batch_request

PATIENT_ID = "1"

def create_get_full_recepta_batch_bundle(patient_id):
    return {
        "resourceType": "Bundle",
        "type": "batch",
        "entry": [
            {
                "request": {
                    "method": "GET",
                    "url": (
                        f"MedicationRequest"
                        f"?subject=Patient/{patient_id}"
                        f"&_include=MedicationRequest:medication"
                        f"&_include=MedicationRequest:subject"
                        f"&_include=MedicationRequest:requester"
                    )
                }
            }
        ]
    }

if __name__ == "__main__":
    batch_bundle = create_get_full_recepta_batch_bundle(PATIENT_ID)
    batch_response = send_batch_request(batch_bundle)
    
    save_batch_response(batch_response, "recepta.json")
    print("Zapisano bundle recepta.")
