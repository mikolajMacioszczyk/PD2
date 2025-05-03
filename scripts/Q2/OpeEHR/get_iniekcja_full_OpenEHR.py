from openEHR_utils import find_ehr_by_subject_id, get_composition_details, get_latest_ehr_composition_id, save_composition_response

PATIENT_PESEL = 80010112350

if __name__ == "__main__":
    ehr_id = find_ehr_by_subject_id(PATIENT_PESEL)
    print(f"EHR id = {ehr_id}")

    last_updated_id = get_latest_ehr_composition_id(ehr_id)
    print(f"Last updated composition = {last_updated_id}")

    composition = get_composition_details(ehr_id, last_updated_id)
    save_composition_response(composition, "iniekcja.json")
    print("Saved composition for iniekcja.")
    pass
