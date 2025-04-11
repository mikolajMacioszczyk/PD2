from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.organization import Organization
from fhir.resources.medication import Medication
from fhir_utils import post_resource, create_or_get_by_identifier, load_fhir_resource

MEDICAL_DOCUMENT_TYPE = "recepta"
default_patient_file = "patient.json"
default_practitioner_file = "practitioner.json"
default_organization_file = "organization.json"
default_medication_file = "medication.json"

def upload_recepta_full(patient_file = default_patient_file, 
                        practitioner_file = default_practitioner_file,
                        organization_file = default_organization_file,
                        medication_file = default_medication_file):
    # Load resources
    patient = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, patient_file, Patient)
    practitioner = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, practitioner_file, Practitioner)
    organization = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, organization_file, Organization)
    medication = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, medication_file, Medication)

    # Add resources to the server
    patient_id = create_or_get_by_identifier(patient, patient.identifier[0].system)
    print("Patient ID:", patient_id)

    practitioner_id = create_or_get_by_identifier(practitioner, practitioner.identifier[0].system)
    print("Practitioner ID:", practitioner_id)

    practitioner_id = create_or_get_by_identifier(practitioner, practitioner.identifier[0].system)
    print("Practitioner ID:", practitioner_id)

    organization_id = post_resource(organization)
    print("Organization ID:", organization_id)

    medication_id = post_resource(medication)
    print("Medication ID:", medication_id)

    # TODO: Medication request

if __name__ == "__main__":
    upload_recepta_full()