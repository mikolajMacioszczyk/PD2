import requests
import json

from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.condition import Condition
from fhir.resources.medicationstatement import MedicationStatement
from fhir.resources.servicerequest import ServiceRequest

FHIR_SERVER = "http://localhost:8080/fhir"

patient_file = "patient.json"
practitioner_file = "practitioner.json"
condition_parasthesia_file = "condition-parasthesia.json"
medication_statement_magnesium_file = "medication-statement-magnesium.json"
service_request_file = "service-request.json"

def load_fhir_resource(file_path, resource_class):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return resource_class.model_validate(data)

patient = load_fhir_resource(patient_file, Patient)
practitioner = load_fhir_resource(practitioner_file, Practitioner)
condition_parasthesia = load_fhir_resource(condition_parasthesia_file, Condition)
medication_statement_magnesium = load_fhir_resource(medication_statement_magnesium_file, MedicationStatement)
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
        print(f"Request failed with status code {response.status_code}: {response.text}")
        return None

patient_id = post_resource(patient)
print("Patient ID:", patient_id)

practitioner_id = post_resource(practitioner)
print("Practitioner ID:", practitioner_id)

condition_parasthesia.subject.reference = f"Patient/{patient_id}"
condition_parasthesia_id = post_resource(condition_parasthesia)
print("Condition Parasthesia ID:", condition_parasthesia_id)

medication_statement_magnesium.subject.reference = f"Patient/{patient_id}"
medication_statement_magnesium_id = post_resource(medication_statement_magnesium)
print("Medication Statement Magnesium ID:", medication_statement_magnesium_id)

# post_resource(service_request)

# TODO: docker volume
# TODO: ujednolicony coding
# TODO: posprawdzaj kody
# TODO: Lepszy skrypt (wykorzystuje metody)
# TODO: duplikaty:
# "identifier": [
#   {
#     "system": "http://hospital.example.org/patients",
#     "value": "12345"
#   }