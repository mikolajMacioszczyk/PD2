from fhir_utils import get_latest_resource_id_by_patient, get_patient_id_by_pesel, get_resource, save_batch_response, send_batch_request

PATIENT_PESEL = 80010112349

def create_get_full_pomiar_batch_bundle(observation_id):
    return {
        "resourceType": "Bundle",
        "type": "batch",
        "entry": [
            {
                "request": {
                    "method": "GET",
                    "url": (
                        f"Observation"
                        f"?_id={observation_id}"
                        f"&_include=Observation:subject"
                        f"&_include=Observation:device"
                        f"&_include=Observation:encounter"
                        f"&_include=Observation:performer"
                        f"&_include:iterate=Device:definition"
                    )
                }
            },
        ]
    }

def get_doctor_name(observation_id):
    resource_bundle = get_resource("Observation", observation_id, include="Observation:performer", elements="performer")
    doctor_name = resource_bundle["entry"][1]["resource"]["name"][0]
    return f"{doctor_name['prefix'][0]} {doctor_name['given'][0]} {doctor_name['family']}"

def get_pressure_measurement_result(observation_id):
    resource_bundle = get_resource("Observation", observation_id, elements="valueQuantity")
    valueQuantity = resource_bundle["entry"][0]["resource"]["valueQuantity"]
    return f"{valueQuantity['value']} {valueQuantity["unit"]}"

def get_device_part_number(observation_id):
    resource_bundle = get_resource("Observation", observation_id, include="Observation:device", elements="device")
    return resource_bundle["entry"][1]["resource"]["serialNumber"]

if __name__ == "__main__":
    patient_id = get_patient_id_by_pesel(PATIENT_PESEL)
    print(f"Patient id = {patient_id}")

    last_updated_resource_id = get_latest_resource_id_by_patient("Observation", "subject", patient_id)
    print(f"Last updated Observation = {last_updated_resource_id}")

    batch_bundle = create_get_full_pomiar_batch_bundle(last_updated_resource_id)
    batch_response = send_batch_request(batch_bundle)
    
    save_batch_response(batch_response, "pomiar.json")
    print("Saved bundle for pomiar.")

    doctor_name = get_doctor_name(last_updated_resource_id)
    print(f"Doctor name = {doctor_name}")

    pressure_measurement_result = get_pressure_measurement_result(last_updated_resource_id)
    print(f"Pressure measurement result = {pressure_measurement_result}")

    device_part_number = get_device_part_number(last_updated_resource_id)
    print(f"Device part number = {device_part_number}")
