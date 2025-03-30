import json

from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.condition import Condition
from fhir.resources.medicationstatement import MedicationStatement
from fhir.resources.servicerequest import ServiceRequest

from conf import FHIR_SERVER
from utils import post_resource, create_or_get_by_identifier

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
service_request = load_fhir_resource("service-request.json", ServiceRequest)

patient_id = create_or_get_by_identifier(patient, patient.identifier[0].system)
print("Patient ID:", patient_id)

practitioner_id = create_or_get_by_identifier(practitioner, practitioner.identifier[0].system)
print("Practitioner ID:", practitioner_id)

condition_parasthesia.subject.reference = f"Patient/{patient_id}"
condition_parasthesia_id = post_resource(condition_parasthesia)
print("Condition Parasthesia ID:", condition_parasthesia_id)

medication_statement_magnesium.subject.reference = f"Patient/{patient_id}"
medication_statement_magnesium_id = post_resource(medication_statement_magnesium)
print("Medication Statement Magnesium ID:", medication_statement_magnesium_id)

service_request.subject.reference = f"Patient/{patient_id}"
service_request.requester.reference = f"Practitioner/{practitioner_id}"
service_request.reason[1].reference.reference = f"Condition/{condition_parasthesia_id}"
service_request.supportingInfo[0].reference.reference = f"MedicationStatement/{medication_statement_magnesium_id}"

service_request_id = post_resource(service_request)
print("Service Request ID:", service_request_id)

# TODO: ujednolicony coding
# TODO: posprawdzaj kody
# TODO: przemyśl: concept a reference
# TODO: Lepszy skrypt (wykorzystuje metody)
