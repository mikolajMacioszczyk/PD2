
from openehr_conf import DATA_DIRECTORY_PATH
from composition import upload_and_save

MEDICAL_DOCUMENT_TYPE = "pomiar"
TEMPLATE_ID = "Intraocular_pressure_study"
default_pesel = "80010112349"
default_composition_file_name = 'Intraocular_pressure_study-flat.json'
default_composition_file_path = f"{DATA_DIRECTORY_PATH}{MEDICAL_DOCUMENT_TYPE}/OpenEHR/input/{default_composition_file_name}"

def upload_pomiar_full():
    upload_and_save(default_pesel, default_composition_file_path, TEMPLATE_ID, MEDICAL_DOCUMENT_TYPE)

if __name__ == "__main__":
    upload_pomiar_full()