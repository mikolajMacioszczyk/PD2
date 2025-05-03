from fhir_utils import get_latest_updated_entry, get_patient_id_by_pesel, get_resource_list_by_patient, save_batch_response, send_batch_request

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

if __name__ == "__main__":
    patient_id = get_patient_id_by_pesel(PATIENT_PESEL)
    print(f"Patient id = {patient_id}")

    resource_list = get_resource_list_by_patient("DiagnosticReport", "subject", patient_id)
    last_updated = get_latest_updated_entry(resource_list)
    print(f"Last updated DiagnosticReport = {last_updated['id']}")

    batch_bundle = create_get_full_wyniki_badan_batch_bundle(last_updated['id'])
    batch_response = send_batch_request(batch_bundle)
    
    save_batch_response(batch_response, "wyniki_badan.json")
    print("Saved bundle for wyniki_badan.")

