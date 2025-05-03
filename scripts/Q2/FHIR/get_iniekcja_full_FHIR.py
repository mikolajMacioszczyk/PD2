from fhir_utils import get_latest_resource_id_by_patient, get_patient_id_by_pesel, save_batch_response, send_batch_request

PATIENT_PESEL = 80010112350

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

if __name__ == "__main__":
    patient_id = get_patient_id_by_pesel(PATIENT_PESEL)
    print(f"Patient id = {patient_id}")

    last_updated_resource_id = get_latest_resource_id_by_patient("MedicationAdministration", "subject", patient_id)
    print(f"Last updated MedicationAdministration = {last_updated_resource_id}")

    batch_bundle = create_get_full_iniekcja_batch_bundle(patient_id, last_updated_resource_id)
    batch_response = send_batch_request(batch_bundle)
    
    save_batch_response(batch_response, "iniekcja.json")
    print("Saved bundle for iniekcja.")
