from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.organization import Organization
from fhir.resources.device import Device
from fhir.resources.observation import Observation
from fhir.resources.encounter import Encounter

from fhir_utils import get_bundle, post_resource, create_or_get_by_identifier, load_fhir_resource
from file_output_fhir import save_to_output_file

MEDICAL_DOCUMENT_TYPE = "pomiar"
default_patient_file = "patient.json"
default_practitioner_file = "practitioner.json"
default_organization_file = "organization.json"
default_device_file = "device.json"
default_observation_file = "observation.json"
default_encounter_file = "encounter.json"

def upload_wyniki_badan_full(patient_file = default_patient_file, 
                            practitioner_file = default_practitioner_file,
                            organization_file = default_organization_file,
                            device_file = default_device_file,
                            observation_file = default_observation_file,
                            encounter_file = default_encounter_file):
    # Load resources
    patient = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, patient_file, Patient)
    practitioner = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, practitioner_file, Practitioner)
    organization = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, organization_file, Organization)
    device = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, device_file, Device)
    observation = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, observation_file, Observation)
    encounter = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, encounter_file, Encounter)

    # Add resources to the server
    patient_id = create_or_get_by_identifier(patient, patient.identifier[0].system)
    print("Patient ID:", patient_id)

    practitioner_id = create_or_get_by_identifier(practitioner, practitioner.identifier[0].system)
    print("Practitioner ID:", practitioner_id)

    organization_id = post_resource(organization)
    print("Organization ID:", organization_id)

    # TODO: Device properties
    device.owner.reference = f"Organization/{organization_id}"
    device_id = post_resource(device)
    print("Device ID:", device_id)

    encounter.subject.reference = f"Patient/{patient_id}"
    encounter.serviceProvider.reference = f"Organization/{organization_id}"
    encounter_id = post_resource(encounter)
    print("Encounter ID:", encounter_id)

    observation.subject.reference = f"Patient/{patient_id}"
    observation.device.reference = f"Device/{device_id}"
    observation.performer[0].reference = f"Practitioner/{practitioner_id}"
    observation.encounter.reference = f"Encounter/{encounter_id}"
    observation_id = post_resource(observation)
    print("Observation ID:", observation_id)

    resource_bundle = get_bundle(Observation.__name__, observation_id, [
        { 'name': Organization.__name__, 'id': organization_id }
    ])
    if resource_bundle:
        file_name = f"bundle-{MEDICAL_DOCUMENT_TYPE}-JSON-{observation_id}.json"
        save_to_output_file(resource_bundle, MEDICAL_DOCUMENT_TYPE, file_name)
        print(f"Saved bundle to {file_name}")

if __name__ == "__main__":
    upload_wyniki_badan_full()
