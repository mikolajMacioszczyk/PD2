from fhir_utils import get_latest_resource_id_by_patient, get_patient_id_by_pesel, get_resource, get_resource_by_ref, save_batch_response, send_batch_request

PATIENT_PESEL = 80010112346

def create_get_full_skierowanie_batch_bundle(patient_id, service_request_id):
    return {
        "resourceType": "Bundle",
        "type": "batch",
        "entry": [
            {
                "request": {
                    "method": "GET",
                    "url": (
                        f"ServiceRequest"
                        f"?_id={service_request_id}"
                        f"&_include=ServiceRequest:subject"
                        f"&_include=ServiceRequest:requester"
                    )
                }
            },
            {
                "request": {
                    "method": "GET",
                    "url": (
                        f"Condition"
                        f"?subject=Patient/{patient_id}"
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

def get_test_name(service_request_id):
    resource_bundle = get_resource("ServiceRequest", service_request_id, elements="code")
    return resource_bundle["entry"][0]["resource"]["code"]["concept"]["text"]

def get_health_problem(service_request_id, patient_id):
    resource_bundle = send_batch_request({
        "resourceType": "Bundle",
        "type": "batch",
        "entry": [
            {
                "request": {
                    "method": "GET",
                    "url": (
                        f"ServiceRequest"
                        f"?_id={service_request_id}"
                    )
                }
            },
            {
                "request": {
                    "method": "GET",
                    "url": (
                        f"Condition"
                        f"?subject=Patient/{patient_id}"
                    )
                }
            }
        ]
    })
    service_request = resource_bundle["entry"][0]["resource"]["entry"][0]["resource"]
    condition_references = [item["reference"]["reference"].split("/")[1] for item in service_request["reason"]]

    conditions = [item['resource']['code']['text']
                  for item in resource_bundle["entry"][1]["resource"]["entry"]
                  if item["resource"]["id"] in condition_references]

    return conditions

def get_alergen(service_request_id, patient_id):
    resource_bundle = send_batch_request({
        "resourceType": "Bundle",
        "type": "batch",
        "entry": [
            {
                "request": {
                    "method": "GET",
                    "url": (
                        f"ServiceRequest"
                        f"?_id={service_request_id}"
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
    service_request = resource_bundle["entry"][0]["resource"]["entry"][0]["resource"]
    supporting_info_references = [item["reference"]["reference"].split("/")[1] 
                                  for item in service_request["supportingInfo"]
                                  if item["reference"]["reference"].split("/")[0] == "AllergyIntolerance"]
    
    allergy_intolerances = [item['resource']["code"]["text"]
                  for item in resource_bundle["entry"][1]["resource"]["entry"]
                  if item["resource"]["id"] in supporting_info_references]

    return allergy_intolerances

if __name__ == "__main__":
    patient_id = get_patient_id_by_pesel(PATIENT_PESEL)
    print(f"Patient id = {patient_id}")

    last_updated_resource_id = get_latest_resource_id_by_patient("ServiceRequest", "subject", patient_id)
    print(f"Last updated ServiceRequest = {last_updated_resource_id}")

    batch_bundle = create_get_full_skierowanie_batch_bundle(patient_id, last_updated_resource_id)
    batch_response = send_batch_request(batch_bundle)
    
    save_batch_response(batch_response, "skierowanie.json")
    print("Saved bundle for skierowanie.")

    test_name = get_test_name(last_updated_resource_id)
    print(f"Test name = {test_name}")

    health_problem = get_health_problem(last_updated_resource_id, patient_id)
    print(f"Health problem = {health_problem}")

    alergen = get_alergen(last_updated_resource_id, patient_id)
    print(f"Alergen = {alergen}")
