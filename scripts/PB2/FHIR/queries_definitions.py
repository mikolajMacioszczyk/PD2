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

def create_get_health_problem_batch_bundle(patient_id, service_request_id):
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
            }
        ]
    }

def create_get_alergen_batch_bundle(patient_id, service_request_id):
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