# run me with: locust -f .\performance_tests_openehr.py  --csv stats/performance_tests_openehr
# run me with: python3 -m locust -f ./performance_tests_openehr.py --headless -u 10 -r 1 --csv stats/performance_tests_openehr --run-time 1h
import os
import sys
from locust import HttpUser, between, task
import urllib
import urllib3
import json
from OpenEHR.openehr_conf import OPENEHR_SERVER
from utils import *
from queue import Queue
import logging

## ignore HTTPS errors in console
logging.getLogger("urllib3.connection").setLevel(logging.ERROR)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

OpenEHR_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'OpenEHR'))
sys.path.append(OpenEHR_path)

from upload_recepta_openehr import upload_recepta_full as upload_recepta_openehr
from upload_skierowanie_openehr import upload_skierowanie_full as upload_skierowanie_openehr

specify_logging_level(LogLevel.INFO)
USERS_PER_DOCUMENT_COUNT = 1
DOCUMENT_TYPES = ["recepta", "skierowanie", "pomiar", "plan_leczenia", "wyniki_badan"]

all_pesels = generate_unique_11_digit_numbers(USERS_PER_DOCUMENT_COUNT * len(DOCUMENT_TYPES))
pesels_queue = Queue()
for pesel_from_queue in all_pesels:
    pesels_queue.put(pesel_from_queue)

# TODO: Upload templates

ehr_headers = {
    'Content-Type': 'application/json',
    "Accept": "application/json",
    'Prefer': 'return=representation'
}

BASE_URL = f"{OPENEHR_SERVER}ehrbase/rest/openehr/v1"

class Patient(HttpUser):
    abstract = True

    def _get_property(self, request_name, ehr_id, composition_id, archetype_type, archetype_value, property_path, additional_condition = None, verbose=False):
        identifier = composition_id.split(":")[0]
        aql_query = f"""
        SELECT 
            o/{property_path}
        FROM 
            EHR e
        CONTAINS COMPOSITION c
        CONTAINS {archetype_type} o[{archetype_value}]
        WHERE 
            e/ehr_id/value = '{ehr_id}'
            AND c/uid/value = '{identifier}'
        LIMIT 1
        """

        if additional_condition:
            aql_query = f"""
            SELECT 
                o/{property_path}
            FROM 
                EHR e
            CONTAINS COMPOSITION c
            CONTAINS {archetype_type} o[{archetype_value}]
            WHERE 
                e/ehr_id/value = '{ehr_id}'
                AND c/uid/value = '{identifier}'
                AND {additional_condition}
            LIMIT 1
            """

        response = self.client.post(
            f"{BASE_URL}/query/aql",
            headers=ehr_headers,
            json={"q": aql_query},
            name=request_name
        )

        self._handle_response(response, request_name)
    
    def _handle_response(self, response, request_name):
        if response.status_code == 200:
            log(f"Got {request_name} for patient with pesel {self.pesel} and ehr id {self.ehr_id}", LogLevel.DEBUG)
        else:
            log(f"Failed to get {request_name} for patient with pesel {self.pesel} and ehr id {self.ehr_id}", LogLevel.WARNING)
    
class PatientWithRecepta(Patient):
    fixed_count = USERS_PER_DOCUMENT_COUNT
    host = OPENEHR_SERVER

    def on_start(self):
        try:
            self.pesel = pesels_queue.get_nowait()
            (ehr_id, composition_id) = upload_recepta_openehr(self.pesel, save=False, verbose=False)
            self.ehr_id = ehr_id
            self.composition_id = composition_id
            self.encoded_identifier = urllib.parse.quote_plus(composition_id)
            log(f"Created recepta composition for patient with pesel: {self.pesel} and ehr id: {self.ehr_id} in OpenEHR", LogLevel.INFO)
        except:
            raise Exception("No more PESELS available!")
        
    @task(1)
    def get_whole_data(self):
        request_url = f"{BASE_URL}/ehr/{self.ehr_id}/composition/{self.encoded_identifier}"
        recepta_response = self.client.get(request_url, name="get_recepta_full", headers=ehr_headers, verify=False)
        if recepta_response.status_code == 200:
            log(f"Got recepta full data patient with pesel {self.pesel} and ehr id {self.ehr_id}", LogLevel.DEBUG)
        else:
            log(f"Failed to get recepta full data patient with pesel: {self.pesel} and ehr id: {self.ehr_id}", LogLevel.WARNING)
            log(recepta_response.content, LogLevel.WARNING)

    @task(1)
    def get_pharmaceutical_form(self):
        self._get_property("get_pharmaceutical_form", 
                            self.ehr_id, 
                            self.composition_id,
                            archetype_type="CLUSTER",
                            archetype_value="openEHR-EHR-CLUSTER.medication_substance.v0",
                            property_path="items[at0133]/value/value")
    
    @task(1)
    def get_frequency(self):
        self._get_property("get_frequency", 
                            self.ehr_id, 
                            self.composition_id,
                            archetype_type="CLUSTER",
                            archetype_value="openEHR-EHR-CLUSTER.timing_daily.v0",
                            property_path="items[at0003]/value")

    @task(1)
    def get_validity_period(self):
        self._get_property("get_validity_period", 
                            self.ehr_id, 
                            self.composition_id,
                            archetype_type="CLUSTER",
                            archetype_value="openEHR-EHR-CLUSTER.medication_authorisation.v0",
                            property_path="items[at0072]/value/value")

class PatientWithSkierowanie(Patient):
    fixed_count = USERS_PER_DOCUMENT_COUNT
    host = OPENEHR_SERVER

    def on_start(self):
        try:
            self.pesel = pesels_queue.get_nowait()
            (ehr_id, composition_id) = upload_skierowanie_openehr(self.pesel, save=False, verbose=False)
            self.ehr_id = ehr_id
            self.composition_id = composition_id
            self.encoded_identifier = urllib.parse.quote_plus(composition_id)
            log(f"Created skierowanie composition for patient with pesel: {self.pesel} and ehr id: {self.ehr_id} in OpenEHR", LogLevel.INFO)
        except:
            raise Exception("No more PESELS available!")
        
    @task(1)
    def get_whole_data(self):
        request_url = f"{BASE_URL}/ehr/{self.ehr_id}/composition/{self.encoded_identifier}"
        skierowanie_response = self.client.get(request_url, name="get_skierowanie_full", headers=ehr_headers, verify=False)
        if skierowanie_response.status_code == 200:
            log(f"Got skierowanie full data patient with pesel {self.pesel} and ehr id {self.ehr_id}", LogLevel.DEBUG)
        else:
            log(f"Failed to get skierowanie full data patient with pesel: {self.pesel} and ehr id: {self.ehr_id}", LogLevel.WARNING)
            log(skierowanie_response.content, LogLevel.WARNING)

    @task(1)
    def get_test_name(self):
        self._get_property("get_test_name", 
                            self.ehr_id, 
                            self.composition_id,
                            archetype_type="OBSERVATION",
                            archetype_value="openEHR-EHR-OBSERVATION.lab_test.v1",
                            property_path="data[at0001]/events[at0002]/data[at0003]/items[at0005]/value/value")

    @task(1)
    def get_health_problem(self):
        self._get_property("get_health_problem", 
                            self.ehr_id, 
                            self.composition_id,
                            archetype_type="EVALUATION",
                            archetype_value="openEHR-EHR-EVALUATION.problem.v1",
                            property_path="data[at0001]/items[at0002]/value/value")

    @task(1)
    def get_alergen(self):
        self._get_property("get_alergen", 
                            self.ehr_id, 
                            self.composition_id,
                            archetype_type="EVALUATION",
                            archetype_value="openEHR-EHR-EVALUATION.adverse.v1",
                            property_path="data[at0002]/items[at0003]/value/value")
    
# class PatientWithPomiar(Patient):
#     fixed_count = USERS_PER_DOCUMENT_COUNT
#     host = FHIR_SERVER

#     def on_start(self):
#         try:
#             self.pesel = pesels_queue.get_nowait()
#             (patient_id, observation_id) = upload_pomiar_fhir(self.pesel, save=False, verbose=False)
#             self.patient_id = patient_id
#             self.observation_id = observation_id
#             log(f"Created pomiar resources for patient with pesel: {self.pesel} and id: {self.patient_id} in FHIR", LogLevel.INFO)
#         except:
#             raise Exception("No more PESELS available!")
        
#     @task(1)
#     def get_whole_data(self):
#         batch_bundle = create_get_full_pomiar_batch_bundle(self.observation_id)
#         headers = {"Content-Type": "application/fhir+json"}
#         recepta_response = self.client.post(FHIR_SERVER, name="get_pomiar_full", headers=headers, data=json.dumps(batch_bundle), verify=False)
#         if recepta_response.status_code == 200:
#             log(f"Got pomiar full data patient with pesel {self.pesel} and id {self.patient_id}", LogLevel.DEBUG)
#         else:
#             log(f"Failed to get pomiar full data patient with pesel: {self.pesel} and id: {self.patient_id}", LogLevel.WARNING)

#     @task(1)
#     def get_doctor_name(self):
#         self._get_resource("get_doctor_name", "Observation", self.observation_id, include="Observation:performer", elements="performer")

#     @task(1)
#     def get_pressure_measurement_result(self):
#         self._get_resource("get_pressure_measurement_result", "Observation", self.observation_id, elements="valueQuantity")

#     @task(1)
#     def get_device_part_number(self):
#         self._get_resource("get_device_part_number", "Observation", self.observation_id, include="Observation:device", elements="device")

# class PatientWithPlanLeczenia(Patient):
#     fixed_count = USERS_PER_DOCUMENT_COUNT
#     host = FHIR_SERVER

#     def on_start(self):
#         try:
#             self.pesel = pesels_queue.get_nowait()
#             (patient_id, medication_administration_id) = upload_iniekcja_fhir(self.pesel, save=False, verbose=False)
#             self.patient_id = patient_id
#             self.medication_administration_id = medication_administration_id
#             log(f"Created medication administration resources for patient with pesel: {self.pesel} and id: {self.patient_id} in FHIR", LogLevel.INFO)
#         except:
#             raise Exception("No more PESELS available!")
        
#     @task(1)
#     def get_whole_data(self):
#         batch_bundle = create_get_full_iniekcja_batch_bundle(self.patient_id, self.medication_administration_id)
#         headers = {"Content-Type": "application/fhir+json"}
#         recepta_response = self.client.post(FHIR_SERVER, name="get_plan_leczenia_full", headers=headers, data=json.dumps(batch_bundle), verify=False)
#         if recepta_response.status_code == 200:
#             log(f"Got plan leczenia full data patient with pesel {self.pesel} and id {self.patient_id}", LogLevel.DEBUG)
#         else:
#             log(f"Failed to get plan leczenia full data patient with pesel: {self.pesel} and id: {self.patient_id}", LogLevel.WARNING)

#     @task(1)
#     def get_medication_name(self):
#         self._get_resource("get_medication_name", "MedicationAdministration", self.medication_administration_id, include="MedicationAdministration:medication", elements="medication")

#     @task(1)
#     def get_dose_value_and_unit(self):
#         self._get_resource("get_dose_value_and_unit", "MedicationAdministration", self.medication_administration_id, elements="dosage")

#     @task(1)
#     def get_allergy_reaction(self):
#         request_name = "get_allergy_reaction"
#         get_allergy_reaction_batch_bundle = create_get_allergy_reaction_batch_bundle(self.patient_id, self.medication_administration_id)
#         headers = {"Content-Type": "application/fhir+json"}
#         response = self.client.post(FHIR_SERVER, name=request_name, headers=headers, data=json.dumps(get_allergy_reaction_batch_bundle), verify=False)
        
#         self._handle_response(response, request_name)

# class PatientWithWynikiBadan(Patient):
#     fixed_count = USERS_PER_DOCUMENT_COUNT
#     host = FHIR_SERVER

#     def on_start(self):
#         try:
#             self.pesel = pesels_queue.get_nowait()
#             (patient_id, diagnostic_report_id) = upload_wyniki_badan_fhir(self.pesel, save=False, verbose=False)
#             self.patient_id = patient_id
#             self.diagnostic_report_id = diagnostic_report_id
#             log(f"Created diagnostic report resources for patient with pesel: {self.pesel} and id: {self.patient_id} in FHIR", LogLevel.INFO)
#         except:
#             raise Exception("No more PESELS available!")
        
#     @task(1)
#     def get_whole_data(self):
#         batch_bundle = create_get_full_wyniki_badan_batch_bundle(self.diagnostic_report_id)
#         headers = {"Content-Type": "application/fhir+json"}
#         recepta_response = self.client.post(FHIR_SERVER, name="get_wyniki_badan_full", headers=headers, data=json.dumps(batch_bundle), verify=False)
#         if recepta_response.status_code == 200:
#             log(f"Got wyniki badan full data patient with pesel {self.pesel} and id {self.patient_id}", LogLevel.DEBUG)
#         else:
#             log(f"Failed to get wyniki badan full data patient with pesel: {self.pesel} and id: {self.patient_id}", LogLevel.WARNING)

#     @task(1)
#     def get_specimen_collection_time(self):
#         self._get_resource("get_specimen_collection_time", "DiagnosticReport", self.diagnostic_report_id, include="DiagnosticReport:specimen", elements="specimen")

#     @task(1)
#     def get_glucose_result(self):
#         self._get_resource("get_glucose_result", "DiagnosticReport", self.diagnostic_report_id, include="DiagnosticReport:result", elements="result")

#     @task(1)
#     def get_HbA1c_SNOMED_CT(self):
#         self._get_resource("get_HbA1c_SNOMED_CT", "DiagnosticReport", self.diagnostic_report_id, include="DiagnosticReport:result", elements="specimen")
