from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.condition import Condition
from fhir.resources.medicationstatement import MedicationStatement
from fhir.resources.servicerequest import ServiceRequest

from fhir_utils import post_resource, create_or_get_by_identifier, load_fhir_resource

default_patient_file = "patient.json"
default_practitioner_file = "practitioner.json"
default_condition_parasthesia_file = "condition-parasthesia.json"
default_medication_statement_magnesium_file = "medication-statement-magnesium.json"
default_service_request_file = "service-request.json"

def upload_skierowanie_full(patient_file = default_patient_file, 
                            practitioner_file = default_practitioner_file,
                            condition_parasthesia_file = default_condition_parasthesia_file, 
                            medication_statement_magnesium_file = default_medication_statement_magnesium_file, 
                            service_request_file = default_service_request_file):
    patient = load_fhir_resource(patient_file, Patient)
    practitioner = load_fhir_resource(practitioner_file, Practitioner)
    condition_parasthesia = load_fhir_resource(condition_parasthesia_file, Condition)
    medication_statement_magnesium = load_fhir_resource(medication_statement_magnesium_file, MedicationStatement)
    service_request = load_fhir_resource(service_request_file, ServiceRequest)

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

if __name__ == "__main__":
    upload_skierowanie_full()

# TODO: przemyśl: concept a reference