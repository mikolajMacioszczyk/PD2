from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.medication import Medication
from fhir.resources.allergyintolerance import AllergyIntolerance
from fhir.resources.medicationadministration import MedicationAdministration
from fhir.resources.goal import Goal
from fhir.resources.careplan import CarePlan

from fhir_utils import get_bundle, post_resource, create_or_get_by_identifier, load_fhir_resource
from file_output_fhir import save_to_output_file
from fhir_conf import VERBOSE

MEDICAL_DOCUMENT_TYPE = "iniekcja"
default_patient_file = "patient.json"
default_practitioner_file = "practitioner.json"
default_medication_file = "medication.json"
default_allergy_intolerance_file = "allergy_intolerance.json"
default_goal_file = "goal.json"
default_care_plan_file = "care_plan.json"
default_medication_administration_file = "medication_administration.json"

def upload_iniekcja_full(pesel,
                        save = True,
                        patient_file = default_patient_file, 
                        practitioner_file = default_practitioner_file,
                        medication_file = default_medication_file,
                        allergy_intolerance_file = default_allergy_intolerance_file,
                        goal_file = default_goal_file,
                        care_plan_file = default_care_plan_file,
                        medication_administration_file = default_medication_administration_file,
                        verbose = VERBOSE):
    # Load resources
    patient = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, patient_file, Patient)
    patient.identifier[0].value = str(pesel)
    practitioner = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, practitioner_file, Practitioner)
    medication = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, medication_file, Medication)
    allergy_intolerance = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, allergy_intolerance_file, AllergyIntolerance)
    goal = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, goal_file, Goal)
    care_plan = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, care_plan_file, CarePlan)
    medication_administration = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, medication_administration_file, MedicationAdministration)

    # Add resources to the server
    patient_id = create_or_get_by_identifier(patient, patient.identifier[0].system)
    if verbose:
        print("Patient ID:", patient_id)

    practitioner_id = create_or_get_by_identifier(practitioner, practitioner.identifier[0].system)
    if verbose:
        print("Practitioner ID:", practitioner_id)

    allergy_intolerance.patient.reference = f"Patient/{patient_id}"
    allergy_intolerance_id = post_resource(allergy_intolerance)
    if verbose:
        print("Allergy Intolerance ID:", allergy_intolerance_id)

    medication_id = post_resource(medication)
    if verbose:
        print("Medication ID:", medication_id)

    goal.subject.reference = f"Patient/{patient_id}"
    goal_id = post_resource(goal)
    if verbose:
        print("Goal ID:", goal_id)

    care_plan.subject.reference = f"Patient/{patient_id}"
    care_plan.contributor[0].reference = f"Practitioner/{practitioner_id}"
    care_plan.supportingInfo[0].reference = f"AllergyIntolerance/{allergy_intolerance_id}"
    care_plan.goal[0].reference = f"Goal/{goal_id}"
    care_plan_id = post_resource(care_plan)
    if verbose:
        print("Care Plan ID:", care_plan_id)

    medication_administration.basedOn[0].reference = f"CarePlan/{care_plan_id}"
    medication_administration.medication.reference.reference = f"Medication/{medication_id}"
    medication_administration.subject.reference = f"Patient/{patient_id}"
    medication_administration.performer[0].actor.reference.reference = f"Practitioner/{practitioner_id}"
    medication_administration_id = post_resource(medication_administration)
    if verbose:
        print("Medication Administration ID:", medication_administration_id)

    if save:
        resource_bundle = get_bundle(MedicationAdministration.__name__, medication_administration_id, [
            { "name": AllergyIntolerance.__name__, "id": allergy_intolerance_id },
            { "name": CarePlan.__name__, "id": care_plan_id },
            { "name": Goal.__name__, "id": goal_id },
        ])
        if resource_bundle:
            file_name = f"bundle-{MEDICAL_DOCUMENT_TYPE}-JSON-{medication_administration_id}.json"
            save_to_output_file(resource_bundle, MEDICAL_DOCUMENT_TYPE, file_name)
            if verbose:
                print(f"Saved bundle to {file_name}")

    return (patient_id, medication_administration_id)

if __name__ == "__main__":
    upload_iniekcja_full(pesel=80010112350, verbose=True)
