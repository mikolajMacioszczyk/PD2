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
from upload_pomiar_openehr import upload_pomiar_full as upload_pomiar_openehr
from upload_iniekcja_openehr import upload_iniekcja_full as upload_plan_leczenia_openehr
from upload_wyniki_badan_openehr import upload_wyniki_badan_full as upload_wyniki_badan_openehr


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

    def _get_property(self, request_name, ehr_id, composition_id, archetype_type, archetype_value, property_path, additional_condition = None):
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

    def _get_top_level_property(self, request_name, ehr_id, composition_id, property_path):
        identifier = composition_id.split(":")[0]
        aql_query = f"""
        SELECT 
            {property_path}
        FROM 
            EHR e
            CONTAINS COMPOSITION c
        WHERE 
            e/ehr_id/value = '{ehr_id}'
            AND c/uid/value = '{identifier}'
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
        recepta_response = self.client.get(request_url, name="get_recepta_full_openehr", headers=ehr_headers, verify=False)
        if recepta_response.status_code == 200:
            log(f"Got recepta full data patient with pesel {self.pesel} and ehr id {self.ehr_id}", LogLevel.DEBUG)
        else:
            log(f"Failed to get recepta full data patient with pesel: {self.pesel} and ehr id: {self.ehr_id}", LogLevel.WARNING)
            log(recepta_response.content, LogLevel.WARNING)

    @task(1)
    def get_pharmaceutical_form(self):
        self._get_property("get_pharmaceutical_form_openehr", 
                            self.ehr_id, 
                            self.composition_id,
                            archetype_type="CLUSTER",
                            archetype_value="openEHR-EHR-CLUSTER.medication_substance.v0",
                            property_path="items[at0133]/value/value")
    
    @task(1)
    def get_frequency(self):
        self._get_property("get_frequency_openehr", 
                            self.ehr_id, 
                            self.composition_id,
                            archetype_type="CLUSTER",
                            archetype_value="openEHR-EHR-CLUSTER.timing_daily.v0",
                            property_path="items[at0003]/value")

    @task(1)
    def get_validity_period(self):
        self._get_property("get_validity_period_openehr", 
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
        skierowanie_response = self.client.get(request_url, name="get_skierowanie_full_openehr", headers=ehr_headers, verify=False)
        if skierowanie_response.status_code == 200:
            log(f"Got skierowanie full data patient with pesel {self.pesel} and ehr id {self.ehr_id}", LogLevel.DEBUG)
        else:
            log(f"Failed to get skierowanie full data patient with pesel: {self.pesel} and ehr id: {self.ehr_id}", LogLevel.WARNING)
            log(skierowanie_response.content, LogLevel.WARNING)

    @task(1)
    def get_test_name(self):
        self._get_property("get_test_name_openehr", 
                            self.ehr_id, 
                            self.composition_id,
                            archetype_type="OBSERVATION",
                            archetype_value="openEHR-EHR-OBSERVATION.lab_test.v1",
                            property_path="data[at0001]/events[at0002]/data[at0003]/items[at0005]/value/value")

    @task(1)
    def get_health_problem(self):
        self._get_property("get_health_problem_openehr", 
                            self.ehr_id, 
                            self.composition_id,
                            archetype_type="EVALUATION",
                            archetype_value="openEHR-EHR-EVALUATION.problem.v1",
                            property_path="data[at0001]/items[at0002]/value/value")

    @task(1)
    def get_alergen(self):
        self._get_property("get_alergen_openehr", 
                            self.ehr_id, 
                            self.composition_id,
                            archetype_type="EVALUATION",
                            archetype_value="openEHR-EHR-EVALUATION.adverse.v1",
                            property_path="data[at0002]/items[at0003]/value/value")
        
class PatientWithPomiar(Patient):
    fixed_count = USERS_PER_DOCUMENT_COUNT
    host = OPENEHR_SERVER

    def on_start(self):
        try:
            self.pesel = pesels_queue.get_nowait()
            (ehr_id, composition_id) = upload_pomiar_openehr(self.pesel, save=False, verbose=False)
            self.ehr_id = ehr_id
            self.composition_id = composition_id
            self.encoded_identifier = urllib.parse.quote_plus(composition_id)
            log(f"Created pomiar composition for patient with pesel: {self.pesel} and ehr id: {self.ehr_id} in OpenEHR", LogLevel.INFO)
        except:
            raise Exception("No more PESELS available!")
        
    @task(1)
    def get_whole_data(self):
        request_url = f"{BASE_URL}/ehr/{self.ehr_id}/composition/{self.encoded_identifier}"
        pomiar_response = self.client.get(request_url, name="get_pomiar_full_openehr", headers=ehr_headers, verify=False)
        if pomiar_response.status_code == 200:
            log(f"Got pomiar full data patient with pesel {self.pesel} and ehr id {self.ehr_id}", LogLevel.DEBUG)
        else:
            log(f"Failed to get pomiar full data patient with pesel: {self.pesel} and ehr id: {self.ehr_id}", LogLevel.WARNING)
            log(pomiar_response.content, LogLevel.WARNING)

    @task(1)
    def get_doctor_name(self):
        self._get_top_level_property("get_doctor_name_openehr", 
                            self.ehr_id, 
                            self.composition_id,
                            property_path="c/composer/name AS composer_name")

    @task(1)
    def get_pressure_measurement_result(self):
        self._get_property("get_pressure_measurement_result_openehr", 
                            self.ehr_id, 
                            self.composition_id,
                            archetype_type="OBSERVATION",
                            archetype_value="openEHR-EHR-OBSERVATION.intraocular_pressure.v0",
                            property_path="data[at0001]/events[at0002]/data[at0003]/items[at0042]/value")
        
    @task(1)
    def get_device_part_number(self):
        self._get_property("get_device_part_number_openehr", 
                            self.ehr_id, 
                            self.composition_id,
                            archetype_type="CLUSTER",
                            archetype_value="openEHR-EHR-CLUSTER.device_details.v1",
                            property_path="items[at0007]/value/value")
 
class PatientWithPlanLeczenia(Patient):
    fixed_count = USERS_PER_DOCUMENT_COUNT
    host = OPENEHR_SERVER

    def on_start(self):
        try:
            self.pesel = pesels_queue.get_nowait()
            (ehr_id, composition_id) = upload_plan_leczenia_openehr(self.pesel, save=False, verbose=False)
            self.ehr_id = ehr_id
            self.composition_id = composition_id
            self.encoded_identifier = urllib.parse.quote_plus(composition_id)
            log(f"Created plan leczenia composition for patient with pesel: {self.pesel} and ehr id: {self.ehr_id} in OpenEHR", LogLevel.INFO)
        except:
            raise Exception("No more PESELS available!")
        
    @task(1)
    def get_whole_data(self):
        request_url = f"{BASE_URL}/ehr/{self.ehr_id}/composition/{self.encoded_identifier}"
        plan_leczenia_response = self.client.get(request_url, name="get_plan_leczenia_full_openehr", headers=ehr_headers, verify=False)
        if plan_leczenia_response.status_code == 200:
            log(f"Got plan leczenia full data patient with pesel {self.pesel} and ehr id {self.ehr_id}", LogLevel.DEBUG)
        else:
            log(f"Failed to get plan leczenia full data patient with pesel: {self.pesel} and ehr id: {self.ehr_id}", LogLevel.WARNING)
            log(plan_leczenia_response.content, LogLevel.WARNING)    

    @task(1)
    def get_mediaction_name(self):
        self._get_property("get_mediaction_name_openehr", 
                            self.ehr_id, 
                            self.composition_id,
                            archetype_type="INSTRUCTION",
                            archetype_value="openEHR-EHR-INSTRUCTION.medication_order.v0",
                            property_path="activities[at0001]/description[at0002]/items[at0070]/value/value")
        
    @task(1)
    def get_dose_value_and_unit(self):
        self._get_property("get_dose_value_and_unit_openehr", 
                            self.ehr_id, 
                            self.composition_id,
                            archetype_type="INSTRUCTION",
                            archetype_value="openEHR-EHR-INSTRUCTION.medication_order.v0",
                            property_path="activities[at0001]/description[at0002]/items[at0109]/value/value")
        
    @task(1)
    def get_allergy_reaction(self):
        self._get_property("get_allergy_reaction_openehr", 
                            self.ehr_id, 
                            self.composition_id,
                            archetype_type="EVALUATION",
                            archetype_value="openEHR-EHR-EVALUATION.adverse_reaction_risk.v1",
                            property_path="data[at0001]/items[at0006]/value/value")

class PatientWithWynikiBadan(Patient):
    fixed_count = USERS_PER_DOCUMENT_COUNT
    host = OPENEHR_SERVER

    def on_start(self):
        try:
            self.pesel = pesels_queue.get_nowait()
            (ehr_id, composition_id) = upload_wyniki_badan_openehr(self.pesel, save=False, verbose=False)
            self.ehr_id = ehr_id
            self.composition_id = composition_id
            self.encoded_identifier = urllib.parse.quote_plus(composition_id)
            log(f"Created wyniki badan composition for patient with pesel: {self.pesel} and ehr id: {self.ehr_id} in OpenEHR", LogLevel.INFO)
        except:
            raise Exception("No more PESELS available!")
        
    @task(1)
    def get_whole_data(self):
        request_url = f"{BASE_URL}/ehr/{self.ehr_id}/composition/{self.encoded_identifier}"
        wyniki_badan_response = self.client.get(request_url, name="get_wyniki_badan_full_openehr", headers=ehr_headers, verify=False)
        if wyniki_badan_response.status_code == 200:
            log(f"Got wyniki badan full data patient with pesel {self.pesel} and ehr id {self.ehr_id}", LogLevel.DEBUG)
        else:
            log(f"Failed to get wyniki badan full data patient with pesel: {self.pesel} and ehr id: {self.ehr_id}", LogLevel.WARNING)
            log(wyniki_badan_response.content, LogLevel.WARNING) 

    @task(1)
    def get_specimen_collection_time(self):
        self._get_property("get_specimen_collection_time_openehr", 
                            self.ehr_id, 
                            self.composition_id,
                            archetype_type="CLUSTER",
                            archetype_value="openEHR-EHR-CLUSTER.specimen.v1",
                            property_path="items[at0015]/value/value")  
        
    @task(1)
    def get_glucose_result(self):
        self._get_property("get_glucose_result_openehr", 
                            self.ehr_id, 
                            self.composition_id,
                            archetype_type="CLUSTER",
                            archetype_value="openEHR-EHR-CLUSTER.laboratory_test_analyte.v1",
                            property_path="items[at0001]/value")  
        
    @task(1)
    def get_HbA1c_SNOMED_CT(self):
        self._get_property("get_HbA1c_SNOMED_CT_openehr", 
                            self.ehr_id, 
                            self.composition_id,
                            archetype_type="CLUSTER",
                            archetype_value="openEHR-EHR-CLUSTER.laboratory_test_analyte.v1",
                            property_path="items[at0024]/value/defining_code/code_string",
                            additional_condition="o/name/value = 'HbA1c'")  
