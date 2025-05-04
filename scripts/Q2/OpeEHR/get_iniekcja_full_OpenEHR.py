from openEHR_utils import get_property, find_ehr_by_subject_id, get_composition_details, get_latest_ehr_composition_id, save_composition_response

PATIENT_PESEL = 80010112350

def get_mediaction_name(ehr_id, composition_id):
    return get_property(ehr_id, 
                        composition_id,
                        archetype_type="INSTRUCTION",
                        archetype_value="openEHR-EHR-INSTRUCTION.medication_order.v0",
                        property_path="activities[at0001]/description[at0002]/items[at0070]/value/value")[0]

def get_dose_value_and_unit(ehr_id, composition_id):
    return get_property(ehr_id, 
                        composition_id,
                        archetype_type="INSTRUCTION",
                        archetype_value="openEHR-EHR-INSTRUCTION.medication_order.v0",
                        property_path="activities[at0001]/description[at0002]/items[at0109]/value/value")[0]

def get_allergy_reaction(ehr_id, composition_id):
    return get_property(ehr_id, 
                        composition_id,
                        archetype_type="EVALUATION",
                        archetype_value="openEHR-EHR-EVALUATION.adverse_reaction_risk.v1",
                        property_path="data[at0001]/items[at0006]/value/value")[0]

if __name__ == "__main__":
    ehr_id = find_ehr_by_subject_id(PATIENT_PESEL)
    print(f"EHR id = {ehr_id}")

    last_updated_id = get_latest_ehr_composition_id(ehr_id, "Progress Note")
    print(f"Last updated Progress Note composition = {last_updated_id}")

    composition = get_composition_details(ehr_id, last_updated_id)
    save_composition_response(composition, "iniekcja.json")
    print("Saved composition for iniekcja.")

    medication_name = get_mediaction_name(ehr_id, last_updated_id)
    print(f"Medication name = {medication_name}")

    dose_value_unit = get_dose_value_and_unit(ehr_id, last_updated_id)
    print(f"Dose value and unit = {dose_value_unit}")

    allergy_reaction = get_allergy_reaction(ehr_id, last_updated_id)
    print(f"Allergy reaction = {allergy_reaction}")
