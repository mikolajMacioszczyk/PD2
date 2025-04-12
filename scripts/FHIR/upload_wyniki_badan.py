from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.organization import Organization
from fhir.resources.specimen import Specimen
from fhir.resources.observation import Observation
from fhir.resources.diagnosticreport import DiagnosticReport

from fhir_utils import get_resource, post_resource, create_or_get_by_identifier, load_fhir_resource
from file_output_fhir import save_to_output_file

MEDICAL_DOCUMENT_TYPE = "wyniki_badan"
default_patient_file = "patient.json"
default_practitioner_file = "practitioner.json"
default_organization_file = "organization.json"
default_specimen_file = "specimen.json"
default_observation_glucose_file = "observation-glucose.json"
default_observation_hba1c_file = "observation-hba1c.json"
default_diagnostic_report_file = "diagnostic-report.json"

def upload_wyniki_badan_full(patient_file = default_patient_file, 
                            practitioner_file = default_practitioner_file,
                            organization_file = default_organization_file,
                            specimen_file = default_specimen_file,
                            observation_glucose_file = default_observation_glucose_file,
                            observation_hba1c_file = default_observation_hba1c_file,
                            diagnostic_report_file = default_diagnostic_report_file):
    # Load resources
    patient = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, patient_file, Patient)
    practitioner = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, practitioner_file, Practitioner)
    organization = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, organization_file, Organization)
    specimen = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, specimen_file, Specimen)
    observation_glucose = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, observation_glucose_file, Observation)
    observation_hba1c = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, observation_hba1c_file, Observation)
    diagnostic_report = load_fhir_resource(MEDICAL_DOCUMENT_TYPE, diagnostic_report_file, DiagnosticReport)

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

    observation_hba1c.subject.reference = f"Patient/{patient_id}"
    observation_hba1c.specimen.reference = f"Specimen/{specimen_id}"
    observation_hba1c_id = post_resource(observation_hba1c)
    print("Observation HbA1c ID:", observation_hba1c_id)

    diagnostic_report.subject.reference = f"Patient/{patient_id}"
    diagnostic_report.performer[0].reference = f"Organization/{organization_id}"
    diagnostic_report.resultsInterpreter[0].reference = f"Practitioner/{practitioner_id}"
    diagnostic_report.specimen[0].reference = f"Specimen/{specimen_id}"
    diagnostic_report.result[0].reference = f"Observation/{observation_glucose_id}"
    diagnostic_report.result[1].reference = f"Observation/{observation_hba1c_id}"
    diagnostic_report_id = post_resource(diagnostic_report)
    print("Diagnostic Report ID:", diagnostic_report_id)

    includes = [
        "DiagnosticReport:subject", 
        "DiagnosticReport:results-interpreter",
        "DiagnosticReport:specimen",
        "DiagnosticReport:result"
        ]
    resource_bundle = get_resource(DiagnosticReport.__name__, diagnostic_report_id, includes)
    if resource_bundle:
        file_name = f"bundle-{MEDICAL_DOCUMENT_TYPE}-JSON-{diagnostic_report_id}.json"
        save_to_output_file(resource_bundle, MEDICAL_DOCUMENT_TYPE, file_name)
        print(f"Saved bundle to {file_name}")

if __name__ == "__main__":
    upload_wyniki_badan_full()
