from upload_template import upload_template

MEDICAL_DOCUMENT_TYPE = "iniekcja"
default_template_file_name = 'AMD_treatment.opt'

def upload_AMD_template():
    upload_template(template_file_name=default_template_file_name, medical_document_type=MEDICAL_DOCUMENT_TYPE)

if __name__ == "__main__":
    upload_AMD_template()