
from openehr_conf import DATA_DIRECTORY_PATH
from composition import upload_and_save

MEDICAL_DOCUMENT_TYPE = "iniekcja"
TEMPLATE_ID = "AMD_treatment"
default_pesel = "80010112350"
default_composition_file_name = 'AMD_treatment-flat.json'
default_composition_file_path = f"{DATA_DIRECTORY_PATH}{MEDICAL_DOCUMENT_TYPE}/OpenEHR/input/{default_composition_file_name}"

if __name__ == "__main__":
    upload_and_save(default_pesel, default_composition_file_path, TEMPLATE_ID, MEDICAL_DOCUMENT_TYPE)