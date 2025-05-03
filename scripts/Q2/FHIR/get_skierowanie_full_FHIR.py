from fhir_utils import get_latest_resource_id_by_patient, get_patient_id_by_pesel, save_batch_response, send_batch_request

PATIENT_PESEL = 80010112346

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
    patient_id = get_patient_id_by_pesel(PATIENT_PESEL)
    print(f"Patient id = {patient_id}")

    last_updated_resource_id = get_latest_resource_id_by_patient("ServiceRequest", "subject", patient_id)
    print(f"Last updated ServiceRequest = {last_updated_resource_id}")

    batch_bundle = create_get_full_skierowanie_batch_bundle(patient_id, last_updated_resource_id)
    batch_response = send_batch_request(batch_bundle)
    
    save_batch_response(batch_response, "skierowanie.json")
    print("Saved bundle for skierowanie.")

