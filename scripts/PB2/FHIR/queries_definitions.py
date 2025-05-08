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

def create_get_full_iniekcja_batch_bundle(patient_id, medication_administration_id):
    return {
        "resourceType": "Bundle",
        "type": "batch",
        "entry": [
            {
                "request": {
                    "method": "GET",
                    "url": (
                        f"MedicationAdministration"
                        f"?_id={medication_administration_id}"
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

def create_get_allergy_reaction_batch_bundle(patient_id, medication_administration_id):
    return {
        "resourceType": "Bundle",
        "type": "batch",
        "entry": [
            {
                "request": {
                    "method": "GET",
                    "url": (
                        f"MedicationAdministration"
                        f"?_id={medication_administration_id}"
                    )
                }
            },
            {
                "request": {
                    "method": "GET",
                    "url": (
                        f"CarePlan"
                        f"?patient=Patient/{patient_id}"
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

def create_get_full_wyniki_badan_batch_bundle(diagnostic_report_id):
    return {
        "resourceType": "Bundle",
        "type": "batch",
        "entry": [
            {
                "request": {
                    "method": "GET",
                    "url": (
                        f"DiagnosticReport"
                        f"?_id={diagnostic_report_id}"
                        f"&_include=DiagnosticReport:subject"
                        f"&_include=DiagnosticReport:performer"
                        f"&_include=DiagnosticReport:specimen"
                        f"&_include=DiagnosticReport:result"
                        f"&_include=DiagnosticReport:*"
                    )
                }
            },
        ]
    }