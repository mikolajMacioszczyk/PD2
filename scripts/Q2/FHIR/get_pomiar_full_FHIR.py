from fhir_utils import get_latest_updated_entry, get_patient_id_by_pesel, get_resource_list_by_patient, save_batch_response, send_batch_request

PATIENT_PESEL = 80010112349

def create_get_full_pomiar_batch_bundle(observation_id):
    return {
        "resourceType": "Bundle",
        "type": "batch",
        "entry": [
            {
                "request": {
                    "method": "GET",
                    "url": (
                        f"Observation"
                        f"?_id={observation_id}"
                        f"&_include=Observation:subject"
                        f"&_include=Observation:device"
                        f"&_include=Observation:encounter"
                        f"&_include=Observation:performer"
                        f"&_include:iterate=Device:definition"
                    )
                }
            },
        ]
    }

if __name__ == "__main__":
    patient_id = get_patient_id_by_pesel(PATIENT_PESEL)
    print(f"Patient id = {patient_id}")

    resource_list = get_resource_list_by_patient("Observation", "subject", patient_id)
    last_updated = get_latest_updated_entry(resource_list)
    print(f"Last updated Observation = {last_updated['id']}")

    batch_bundle = create_get_full_pomiar_batch_bundle(last_updated['id'])
    batch_response = send_batch_request(batch_bundle)
    
    save_batch_response(batch_response, "pomiar.json")
    print("Saved bundle for pomiar.")
