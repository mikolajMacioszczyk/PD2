from upload_template import upload_template

MEDICAL_DOCUMENT_TYPE = "pomiar"
default_template_file_name = 'Intraocular_pressure_study.opt'

def upload_intraocular_pressure_study_template():
    upload_template(template_file_name=default_template_file_name, medical_document_type=MEDICAL_DOCUMENT_TYPE)

if __name__ == "__main__":
    upload_intraocular_pressure_study_template()