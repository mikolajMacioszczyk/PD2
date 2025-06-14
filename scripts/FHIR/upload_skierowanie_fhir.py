from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.organization import Organization
from fhir.resources.condition import Condition
from fhir.resources.allergyintolerance import AllergyIntolerance
from fhir.resources.servicerequest import ServiceRequest
from fhir_conf import VERBOSE

from fhir_utils import get_bundle, post_resource, create_or_get_by_identifier, load_fhir_resource
from file_output_fhir import save_to_output_file

MEDICAL_DOCUMENT_TYPE = "skierowanie"
default_patient_file = "patient.json"
default_practitioner_file = "practitioner.json"
default_organization_file = "organization.json"
default_condition_influenza_file = "condition_influenza.json"
default_condition_anemia_file = "condition_anemia.json"
default_allergy_intolerance_file = "allergy_intolerance.json"
default_service_request_file = "service_request.json"

def upload_skierowanie_full(pesel,
                            save = True,
                            patient_file = default_patient_file, 
                            practitioner_file = default_practitioner_file,
                            organization_file = default_organization_file,
                            condition_influenza_file = default_condition_influenza_file,
                            condition_anemia_file = default_condition_anemia_file,
                            allergy_intolerance_file = default_allergy_intolerance_file,
                            service_request_file = default_service_request_file,
                            verbose = VERBOSE):
    # Load resources
    patient = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, patient_file, Patient)
    patient.identifier[0].value = str(pesel)
    practitioner = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, practitioner_file, Practitioner)
    organization = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, organization_file, Organization)
    condition_influenza = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, condition_influenza_file, Condition)
    condition_anemia = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, condition_anemia_file, Condition)
    allergy_intolerance = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, allergy_intolerance_file, AllergyIntolerance)
    service_request = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, service_request_file, ServiceRequest)

    # Add resources to the server
    patient_id = create_or_get_by_identifier(patient, patient.identifier[0].system)
    if verbose:
        print("Patient ID:", patient_id)

    practitioner_id = create_or_get_by_identifier(practitioner, practitioner.identifier[0].system)
    if verbose:
        print("Practitioner ID:", practitioner_id)

    organization_id = post_resource(organization)
    if verbose:
        print("Organization ID:", organization_id)

    condition_influenza.subject.reference = f"Patient/{patient_id}"
    condition_influenza_id = post_resource(condition_influenza)
    if verbose:
        print("Condition Influenza ID:", condition_influenza_id)

    condition_anemia.subject.reference = f"Patient/{patient_id}"
    condition_anemia_id = post_resource(condition_anemia)
    if verbose:
        print("Condition anemia ID:", condition_anemia_id)

    allergy_intolerance.patient.reference = f"Patient/{patient_id}"
    allergy_intolerance_id = post_resource(allergy_intolerance)
    if verbose:
        print("Allergy Intolerance ID:", allergy_intolerance_id)

    service_request.subject.reference = f"Patient/{patient_id}"
    service_request.requester.reference = f"Practitioner/{practitioner_id}"
    service_request.reason[0].reference.reference = f"Condition/{condition_influenza_id}"
    service_request.reason[1].reference.reference = f"Condition/{condition_anemia_id}"
    service_request.location[0].reference.reference = f"Organization/{organization_id}"
    service_request.supportingInfo[0].reference.reference = f"AllergyIntolerance/{allergy_intolerance_id}"
    service_request_id = post_resource(service_request)
    if verbose:
        print("Service Request ID:", service_request_id)

    if save:
        resource_bundle = get_bundle(ServiceRequest.__name__, service_request_id, [
            { "name": Condition.__name__, "id": condition_influenza_id },
            { "name": Condition.__name__, "id": condition_anemia_id },
            { "name": AllergyIntolerance.__name__, "id": allergy_intolerance_id },
            { "name": Organization.__name__, "id": organization_id }
        ])
        if resource_bundle:
            file_name = f"bundle-{MEDICAL_DOCUMENT_TYPE}-JSON-{service_request_id}.json"
            save_to_output_file(resource_bundle, MEDICAL_DOCUMENT_TYPE, file_name)
            if verbose:
                print(f"Saved bundle to {file_name}")

    return (patient_id, service_request_id)

if __name__ == "__main__":
    upload_skierowanie_full(pesel=80010112346, verbose=True)
