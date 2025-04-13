from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.organization import Organization
from fhir.resources.medication import Medication
from fhir.resources.medicationrequest import MedicationRequest
from fhir_utils import get_bundle, post_resource, create_or_get_by_identifier, load_fhir_resource
from file_output_fhir import save_to_output_file

MEDICAL_DOCUMENT_TYPE = "recepta"
default_patient_file = "patient.json"
default_practitioner_file = "practitioner.json"
default_organization_file = "organization.json"
default_medication_file = "medication.json"
default_medication_request_file = "medication_request.json"

def upload_recepta_full(patient_file = default_patient_file, 
                        practitioner_file = default_practitioner_file,
                        organization_file = default_organization_file,
                        medication_file = default_medication_file,
                        medication_request_file = default_medication_request_file):
    # Load resources
    patient = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, patient_file, Patient)
    practitioner = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, practitioner_file, Practitioner)
    organization = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, organization_file, Organization)
    medication = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, medication_file, Medication)
    medication_request = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, medication_request_file, MedicationRequest)

    # Add resources to the server
    patient_id = create_or_get_by_identifier(patient, patient.identifier[0].system)
    print("Patient ID:", patient_id)

    practitioner_id = create_or_get_by_identifier(practitioner, practitioner.identifier[0].system)
    print("Practitioner ID:", practitioner_id)

    organization_id = post_resource(organization)
    print("Organization ID:", organization_id)

    medication_id = post_resource(medication)
    print("Medication ID:", medication_id)

    medication_request.medication.reference.reference = f"Medication/{medication_id}"
    medication_request.subject.reference = f"Patient/{patient_id}"
    medication_request.informationSource[0].reference = f"Organization/{organization_id}"
    medication_request.requester.reference = f"Practitioner/{practitioner_id}"
    medication_request_id = post_resource(medication_request)
    print("Medication Request ID:", medication_request_id)

    resource_bundle = get_bundle(MedicationRequest.__name__, medication_request_id, [
        { 'name': Organization.__name__, 'id': organization_id }
    ])
    if resource_bundle:
        file_name = f"bundle-{MEDICAL_DOCUMENT_TYPE}-JSON-{medication_request_id}.json"
        save_to_output_file(resource_bundle, MEDICAL_DOCUMENT_TYPE, file_name)
        print(f"Saved bundle to {file_name}")

if __name__ == "__main__":
    upload_recepta_full()