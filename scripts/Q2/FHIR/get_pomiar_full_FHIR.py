from fhir_utils import save_batch_response, send_batch_request

PATIENT_ID = 13
OBSERVATION_ID = 19

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
    batch_bundle = create_get_full_pomiar_batch_bundle(OBSERVATION_ID)
    batch_response = send_batch_request(batch_bundle)
    
    save_batch_response(batch_response, "pomiar.json")
    print("Zapisano bundle pomiar.")
