from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.organization import Organization
from fhir.resources.condition import Condition
from fhir.resources.allergyintolerance import AllergyIntolerance
from fhir.resources.servicerequest import ServiceRequest

from fhir_utils import post_resource, create_or_get_by_identifier, load_fhir_resource

MEDICAL_DOCUMENT_TYPE = "skierowanie"
default_patient_file = "patient.json"
default_practitioner_file = "practitioner.json"
default_organization_file = "organization.json"
default_condition_file = "condition.json"
default_allergy_intolerance_file = "allergy_intolerance.json"
default_service_request_file = "service_request.json"

def upload_skierowanie_full(patient_file = default_patient_file, 
                            practitioner_file = default_practitioner_file,
                            organization_file = default_organization_file,
                            condition_file = default_condition_file,
                            allergy_intolerance_file = default_allergy_intolerance_file,
                            service_request_file = default_service_request_file):
    # Load resources
    patient = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, patient_file, Patient)
    practitioner = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, practitioner_file, Practitioner)
    organization = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, organization_file, Organization)
    condition = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, condition_file, Condition)
    allergy_intolerance = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, allergy_intolerance_file, AllergyIntolerance)
    service_request = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, service_request_file, ServiceRequest)

    # Add resources to the server
    patient_id = create_or_get_by_identifier(patient, patient.identifier[0].system)
    print("Patient ID:", patient_id)

    practitioner_id = create_or_get_by_identifier(practitioner, practitioner.identifier[0].system)
    print("Practitioner ID:", practitioner_id)

    organization_id = post_resource(organization)
    print("Organization ID:", organization_id)

    condition.subject.reference = f"Patient/{patient_id}"
    condition_id = post_resource(condition)
    print("Condition ID:", condition_id)

    allergy_intolerance.patient.reference = f"Patient/{patient_id}"
    allergy_intolerance_id = post_resource(allergy_intolerance)
    print("Allergy Intolerance ID:", allergy_intolerance_id)

    service_request.subject.reference = f"Patient/{patient_id}"
    service_request.requester.reference = f"Practitioner/{practitioner_id}"
    service_request.location[0].reference.reference = f"Organization/{organization_id}"
    service_request_id = post_resource(service_request)
    print("Service Request ID:", service_request_id)

if __name__ == "__main__":
    upload_skierowanie_full()
