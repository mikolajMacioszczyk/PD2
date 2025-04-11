
from openehr_conf import DATA_DIRECTORY_PATH
from upload_composition import upload_composition

MEDICAL_DOCUMENT_TYPE = "skierowanie"
default_pesel = "80010112346"
default_composition_file_name = 'eRefferal-flat.json'
default_composition_file_path = f"{DATA_DIRECTORY_PATH}{MEDICAL_DOCUMENT_TYPE}/OpenEHR/{default_composition_file_name}"

if __name__ == "__main__":
    template_id = "eReferral"
    upload_composition(default_pesel, default_composition_file_path, template_id)