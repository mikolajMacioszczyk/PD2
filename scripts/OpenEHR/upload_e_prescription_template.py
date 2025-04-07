import requests
from openehr_conf import OPENEHR_SERVER

template_file_path = 'ePrescription.opt'

url = f'{OPENEHR_SERVER}ehrbase/rest/openehr/v1/definition/template/adl1.4'

headers = {
    'Content-Type': 'application/xml'
}

with open(template_file_path, 'rb') as file:
    template_data = file.read()

response = requests.post(url, headers=headers, data=template_data)

print(f'Status: {response.status_code}')
print(f'Odpowiedź: {response.text}')