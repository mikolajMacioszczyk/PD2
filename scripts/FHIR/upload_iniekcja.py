from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.medication import Medication

from fhir_utils import get_bundle, post_resource, create_or_get_by_identifier, load_fhir_resource
from file_output_fhir import save_to_output_file

MEDICAL_DOCUMENT_TYPE = "iniekcja"
default_patient_file = "patient.json"
default_practitioner_file = "practitioner.json"
default_medication_file = "medication.json"

def upload_iniekcja_full(patient_file = default_patient_file, 
                            practitioner_file = default_practitioner_file,
                            medication_file = default_medication_file):
    # Load resources
    patient = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, patient_file, Patient)
    practitioner = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, practitioner_file, Practitioner)
    medication = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, medication_file, Medication)

    # Add resources to the server
    patient_id = create_or_get_by_identifier(patient, patient.identifier[0].system)
    print("Patient ID:", patient_id)

    practitioner_id = create_or_get_by_identifier(practitioner, practitioner.identifier[0].system)
    print("Practitioner ID:", practitioner_id)

    medication_id = post_resource(medication)
    print("Medication ID:", medication_id)

    # TODO: Organization - bayer connected to medication
    # TODO: BodyStructure
    # TODO: ServiceRequest
    # TODO: MedicationAdministration
    # TODO: AllergyIntolerance
    # TODO: Check if nothing missing
    # TODO: Get and save

if __name__ == "__main__":
    upload_iniekcja_full()
