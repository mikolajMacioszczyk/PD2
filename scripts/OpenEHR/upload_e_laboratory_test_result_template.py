from upload_template import upload_template

MEDICAL_DOCUMENT_TYPE = "wyniki_badan"
default_template_file_name = 'eLaboratoryTestResult.opt'

if __name__ == "__main__":
    upload_template(template_file_name=default_template_file_name, medical_document_type=MEDICAL_DOCUMENT_TYPE)