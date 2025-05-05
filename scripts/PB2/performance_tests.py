# run me with: locust -f .\basket_requests.py  --csv stats/basket_requests
# run me with: python3 -m locust -f ./basket_requests.py --headless -u 50 -r 1 --csv stats/basket_requests --run-time 1h
import os
import random
import sys
from locust import HttpUser, between, task
import urllib3
import json
from utils import *

from FHIR.fhir_conf import FHIR_SERVER
from OpeEHR.openehr_conf import OPENEHR_SERVER

# FHIR_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'FHIR'))
# sys.path.append(FHIR_path)

# from fhir_conf import FHIR_SERVER

# OpenEHR_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'OpenEHR'))
# sys.path.append(OpenEHR_path)

# from openehr_conf import OPENEHR_SERVER

USERS_PER_DOCUMENT_COUNT = 1

print(f"FHIR server endpoint = {FHIR_SERVER}")
print(f"OpenEHR server endpoint = {OPENEHR_SERVER}")

DOCUMENT_TYPES_COUNT = 5
pesels = generate_unique_11_digit_numbers(USERS_PER_DOCUMENT_COUNT * DOCUMENT_TYPES_COUNT)

# TODO: Divide pesels into differnt medical document types
# TODO: Initialize database
# TODO: Run tests


# url = f'{CATALOG_HOST}/ActiveProducts'
# catalog_data = fetch_data_from_api(url)
# items = catalog_data.get('items', [])
# catalog_product_ids = [item['id'] for item in items]

# ## ignore HTTPS errors in console
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# dataset_id = str(uuid.uuid4())
# dataset_name = generate_random_string(8)
# organization_name = generate_random_string(8)0
# organization_disease_datasets_id = str(uuid.uuid4())
# subscription_id = str(uuid.uuid4())
# consent_version_id = str(uuid.uuid4())
# consent_definition_id = str(uuid.uuid4())

# wait_until_user_confirms('y')

# class UserTestData:
#     def __init__(self, id, basket_id):
#         self.id = id
#         self.basket_id = basket_id

# counter = 0

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
