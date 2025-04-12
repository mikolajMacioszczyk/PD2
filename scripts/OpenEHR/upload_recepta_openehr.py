from openehr_conf import DATA_DIRECTORY_PATH
from composition import upload_and_save

MEDICAL_DOCUMENT_TYPE = "recepta"
default_pesel = "80010112345"
default_composition_file_name = 'ePrescription-flat.json'
default_composition_file_path = f"{DATA_DIRECTORY_PATH}{MEDICAL_DOCUMENT_TYPE}/OpenEHR/input/{default_composition_file_name}"

if __name__ == "__main__":
    template_id = "ePrescription"
    upload_and_save(default_pesel, default_composition_file_path, template_id, MEDICAL_DOCUMENT_TYPE)