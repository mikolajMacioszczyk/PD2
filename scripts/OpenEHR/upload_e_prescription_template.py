from upload_template import upload_template

MEDICAL_DOCUMENT_TYPE = "recepta"
default_template_file_name = 'ePrescription.opt'

def upload_e_prescription_template():
    upload_template(template_file_name=default_template_file_name, medical_document_type=MEDICAL_DOCUMENT_TYPE)

if __name__ == "__main__":
    upload_e_prescription_template()