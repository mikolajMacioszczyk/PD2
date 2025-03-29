import requests
import json

from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.servicerequest import ServiceRequest

FHIR_SERVER = "http://localhost:8080/fhir"

patient_file = "patient.json"
practitioner_file = "practitioner.json"
service_request_file = "service-request.json"

def load_fhir_resource(file_path, resource_class):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return resource_class.model_validate(data)

patient = load_fhir_resource("patient.json", Patient)
practitioner = load_fhir_resource("practitioner.json", Practitioner)
# service_request = load_fhir_resource("service-request.json", ServiceRequest)

def post_resource(resource):
    resource_type = resource.__class__.__name__
    url = f"{FHIR_SERVER}/{resource_type}"
    response = requests.post(
        url,
        headers={"Content-Type": "application/fhir+json"},
        data=resource.json()
    )
    
    print(f"{resource_type} status: {response.status_code}")

    if response.status_code == 201:
        location = response.headers.get("Location", "")
        resource_id = location.split("/")[-1] if location else None
        return resource_id
    else:
        return None

patient_id = post_resource(patient)
print("Patient ID:", patient_id)
post_resource(practitioner)
practitioner_id = post_resource(practitioner)
print("Practitioner ID:", practitioner_id)
# Condition
# medical statement
# post_resource(service_request)

# TODO: Lepszy skrypt (sprawdza czy istnieje, pobiera id z tworzonych i istniejących)
# TODO: docker volume
# TODO: ujednolicony coding
# TODO: duplikaty:
# "identifier": [
#   {
#     "system": "http://hospital.example.org/patients",
#     "value": "12345"
#   }