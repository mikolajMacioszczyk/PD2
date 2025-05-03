from fhir_utils import save_batch_response, send_batch_request

PATIENT_ID = "20"

def create_get_full_iniekcja_batch_bundle(patient_id):
    return {
        "resourceType": "Bundle",
        "type": "batch",
        "entry": [
            {
                "request": {
                    "method": "GET",
                    "url": (
                        f"MedicationAdministration"
                        f"?subject=Patient/{patient_id}"
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

if __name__ == "__main__":
    batch_bundle = create_get_full_iniekcja_batch_bundle(PATIENT_ID)
    batch_response = send_batch_request(batch_bundle)
    
    save_batch_response(batch_response, "iniekcja.json")
    print("Zapisano bundle injekcja.")
