# run me with: locust -f .\performance_tests_fhir.py  --csv stats/performance_tests_fhir
# run me with: python3 -m locust -f ./performance_tests_fhir.py --headless -u 10 -r 1 --csv stats/performance_tests_fhir --run-time 1h
import os
import sys
from locust import HttpUser, between, task
import urllib3
import json
from FHIR.queries_definitions import *
from FHIR.fhir_conf import FHIR_SERVER
from utils import *
from queue import Queue
import logging

## ignore HTTPS errors in console
logging.getLogger("urllib3.connection").setLevel(logging.ERROR)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FHIR_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'FHIR'))
sys.path.append(FHIR_path)

from upload_recepta_fhir import upload_recepta_full as upload_recepta_fhir
from upload_skierowanie_fhir import upload_skierowanie_full as upload_skierowanie_fhir
from upload_pomiar import upload_pomiar_full as upload_pomiar_fhir
from upload_iniekcja import upload_iniekcja_full as upload_iniekcja_fhir
from upload_wyniki_badan import upload_wyniki_badan_full as upload_wyniki_badan_fhir

specify_logging_level(LogLevel.WARNING)
USERS_PER_DOCUMENT_COUNT = 1
DOCUMENT_TYPES = ["recepta", "skierowanie", "pomiar", "plan_leczenia", "wyniki_badan"]

all_pesels = generate_unique_11_digit_numbers(USERS_PER_DOCUMENT_COUNT * len(DOCUMENT_TYPES))
pesels_queue = Queue()
for pesel_from_queue in all_pesels:
    pesels_queue.put(pesel_from_queue)

class Patient(HttpUser):
    abstract = True
    
    def _get_resource(self, request_name, resource_type, resource_id, include=None, elements=None):
        url = f"{FHIR_SERVER}/{resource_type}"

        params = {
            "_id": resource_id
        }

        if include:
            params["_include"] = include

        if elements:
            params["_elements"] = elements

        response = self.client.get(url, params=params, name=request_name)
        self._handle_response(response, request_name)

    def _handle_response(self, response, request_name):
        if response.status_code == 200:
            log(f"Got {request_name} for patient with pesel {self.pesel} and id {self.patient_id}", LogLevel.DEBUG)
        else:
            log(f"Failed to get {request_name} for patient with pesel {self.pesel} and id {self.patient_id}", LogLevel.WARNING)

class PatientWithRecepta(Patient):
    fixed_count = USERS_PER_DOCUMENT_COUNT
    host = FHIR_SERVER

    def on_start(self):
        try:
            self.pesel = pesels_queue.get_nowait()
            (patient_id, medication_request_id) = upload_recepta_fhir(self.pesel, save=False, verbose=False)
            self.patient_id = patient_id
            self.medication_request_id = medication_request_id
            log(f"Created recepta resources for patient with pesel: {self.pesel} and id: {self.patient_id} in FHIR", LogLevel.INFO)
        except:
            raise Exception("No more PESELS available!")
        
    @task(1)
    def get_whole_data(self):
        batch_bundle = create_get_full_recepta_batch_bundle(self.medication_request_id)
        headers = {"Content-Type": "application/fhir+json"}
        recepta_response = self.client.post(FHIR_SERVER, name="get_recepta_full", headers=headers, data=json.dumps(batch_bundle), verify=False)
        if recepta_response.status_code == 200:
            log(f"Got recepta full data patient with pesel {self.pesel} and id {self.patient_id}", LogLevel.DEBUG)
        else:
            log(f"Failed to get recepta full data patient with pesel: {self.pesel} and id: {self.patient_id}", LogLevel.WARNING)

    @task(1)
    def get_pharmaceutical_form(self):
        self._get_resource("get_pharmaceutical_form", "MedicationRequest", self.medication_request_id, include="MedicationRequest:medication", elements="medication")
    
    @task(1)
    def get_frequency(self):
        self._get_resource("get_frequency", "MedicationRequest", self.medication_request_id, elements="dosageInstruction")

    @task(1)
    def get_validity_period(self):
        self._get_resource("get_validity_period", "MedicationRequest", self.medication_request_id, elements="dispenseRequest")

class PatientWithSkierowanie(Patient):
    fixed_count = USERS_PER_DOCUMENT_COUNT
    host = FHIR_SERVER

    def on_start(self):
        try:
            self.pesel = pesels_queue.get_nowait()
            (patient_id, service_request_id) = upload_skierowanie_fhir(self.pesel, save=False, verbose=False)
            self.patient_id = patient_id
            self.service_request_id = service_request_id
            log(f"Created skierowanie resources for patient with pesel: {self.pesel} and id: {self.patient_id} in FHIR", LogLevel.INFO)
        except:
            raise Exception("No more PESELS available!")
        
    @task(1)
    def get_whole_data(self):
        batch_bundle = create_get_full_skierowanie_batch_bundle(self.patient_id, self.service_request_id)
        headers = {"Content-Type": "application/fhir+json"}
        recepta_response = self.client.post(FHIR_SERVER, name="get_skierowanie_full", headers=headers, data=json.dumps(batch_bundle), verify=False)
        if recepta_response.status_code == 200:
            log(f"Got skierowanie full data patient with pesel {self.pesel} and id {self.patient_id}", LogLevel.DEBUG)
        else:
            log(f"Failed to get skierowanie full data patient with pesel: {self.pesel} and id: {self.patient_id}", LogLevel.WARNING)

    @task(1)
    def get_test_name(self):
        self._get_resource("get_test_name", "ServiceRequest", self.service_request_id, elements="code")

    @task(1)
    def get_health_problem(self):
        request_name = "get_health_problem"
        get_health_problem_batch_bundle = create_get_health_problem_batch_bundle(self.patient_id, self.service_request_id)
        headers = {"Content-Type": "application/fhir+json"}
        response = self.client.post(FHIR_SERVER, name=request_name, headers=headers, data=json.dumps(get_health_problem_batch_bundle), verify=False)
        
        self._handle_response(response, request_name)

    @task(1)
    def get_alergen(self):
        request_name = "get_alergen"
        get_alergen_batch_bundle = create_get_alergen_batch_bundle(self.patient_id, self.service_request_id)
        headers = {"Content-Type": "application/fhir+json"}
        response = self.client.post(FHIR_SERVER, name=request_name, headers=headers, data=json.dumps(get_alergen_batch_bundle), verify=False)
        
        self._handle_response(response, request_name)

class PatientWithPomiar(Patient):
    fixed_count = USERS_PER_DOCUMENT_COUNT
    host = FHIR_SERVER

    def on_start(self):
        try:
            self.pesel = pesels_queue.get_nowait()
            (patient_id, observation_id) = upload_pomiar_fhir(self.pesel, save=False, verbose=False)
            self.patient_id = patient_id
            self.observation_id = observation_id
            log(f"Created pomiar resources for patient with pesel: {self.pesel} and id: {self.patient_id} in FHIR", LogLevel.INFO)
        except:
            raise Exception("No more PESELS available!")
        
    @task(1)
    def get_whole_data(self):
        batch_bundle = create_get_full_pomiar_batch_bundle(self.observation_id)
        headers = {"Content-Type": "application/fhir+json"}
        recepta_response = self.client.post(FHIR_SERVER, name="get_pomiar_full", headers=headers, data=json.dumps(batch_bundle), verify=False)
        if recepta_response.status_code == 200:
            log(f"Got pomiar full data patient with pesel {self.pesel} and id {self.patient_id}", LogLevel.DEBUG)
        else:
            log(f"Failed to get pomiar full data patient with pesel: {self.pesel} and id: {self.patient_id}", LogLevel.WARNING)

    @task(1)
    def get_doctor_name(self):
        self._get_resource("get_doctor_name", "Observation", self.observation_id, include="Observation:performer", elements="performer")

    @task(1)
    def get_pressure_measurement_result(self):
        self._get_resource("get_pressure_measurement_result", "Observation", self.observation_id, elements="valueQuantity")

    @task(1)
    def get_device_part_number(self):
        self._get_resource("get_device_part_number", "Observation", self.observation_id, include="Observation:device", elements="device")

class PatientWithPlanLeczenia(Patient):
    fixed_count = USERS_PER_DOCUMENT_COUNT
    host = FHIR_SERVER

    def on_start(self):
        try:
            self.pesel = pesels_queue.get_nowait()
            (patient_id, medication_administration_id) = upload_iniekcja_fhir(self.pesel, save=False, verbose=False)
            self.patient_id = patient_id
            self.medication_administration_id = medication_administration_id
            log(f"Created medication administration resources for patient with pesel: {self.pesel} and id: {self.patient_id} in FHIR", LogLevel.INFO)
        except:
            raise Exception("No more PESELS available!")
        
    @task(1)
    def get_whole_data(self):
        batch_bundle = create_get_full_iniekcja_batch_bundle(self.patient_id, self.medication_administration_id)
        headers = {"Content-Type": "application/fhir+json"}
        recepta_response = self.client.post(FHIR_SERVER, name="get_plan_leczenia_full", headers=headers, data=json.dumps(batch_bundle), verify=False)
        if recepta_response.status_code == 200:
            log(f"Got plan leczenia full data patient with pesel {self.pesel} and id {self.patient_id}", LogLevel.DEBUG)
        else:
            log(f"Failed to get plan leczenia full data patient with pesel: {self.pesel} and id: {self.patient_id}", LogLevel.WARNING)

    @task(1)
    def get_medication_name(self):
        self._get_resource("get_medication_name", "MedicationAdministration", self.medication_administration_id, include="MedicationAdministration:medication", elements="medication")

    @task(1)
    def get_dose_value_and_unit(self):
        self._get_resource("get_dose_value_and_unit", "MedicationAdministration", self.medication_administration_id, elements="dosage")

    @task(1)
    def get_allergy_reaction(self):
        request_name = "get_allergy_reaction"
        get_allergy_reaction_batch_bundle = create_get_allergy_reaction_batch_bundle(self.patient_id, self.medication_administration_id)
        headers = {"Content-Type": "application/fhir+json"}
        response = self.client.post(FHIR_SERVER, name=request_name, headers=headers, data=json.dumps(get_allergy_reaction_batch_bundle), verify=False)
        
        self._handle_response(response, request_name)

class PatientWithWynikiBadan(Patient):
    fixed_count = USERS_PER_DOCUMENT_COUNT
    host = FHIR_SERVER

    def on_start(self):
        try:
            self.pesel = pesels_queue.get_nowait()
            (patient_id, diagnostic_report_id) = upload_wyniki_badan_fhir(self.pesel, save=False, verbose=False)
            self.patient_id = patient_id
            self.diagnostic_report_id = diagnostic_report_id
            log(f"Created diagnostic report resources for patient with pesel: {self.pesel} and id: {self.patient_id} in FHIR", LogLevel.INFO)
        except:
            raise Exception("No more PESELS available!")
        
    @task(1)
    def get_whole_data(self):
        batch_bundle = create_get_full_wyniki_badan_batch_bundle(self.diagnostic_report_id)
        headers = {"Content-Type": "application/fhir+json"}
        recepta_response = self.client.post(FHIR_SERVER, name="get_wyniki_badan_full", headers=headers, data=json.dumps(batch_bundle), verify=False)
        if recepta_response.status_code == 200:
            log(f"Got wyniki badan full data patient with pesel {self.pesel} and id {self.patient_id}", LogLevel.DEBUG)
        else:
            log(f"Failed to get wyniki badan full data patient with pesel: {self.pesel} and id: {self.patient_id}", LogLevel.WARNING)

    @task(1)
    def get_specimen_collection_time(self):
        self._get_resource("get_specimen_collection_time", "DiagnosticReport", self.diagnostic_report_id, include="DiagnosticReport:specimen", elements="specimen")

    @task(1)
    def get_glucose_result(self):
        self._get_resource("get_glucose_result", "DiagnosticReport", self.diagnostic_report_id, include="DiagnosticReport:result", elements="result")

    @task(1)
    def get_HbA1c_SNOMED_CT(self):
        self._get_resource("get_HbA1c_SNOMED_CT", "DiagnosticReport", self.diagnostic_report_id, include="DiagnosticReport:result", elements="specimen")
