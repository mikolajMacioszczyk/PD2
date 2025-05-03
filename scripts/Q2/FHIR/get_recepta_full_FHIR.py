from fhir_utils import get_latest_resource_id_by_patient, get_patient_id_by_pesel, save_batch_response, send_batch_request

PATIENT_PESEL = 80010112345

def create_get_full_recepta_batch_bundle(medication_request_id):
    return {
        "resourceType": "Bundle",
        "type": "batch",
        "entry": [
            {
                "request": {
                    "method": "GET",
                    "url": (
                        f"MedicationRequest"
                        f"?_id={medication_request_id}"
                        f"&_include=MedicationRequest:medication"
                        f"&_include=MedicationRequest:subject"
                        f"&_include=MedicationRequest:requester"
                    )
                }
            }
        ]
    }

if __name__ == "__main__":
    patient_id = get_patient_id_by_pesel(PATIENT_PESEL)
    print(f"Patient id = {patient_id}")

    last_updated_resource_id = get_latest_resource_id_by_patient("MedicationRequest", "subject", patient_id)
    print(f"Last updated MedicationRequest = {last_updated_resource_id}")

    batch_bundle = create_get_full_recepta_batch_bundle(last_updated_resource_id)
    batch_response = send_batch_request(batch_bundle)
    
    save_batch_response(batch_response, "recepta.json")
    print("Saved bundle for recepta.")
