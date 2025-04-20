from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.medication import Medication
from fhir.resources.bodystructure import BodyStructure
from fhir.resources.allergyintolerance import AllergyIntolerance
from fhir.resources.medicationadministration import MedicationAdministration

from fhir_utils import get_bundle, post_resource, create_or_get_by_identifier, load_fhir_resource
from file_output_fhir import save_to_output_file

MEDICAL_DOCUMENT_TYPE = "iniekcja"
default_patient_file = "patient.json"
default_practitioner_file = "practitioner.json"
default_medication_file = "medication.json"
default_body_structure_file = "body_structure.json"
default_allergy_intolerance_file = "allergy_intolerance.json"
default_medication_administration_file = "medication_administration.json"

def upload_iniekcja_full(patient_file = default_patient_file, 
                            practitioner_file = default_practitioner_file,
                            medication_file = default_medication_file,
                            body_structure_file = default_body_structure_file,
                            allergy_intolerance_file = default_allergy_intolerance_file,
                            medication_administration_file = default_medication_administration_file):
    # Load resources
    patient = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, patient_file, Patient)
    practitioner = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, practitioner_file, Practitioner)
    medication = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, medication_file, Medication)
    body_structure = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, body_structure_file, BodyStructure)
    allergy_intolerance = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, allergy_intolerance_file, AllergyIntolerance)
    medication_administration = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, medication_administration_file, MedicationAdministration)

    # Add resources to the server
    patient_id = create_or_get_by_identifier(patient, patient.identifier[0].system)
    print("Patient ID:", patient_id)

    practitioner_id = create_or_get_by_identifier(practitioner, practitioner.identifier[0].system)
    print("Practitioner ID:", practitioner_id)

    body_structure.patient.reference = f"Patient/{patient_id}"
    body_structure_id = post_resource(body_structure)
    print("Body Structure ID:", body_structure_id)

    allergy_intolerance.patient.reference = f"Patient/{patient_id}"
    allergy_intolerance_id = post_resource(allergy_intolerance)
    print("Allergy Intolerance ID:", allergy_intolerance_id)

    medication_id = post_resource(medication)
    print("Medication ID:", medication_id)

    medication_administration.medication.reference.reference = f"Medication/{medication_id}"
    medication_administration.subject.reference = f"Patient/{patient_id}"
    medication_administration.performer[0].actor.reference.reference = f"Practitioner/{practitioner_id}"
    medication_administration_id = post_resource(medication_administration)
    print("Medication Administration ID:", medication_administration_id)

    # TODO: Organization - bayer connected to medication
    # TODO: ServiceRequest
    # TODO: Check if nothing missing
    # TODO: Get and save

if __name__ == "__main__":
    upload_iniekcja_full()
