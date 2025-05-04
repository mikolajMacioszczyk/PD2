from fhir_utils import get_latest_resource_id_by_patient, get_patient_id_by_pesel, get_resource, save_batch_response, send_batch_request

PATIENT_PESEL = 80010112347

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

def get_specimen_collection_time(diagnostic_report_id):
    resource_bundle = get_resource("DiagnosticReport", diagnostic_report_id, include="DiagnosticReport:specimen", elements="specimen")
    return resource_bundle["entry"][1]["resource"]["collection"]["collectedDateTime"]

def get_glucose_result(diagnostic_report_id):
    resource_bundle = get_resource("DiagnosticReport", diagnostic_report_id, include="DiagnosticReport:result", elements="result")
    glucose_observation = [entry["resource"] for entry in resource_bundle["entry"] 
                           if entry["resource"]["resourceType"] == "Observation" and entry["resource"]["code"]["coding"][0]["code"] == "33747003" ][0]
    return f"{glucose_observation["valueQuantity"]['value']} {glucose_observation["valueQuantity"]['unit']}"

def get_HbA1c_SNOMED_CT(diagnostic_report_id):
    resource_bundle = get_resource("DiagnosticReport", diagnostic_report_id, include="DiagnosticReport:result", elements="specimen")
    observations = [f"{entry["resource"]['code']['coding'][0]['display']}: {entry["resource"]['code']['coding'][0]['code']}" for entry in resource_bundle["entry"] 
                        if entry["resource"]["resourceType"] == "Observation"]
    return observations

if __name__ == "__main__":
    patient_id = get_patient_id_by_pesel(PATIENT_PESEL)
    print(f"Patient id = {patient_id}")

    last_updated_resource_id = get_latest_resource_id_by_patient("DiagnosticReport", "subject", patient_id)
    print(f"Last updated DiagnosticReport = {last_updated_resource_id}")

    batch_bundle = create_get_full_wyniki_badan_batch_bundle(last_updated_resource_id)
    batch_response = send_batch_request(batch_bundle)
    
    save_batch_response(batch_response, "wyniki_badan.json")
    print("Saved bundle for wyniki_badan.")

    specimen_collection_time = get_specimen_collection_time(last_updated_resource_id)
    print(f"Specimen collection time = {specimen_collection_time}")

    glucose_result = get_glucose_result(last_updated_resource_id)
    print(f"Glucose result = {glucose_result}")

    HbA1c_SNOMED_CT = get_HbA1c_SNOMED_CT(last_updated_resource_id)
    print(f"HbA1c SNOMED CT code = {HbA1c_SNOMED_CT}")

