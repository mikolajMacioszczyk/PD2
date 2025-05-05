from openEHR_utils import find_ehr_by_subject_id, get_composition_details, get_latest_ehr_composition_id, get_property, save_composition_response

PATIENT_PESEL = 80010112346

def get_test_name(ehr_id, composition_id):
    return get_property(ehr_id, 
                        composition_id,
                        archetype_type="OBSERVATION",
                        archetype_value="openEHR-EHR-OBSERVATION.lab_test.v1",
                        property_path="data[at0001]/events[at0002]/data[at0003]/items[at0005]/value/value")[0]

def get_health_problem(ehr_id, composition_id):
    return get_property(ehr_id, 
                        composition_id,
                        archetype_type="EVALUATION",
                        archetype_value="openEHR-EHR-EVALUATION.problem.v1",
                        property_path="data[at0001]/items[at0002]/value/value")[0]

def get_alergen(ehr_id, composition_id):
    return get_property(ehr_id, 
                        composition_id,
                        archetype_type="EVALUATION",
                        archetype_value="openEHR-EHR-EVALUATION.adverse.v1",
                        property_path="data[at0002]/items[at0003]/value/value")[0]

if __name__ == "__main__":
    ehr_id = find_ehr_by_subject_id(PATIENT_PESEL)
    print(f"EHR id = {ehr_id}")

    last_updated_id = get_latest_ehr_composition_id(ehr_id, "Referral document")
    print(f"Last updated Referral document composition = {last_updated_id}")

    composition = get_composition_details(ehr_id, last_updated_id)
    save_composition_response(composition, "skierowanie.json")
    print("Saved composition for skierowanie.")

    test_name = get_test_name(ehr_id, last_updated_id)
    print(f"Test name = {test_name}")

    health_problem = get_health_problem(ehr_id, last_updated_id)
    print(f"Health problem = {health_problem}")

    alergen = get_alergen(ehr_id, last_updated_id)
    print(f"Alergen = {alergen}")
