from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.location import Location
from fhir.resources.specimen import Specimen
from fhir.resources.observation import Observation
from fhir.resources.diagnosticreport import DiagnosticReport
from fhir.resources.servicerequest import ServiceRequest

from fhir_utils import post_resource, create_or_get_by_identifier, load_fhir_resource

default_patient_file = "patient.json"
default_practitioner_file = "practitioner.json"
default_location_file = "location.json"
default_specimen_morphology_file = "specimen-morphology.json"
default_specimen_smear_file = "specimen-smear.json"
default_service_request_file = "service-request.json"

def upload_wyniki_badan_full(patient_file = default_patient_file, 
                            practitioner_file = default_practitioner_file,
                            location_file = default_location_file,
                            specimen_morphology_file = default_specimen_morphology_file,
                            specimen_smear_file = default_specimen_smear_file,
                            service_request_file = default_service_request_file):
    
    patient = load_fhir_resource(patient_file, Patient)
    practitioner = load_fhir_resource(practitioner_file, Practitioner)
    location = load_fhir_resource(location_file, Location)
    specimen_morphology = load_fhir_resource(specimen_morphology_file, Specimen)
    specimen_smear = load_fhir_resource(specimen_smear_file, Specimen)
    service_request = load_fhir_resource(service_request_file, ServiceRequest)

    patient_id = create_or_get_by_identifier(patient, patient.identifier[0].system)
    print("Patient ID:", patient_id)

    practitioner_id = create_or_get_by_identifier(practitioner, practitioner.identifier[0].system)
    print("Practitioner ID:", practitioner_id)

    location_id = post_resource(location)
    print("Location ID:", location_id)

    specimen_morphology.subject.reference = f"Patient/{patient_id}"
    specimen_morphology_id = post_resource(specimen_morphology)
    print("Specimen Morphology ID:", specimen_morphology_id)

    specimen_smear.subject.reference = f"Patient/{patient_id}"
    specimen_smear_id = post_resource(specimen_smear)
    print("Specimen Smear ID:", specimen_smear_id)

    # service_request_id = post_resource(service_request)
    # print("Service Request ID:", service_request_id)

if __name__ == "__main__":
    upload_wyniki_badan_full()

# TODO: Observations
# TODO: Service Request
# TODO: service request code
# TODO: Diagnostic Report (check if extension exists)