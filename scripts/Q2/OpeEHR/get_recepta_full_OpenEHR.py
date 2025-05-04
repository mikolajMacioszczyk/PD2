from openEHR_utils import find_ehr_by_subject_id, get_composition_details, get_latest_ehr_composition_id, get_property, save_composition_response

PATIENT_PESEL = 80010112345

def get_pharmaceutical_form(ehr_id, composition_id):
    return get_property(ehr_id, 
                        composition_id,
                        archetype_type="CLUSTER",
                        archetype_value="openEHR-EHR-CLUSTER.medication_substance.v0",
                        property_path="items[at0133]/value/value")[0]

def get_frequency(ehr_id, composition_id):
    frequency = get_property(ehr_id, 
                        composition_id,
                        archetype_type="CLUSTER",
                        archetype_value="openEHR-EHR-CLUSTER.timing_daily.v0",
                        property_path="items[at0003]/value")[0]
    return f"{frequency['magnitude']} {frequency['units']}"

def get_validity_period(ehr_id, composition_id):
    return get_property(ehr_id, 
                        composition_id,
                        archetype_type="CLUSTER",
                        archetype_value="openEHR-EHR-CLUSTER.medication_authorisation.v0",
                        property_path="items[at0072]/value/value")[0]

if __name__ == "__main__":
    ehr_id = find_ehr_by_subject_id(PATIENT_PESEL)
    print(f"EHR id = {ehr_id}")

    last_updated_id = get_latest_ehr_composition_id(ehr_id, "Prescription")
    print(f"Last updated Prescription composition = {last_updated_id}")

    composition = get_composition_details(ehr_id, last_updated_id)
    save_composition_response(composition, "recepta.json")
    print("Saved composition for recepta.")

    pharmaceutical_form = get_pharmaceutical_form(ehr_id, last_updated_id)
    print(f"Pharmaceutical form = {pharmaceutical_form}")

    frequency = get_frequency(ehr_id, last_updated_id)
    print(f"Frequency = {frequency}")

    validity_period = get_validity_period(ehr_id, last_updated_id)
    print(f"Validity period = {validity_period}")
