from openEHR_utils import find_ehr_by_subject_id, get_composition_details, get_latest_ehr_composition_id, get_property, save_composition_response

PATIENT_PESEL = 80010112347

def get_specimen_collection_time(ehr_id, composition_id):
    return get_property(ehr_id, 
                        composition_id,
                        archetype_type="CLUSTER",
                        archetype_value="openEHR-EHR-CLUSTER.specimen.v1",
                        property_path="items[at0015]/value/value")[0]

def get_glucose_result(ehr_id, composition_id):
    glucose_result = get_property(ehr_id, 
                        composition_id,
                        archetype_type="CLUSTER",
                        archetype_value="openEHR-EHR-CLUSTER.laboratory_test_analyte.v1",
                        property_path="items[at0001]/value")[0]
    return f"{glucose_result['magnitude']} {glucose_result['units']}"

def get_HbA1c_SNOMED_CT(ehr_id, composition_id):
    return get_property(ehr_id, 
                        composition_id,
                        archetype_type="CLUSTER",
                        archetype_value="openEHR-EHR-CLUSTER.laboratory_test_analyte.v1",
                        property_path="items[at0024]/value/defining_code/code_string",
                        additional_condition="o/name/value = 'HbA1c'")[0]

if __name__ == "__main__":
    ehr_id = find_ehr_by_subject_id(PATIENT_PESEL)
    print(f"EHR id = {ehr_id}")

    last_updated_id = get_latest_ehr_composition_id(ehr_id, "eLaboratoryTestResult")
    print(f"Last updated eLaboratoryTestResult composition = {last_updated_id}")

    composition = get_composition_details(ehr_id, last_updated_id)
    save_composition_response(composition, "wyniki_badan.json")
    print("Saved composition for wyniki_badan.")

    specimen_collection_time = get_specimen_collection_time(ehr_id, last_updated_id)
    print(f"Specimen collection time = {specimen_collection_time}")

    glucose_result = get_glucose_result(ehr_id, last_updated_id)
    print(f"Glucose result = {glucose_result}")

    HbA1c_SNOMED_CT = get_HbA1c_SNOMED_CT(ehr_id, last_updated_id)
    print(f"HbA1c SNOMED CT code = {HbA1c_SNOMED_CT}")
