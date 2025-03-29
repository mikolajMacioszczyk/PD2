import requests
import json

FHIR_SERVER = "http://localhost:8080/fhir"

patient_file = "patient.json"
practitioner_file = "practitioner.json"
service_request_file = "service-request.json"

with open(patient_file, 'r', encoding='utf-8') as patient_json_data:
    patient = json.load(patient_json_data)

with open(practitioner_file, 'r', encoding='utf-8') as practitioner_json_data:
    practitioner = json.load(practitioner_json_data)

with open(service_request_file, 'r', encoding='utf-8') as service_request_json_data:
    service_request = json.load(service_request_json_data)

def post_resource(resource):
    url = f"{FHIR_SERVER}/{resource['resourceType']}"
    response = requests.post(url, headers={"Content-Type": "application/fhir+json"}, data=json.dumps(resource))
    print(f"{resource['resourceType']} status: {response.status_code}")
    print(response.text)

post_resource(patient)
post_resource(practitioner)
# Condition
# medical statement
post_resource(service_request)

# TODO: Lepszy skrypt (sprawdza czy istnieje, pobiera id z tworzonych i istniejących)
# TODO: docker volume
# TODO: ujednolicony coding
