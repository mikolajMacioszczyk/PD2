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