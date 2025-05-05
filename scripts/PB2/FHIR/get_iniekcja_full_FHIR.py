from fhir_utils import get_resource, get_latest_resource_id_by_patient, get_patient_id_by_pesel, save_batch_response, send_batch_request

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

def get_medication_name(medication_administration_id):
    resource_bundle = get_resource("MedicationAdministration", medication_administration_id, include="MedicationAdministration:medication", elements="medication")
    return resource_bundle["entry"][1]["resource"]["code"]["text"]

def get_dose_value_and_unit(medication_administration_id):
    resource_bundle = get_resource("MedicationAdministration", medication_administration_id, elements="dosage")
    dose = resource_bundle["entry"][0]["resource"]["dosage"]["dose"]
    return f"{dose['value']} {dose['unit']}"

def get_allergy_reaction(medication_administration_id, patient_id):
    resource_bundle = send_batch_request({
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
    })

    medication_administration = resource_bundle["entry"][0]["resource"]["entry"][0]["resource"]
    care_plan_reference = medication_administration['basedOn'][0]['reference'].split("/")[1] 

    care_plan = [entry['resource'] for entry in resource_bundle["entry"][1]["resource"]["entry"]
                 if entry['resource']['id'] == care_plan_reference][0]
    
    supporting_info_references = [item["reference"].split("/")[1] 
                                  for item in care_plan["supportingInfo"]
                                  if item["reference"].split("/")[0] == "AllergyIntolerance"]
    
    allergy_intolerances = [item['resource']["reaction"][0]["manifestation"][0]["concept"]["text"]
                  for item in resource_bundle["entry"][2]["resource"]["entry"]
                  if item["resource"]["id"] in supporting_info_references]

    return allergy_intolerances

if __name__ == "__main__":
    patient_id = get_patient_id_by_pesel(PATIENT_PESEL)
    print(f"Patient id = {patient_id}")

    last_updated_resource_id = get_latest_resource_id_by_patient("MedicationAdministration", "subject", patient_id)
    print(f"Last updated MedicationAdministration = {last_updated_resource_id}")

    batch_bundle = create_get_full_iniekcja_batch_bundle(patient_id, last_updated_resource_id)
    batch_response = send_batch_request(batch_bundle)
    
    save_batch_response(batch_response, "iniekcja.json")
    print("Saved bundle for iniekcja.")

    medication_name = get_medication_name(last_updated_resource_id)
    print(f"Medication name = {medication_name}")

    dose_value_unit = get_dose_value_and_unit(last_updated_resource_id)
    print(f"Dose value and unit = {dose_value_unit}")

    allergy_reaction = get_allergy_reaction(last_updated_resource_id, patient_id)
    print(f"Allergy reaction = {allergy_reaction}")
