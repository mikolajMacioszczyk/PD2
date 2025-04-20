from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.medication import Medication
from fhir.resources.allergyintolerance import AllergyIntolerance
from fhir.resources.medicationadministration import MedicationAdministration
from fhir.resources.careplan import CarePlan

from fhir_utils import get_bundle, post_resource, create_or_get_by_identifier, load_fhir_resource
from file_output_fhir import save_to_output_file

MEDICAL_DOCUMENT_TYPE = "iniekcja"
default_patient_file = "patient.json"
default_practitioner_file = "practitioner.json"
default_medication_file = "medication.json"
default_allergy_intolerance_file = "allergy_intolerance.json"
default_care_plan_file = "care_plan.json"
default_medication_administration_file = "medication_administration.json"

def upload_iniekcja_full(patient_file = default_patient_file, 
                            practitioner_file = default_practitioner_file,
                            medication_file = default_medication_file,
                            allergy_intolerance_file = default_allergy_intolerance_file,
                            care_plan_file = default_care_plan_file,
                            medication_administration_file = default_medication_administration_file):
    # Load resources
    patient = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, patient_file, Patient)
    practitioner = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, practitioner_file, Practitioner)
    medication = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, medication_file, Medication)
    allergy_intolerance = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, allergy_intolerance_file, AllergyIntolerance)
    medication_administration = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, medication_administration_file, MedicationAdministration)
    care_plan = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, care_plan_file, CarePlan)

    # Add resources to the server
    patient_id = create_or_get_by_identifier(patient, patient.identifier[0].system)
    print("Patient ID:", patient_id)

    practitioner_id = create_or_get_by_identifier(practitioner, practitioner.identifier[0].system)
    print("Practitioner ID:", practitioner_id)

    allergy_intolerance.patient.reference = f"Patient/{patient_id}"
    allergy_intolerance_id = post_resource(allergy_intolerance)
    print("Allergy Intolerance ID:", allergy_intolerance_id)

    medication_id = post_resource(medication)
    print("Medication ID:", medication_id)

    care_plan.subject.reference = f"Patient/{patient_id}"
    care_plan.contributor[0].reference = f"Practitioner/{practitioner_id}"
    care_plan_id = post_resource(care_plan)
    print("Care Plan ID:", care_plan_id)

    medication_administration.basedOn[0].reference = f"CarePlan/{care_plan_id}"
    medication_administration.medication.reference.reference = f"Medication/{medication_id}"
    medication_administration.subject.reference = f"Patient/{patient_id}"
    medication_administration.performer[0].actor.reference.reference = f"Practitioner/{practitioner_id}"
    medication_administration_id = post_resource(medication_administration)
    print("Medication Administration ID:", medication_administration_id)

    # TODO: Organization - bayer connected to medication
    # TODO: Check if nothing missing
    # TODO: Get and save

if __name__ == "__main__":
    upload_iniekcja_full()
