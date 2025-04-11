import requests
from openehr_conf import OPENEHR_SERVER, DATA_DIRECTORY_PATH

default_template_file_name = 'ePrescription.opt'
default_template_file_path = f"{DATA_DIRECTORY_PATH}recepta/OpenEHR/{default_template_file_name}"

url = f'{OPENEHR_SERVER}ehrbase/rest/openehr/v1/definition/template/adl1.4'

headers = {
    'Content-Type': 'application/xml'
}

def upload_e_prescription_template(template_file_path = default_template_file_path):
    with open(template_file_path, 'rb') as file:
        template_data = file.read()

    response = requests.post(url, headers=headers, data=template_data)

    if response.status_code == 201:
        print("Template created")
    else:
        print(f'Template creation failed: {response.text}')

if __name__ == "__main__":
    upload_e_prescription_template()