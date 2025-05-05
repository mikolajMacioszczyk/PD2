from openEHR_utils import get_property, get_top_level_property, find_ehr_by_subject_id, get_composition_details, get_latest_ehr_composition_id, save_composition_response

PATIENT_PESEL = 80010112349

def get_doctor_name(ehr_id, composition_id):
    return get_top_level_property(ehr_id, 
                        composition_id,
                        property_path="c/composer/name AS composer_name")[0]

def get_pressure_measurement_result(ehr_id, composition_id):
    result = get_property(ehr_id, 
                        composition_id,
                        archetype_type="OBSERVATION",
                        archetype_value="openEHR-EHR-OBSERVATION.intraocular_pressure.v0",
                        property_path="data[at0001]/events[at0002]/data[at0003]/items[at0042]/value")[0]
    return f"{result['magnitude']} {result['units']}"

def get_device_part_number(ehr_id, composition_id):
    return get_property(ehr_id, 
                        composition_id,
                        archetype_type="CLUSTER",
                        archetype_value="openEHR-EHR-CLUSTER.device_details.v1",
                        property_path="items[at0007]/value/value")[0]

if __name__ == "__main__":
    ehr_id = find_ehr_by_subject_id(PATIENT_PESEL)
    print(f"EHR id = {ehr_id}")

    last_updated_id = get_latest_ehr_composition_id(ehr_id, "Intraocular_pressure_study")
    print(f"Last updated Intraocular_pressure_study composition = {last_updated_id}")

    composition = get_composition_details(ehr_id, last_updated_id)
    save_composition_response(composition, "pomiar.json")
    print("Saved composition for pomiar.")

    doctor_name = get_doctor_name(ehr_id, last_updated_id)
    print(f"Doctor name = {doctor_name}")

    pressure_measurement_result = get_pressure_measurement_result(ehr_id, last_updated_id)
    print(f"Pressure measurement result = {pressure_measurement_result}")

    device_part_number = get_device_part_number(ehr_id, last_updated_id)
    print(f"Device part number = {device_part_number}")