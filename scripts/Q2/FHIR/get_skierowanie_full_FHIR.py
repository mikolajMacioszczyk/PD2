from fhir_utils import save_batch_response, send_batch_request

PATIENT_ID = 6
SERVICE_REQUEST_ID = 12

def create_get_full_skierowanie_batch_bundle(patient_id, service_request_id):
    return {
        "resourceType": "Bundle",
        "type": "batch",
        "entry": [
            {
                "request": {
                    "method": "GET",
                    "url": (
                        f"ServiceRequest"
                        f"?_id={service_request_id}"
                        f"&_include=ServiceRequest:subject"
                        f"&_include=ServiceRequest:requester"
                    )
                }
            },
            {
                "request": {
                    "method": "GET",
                    "url": (
                        f"Condition"
                        f"?subject=Patient/{patient_id}"
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

if __name__ == "__main__":
    batch_bundle = create_get_full_skierowanie_batch_bundle(PATIENT_ID, SERVICE_REQUEST_ID)
    batch_response = send_batch_request(batch_bundle)
    
    save_batch_response(batch_response, "skierowanie.json")
    print("Zapisano bundle skierowanie.")
