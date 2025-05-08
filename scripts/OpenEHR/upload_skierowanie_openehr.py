
from openehr_conf import DATA_DIRECTORY_PATH
from composition import upload_and_save
from openehr_conf import VERBOSE

MEDICAL_DOCUMENT_TYPE = "skierowanie"
TEMPLATE_ID = "eReferral"
default_pesel = "80010112346"
default_composition_file_name = 'eRefferal-flat.json'
default_composition_file_path = f"{DATA_DIRECTORY_PATH}{MEDICAL_DOCUMENT_TYPE}/OpenEHR/input/{default_composition_file_name}"

def upload_skierowanie_full(pesel=default_pesel, save=True, verbose=VERBOSE):
    return upload_and_save(pesel, default_composition_file_path, TEMPLATE_ID, MEDICAL_DOCUMENT_TYPE, save, verbose)

if __name__ == "__main__":
    upload_skierowanie_full(verbose=True)