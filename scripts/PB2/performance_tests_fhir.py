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
USERS_PER_DOCUMENT_COUNT = 2
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
            (patient_id, observation_id) = upload_skierowanie_fhir(self.pesel, save=False, verbose=False)
            self.patient_id = patient_id
            self.observation_id = observation_id
            log(f"Created observation resources for patient with pesel: {self.pesel} and id: {self.patient_id} in FHIR", LogLevel.INFO)
        except:
            raise Exception("No more PESELS available!")
        
    @task(1)
    def get_whole_data(self):
        batch_bundle = create_get_full_pomiar_batch_bundle(self.observation_id)
        headers = {"Content-Type": "application/fhir+json"}
        recepta_response = self.client.post(FHIR_SERVER, name="get_observation_full", headers=headers, data=json.dumps(batch_bundle), verify=False)
        if recepta_response.status_code == 200:
            log(f"Got observation full data patient with pesel {self.pesel} and id {self.patient_id}", LogLevel.DEBUG)
        else:
            log(f"Failed to get observation full data patient with pesel: {self.pesel} and id: {self.patient_id}", LogLevel.WARNING)

    @task(1)
    def get_doctor_name(self):
        self._get_resource("get_doctor_name", "Observation", self.observation_id, include="Observation:performer", elements="performer")

    @task(1)
    def get_pressure_measurement_result(self):
        self._get_resource("get_pressure_measurement_result", "Observation", self.observation_id, elements="valueQuantity")

    @task(1)
    def get_device_part_number(self):
        self._get_resource("get_device_part_number", "Observation", self.observation_id, include="Observation:device", elements="device")


# class OrganizationUser(HttpUser):
#     wait_time = between(1, 5)
#     host = BASKET_HOST

#     def on_start(self) -> None:
#         global counter
#         counter = counter + 1
#         log(f'Counter = {counter}', LogLevel.DEBUG)
#         self.user = UserTestData(counter, '')
#         self.create_new_basket()
#         return super().on_start()
    
#     # POST
#     @task(1)
#     def create_new_basket_task(self):
#         self.create_new_basket()

#     # GET
#     @task(5)
#     def get_basket_task(self):
#         self.get_basket()

#     # PUT
#     @task(10)
#     def add_product_task(self):
#         self.add_product()

#     def create_new_basket(self):
#         headers = {
#             "Content-Type": "application/json" 
#         }

#         create_basket_response = self.client.post("/Basket/guest", name="create basket", headers=headers, data=json.dumps({}), verify=False)

#         if create_basket_response.status_code == 200:
#             response_json = create_basket_response.json()
#             self.user.basket_id = response_json.get('id')
#             log(f"Setting basket id for user {self.user.basket_id}", LogLevel.DEBUG)
#         else:
#             log(f"User {self.user.id} failed to create basket -> status code {create_basket_response.status_code}.", LogLevel.WARNING)
#             log(create_basket_response.text, LogLevel.WARNING)

#     def get_basket(self):
#         headers = {
#             "Content-Type": "application/json" 
#         }

#         log(f"Getting basket {self.user.basket_id}", LogLevel.DEBUG)
#         get_basket_response = self.client.get(f"/Basket/{self.user.basket_id}", name="get basket", headers=headers, verify=False)

#         if get_basket_response.status_code == 200:
#             log(f"Got basket {self.user.basket_id} from basket for user {self.user.id}", LogLevel.DEBUG)
#         else:
#             log(f"User {self.user.id} failed to get basket with id {self.user.basket_id} -> status code {get_basket_response.status_code}.", LogLevel.WARNING)
#             log(get_basket_response.text, LogLevel.WARNING)

#     def add_product(self):
#         headers = {
#             "Content-Type": "application/json" 
#         }

#         product_id = self.get_random_product_id()
#         log(f"Adding product {product_id} to basket {self.user.basket_id}", LogLevel.DEBUG)
#         add_product_response = self.client.put(f"/Basket/{self.user.basket_id}/product/{product_id}/add", name="add product to basket", headers=headers, data=json.dumps({}), verify=False)

#         if add_product_response.status_code == 200:
#             log(f"Added product {product_id} to basket for user {self.user.id}", LogLevel.DEBUG)
#         else:
#             log(f"User {self.user.id} failed to add product {product_id} to basket {self.user.basket_id} -> status code {add_product_response.status_code}.", LogLevel.WARNING)
#             log(add_product_response.text, LogLevel.WARNING)

#     def get_random_product_id(self):
#         return random.choice(catalog_product_ids)
