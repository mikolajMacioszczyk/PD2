from openehr_conf import DATA_DIRECTORY_PATH
from composition import upload_and_save

MEDICAL_DOCUMENT_TYPE = "recepta"
TEMPLATE_ID = "ePrescription"
default_pesel = "80010112345"
default_composition_file_name = 'ePrescription-flat.json'
default_composition_file_path = f"{DATA_DIRECTORY_PATH}{MEDICAL_DOCUMENT_TYPE}/OpenEHR/input/{default_composition_file_name}"

if __name__ == "__main__":
    upload_and_save(default_pesel, default_composition_file_path, TEMPLATE_ID, MEDICAL_DOCUMENT_TYPE)