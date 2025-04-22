import requests
import json
from fhir_conf import FHIR_SERVER

PATIENT_ID = "207"

def get_med_admin_with_includes(patient_id):
    url = (
        f"{FHIR_SERVER}/MedicationAdministration"
        f"?subject=Patient/{patient_id}"
        f"&_include=MedicationAdministration:medication"
        f"&_include=MedicationAdministration:subject"
        f"&_include=MedicationAdministration:performer"
    )
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def get_care_plan_with_includes(patient_id):
    url = (
        f"{FHIR_SERVER}/CarePlan"
        f"?subject=Patient/{patient_id}"
        f"&_include=CarePlan:goal"
    )
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def get_allergy_intollerance(patient_id):
    url = (
        f"{FHIR_SERVER}/AllergyIntolerance"
        f"?patient=Patient/{patient_id}"
    )
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def merge_bundles(bundles):
    resources = {}
    for b in bundles:
        for entry in b.get("entry", []):
            res = entry.get("resource")
            if res:
                res_id = f"{res['resourceType']}/{res['id']}"
                resources[res_id] = res

    merged_bundle = {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": [{"resource": r} for r in resources.values()]
    }
    return merged_bundle
    
medical_administration_data = get_med_admin_with_includes(PATIENT_ID)
care_plan_data = get_care_plan_with_includes(PATIENT_ID)
allergy_intollerance_data = get_allergy_intollerance(PATIENT_ID)
final_bundle = merge_bundles([medical_administration_data, care_plan_data, allergy_intollerance_data])

with open("fhir.json", "w", encoding="utf-8") as f:
    json.dump(final_bundle, f, indent=2, ensure_ascii=False)

print("Zapisano Bundle z MedicationAdministration i powiązanymi zasobami.")
