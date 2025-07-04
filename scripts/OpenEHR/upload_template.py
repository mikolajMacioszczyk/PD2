import requests
from openehr_conf import OPENEHR_SERVER, DATA_DIRECTORY_PATH

url = f'{OPENEHR_SERVER}ehrbase/rest/openehr/v1/definition/template/adl1.4'

headers = {
    'Content-Type': 'application/xml'
}

def upload_template(template_file_name, medical_document_type, verbose_conflict=False):
    template_file_path = f"{DATA_DIRECTORY_PATH}{medical_document_type}/OpenEHR/input/{template_file_name}"

    with open(template_file_path, 'rb') as file:
        template_data = file.read()

    response = requests.post(url, headers=headers, data=template_data)

    if response.status_code == 201:
        print("Template created")
    elif response.status_code == 409:
        if verbose_conflict:
            print(f'Conflict while creating template: {response.text}')
    else:
        print(f'Template creation failed: {response.text}')
