from fhir_utils import get_latest_resource_id_by_patient, get_patient_id_by_pesel, get_resource, save_batch_response, send_batch_request
from recepta_queries_definitions import create_get_full_recepta_batch_bundle

PATIENT_PESEL = 80010112345

def get_pharmaceutical_form(medication_request_id):
    resource_bundle = get_resource("MedicationRequest", medication_request_id, include="MedicationRequest:medication", elements="medication")
    return resource_bundle["entry"][1]["resource"]["doseForm"]["text"]

def get_frequency(medication_request_id):
    resource_bundle = get_resource("MedicationRequest", medication_request_id, elements="dosageInstruction")
    repeat = resource_bundle["entry"][0]["resource"]["dosageInstruction"][0]["timing"]["repeat"]
    return f"{repeat['frequency']}/{repeat['durationUnit']}"

def get_validity_period(medication_request_id):
    resource_bundle = get_resource("MedicationRequest", medication_request_id, elements="dispenseRequest")
    return resource_bundle["entry"][0]["resource"]["dispenseRequest"]["validityPeriod"]["end"]

if __name__ == "__main__":
    patient_id = get_patient_id_by_pesel(PATIENT_PESEL)
    print(f"Patient id = {patient_id}")

    last_updated_resource_id = get_latest_resource_id_by_patient("MedicationRequest", "subject", patient_id)
    print(f"Last updated MedicationRequest = {last_updated_resource_id}")

    batch_bundle = create_get_full_recepta_batch_bundle(last_updated_resource_id)
    batch_response = send_batch_request(batch_bundle)
    
    save_batch_response(batch_response, "recepta.json")
    print("Saved bundle for recepta.")

    pharmaceutical_form = get_pharmaceutical_form(last_updated_resource_id)
    print(f"Pharmaceutical form = {pharmaceutical_form}")

    frequency = get_frequency(last_updated_resource_id)
    print(f"Frequency = {frequency}")

    validity_period = get_validity_period(last_updated_resource_id)
    print(f"Validity period = {validity_period}")
