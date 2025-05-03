from fhir_utils import save_batch_response, send_batch_request

PATIENT_ID = 27
DIAGNOSTIC_REPORT_ID = 33

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
    batch_bundle = create_get_full_wyniki_badan_batch_bundle(DIAGNOSTIC_REPORT_ID)
    batch_response = send_batch_request(batch_bundle)
    
    save_batch_response(batch_response, "wyniki_badan.json")
    print("Zapisano bundle wyniki_badan.")
