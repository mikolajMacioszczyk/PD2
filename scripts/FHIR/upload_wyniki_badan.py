from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.organization import Organization
from fhir.resources.specimen import Specimen
from fhir.resources.observation import Observation
from fhir.resources.diagnosticreport import DiagnosticReport

from fhir_utils import post_resource, create_or_get_by_identifier, load_fhir_resource

MEDICAL_DOCUMENT_TYPE = "wyniki_badan"
default_patient_file = "patient.json"
default_practitioner_file = "practitioner.json"
default_organization_file = "organization.json"
default_specimen_file = "specimen.json"
default_observation_glucose_file = "observation-glucose.json"

def upload_wyniki_badan_full(patient_file = default_patient_file, 
                            practitioner_file = default_practitioner_file,
                            organization_file = default_organization_file,
                            specimen_file = default_specimen_file,
                            observation_glucose_file = default_observation_glucose_file):
    # Load resources
    patient = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, patient_file, Patient)
    practitioner = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, practitioner_file, Practitioner)
    organization = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, organization_file, Organization)
    specimen = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, specimen_file, Specimen)
    observation_glucose = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, observation_glucose_file, Observation)

    # Add resources to the server
    patient_id = create_or_get_by_identifier(patient, patient.identifier[0].system)
    print("Patient ID:", patient_id)

    practitioner_id = create_or_get_by_identifier(practitioner, practitioner.identifier[0].system)
    print("Practitioner ID:", practitioner_id)

    organization_id = post_resource(organization)
    print("Organization ID:", organization_id)

    specimen_id = post_resource(specimen)
    print("Specimen ID:", specimen_id)

    observation_glucose.subject.reference = f"Patient/{patient_id}"
    observation_glucose.specimen.reference = f"Specimen/{specimen_id}"
    observation_glucose_id = post_resource(observation_glucose)
    print("Observation Glucose ID:", observation_glucose_id)

    # TODO: observation hba1c
    # TODO: diagnostic report

if __name__ == "__main__":
    upload_wyniki_badan_full()
