import requests
from openehr_conf import OPENEHR_SERVER, DATA_DIRECTORY_PATH

url = f'{OPENEHR_SERVER}ehrbase/rest/openehr/v1/definition/template/adl1.4'

headers = {
    'Content-Type': 'application/xml'
}

def upload_template(template_file_name, medical_document_type):
    template_file_path = f"{DATA_DIRECTORY_PATH}{medical_document_type}/OpenEHR/{template_file_name}"

    with open(template_file_path, 'rb') as file:
        template_data = file.read()

    response = requests.post(url, headers=headers, data=template_data)

    if response.status_code == 201:
        print("Template created")
    else:
        print(f'Template creation failed: {response.text}')
