from upload_AMD_treatment_template import upload_AMD_template
from upload_e_laboratory_test_result_template import upload_e_laboratory_template
from upload_e_prescription_template import upload_e_prescription_template
from upload_e_referral_template import upload_e_refferal_template
from upload_intraocular_pressure_study_template import upload_intraocular_pressure_study_template

from upload_iniekcja_openehr import upload_iniekcja_full
from upload_pomiar_openehr import upload_pomiar_full
from upload_recepta_openehr import upload_recepta_full
from upload_skierowanie_openehr import upload_skierowanie_full
from upload_wyniki_badan_openehr import upload_wyniki_badan_full

WITH_TEMPLATES = True

if __name__ == "__main__":
    if WITH_TEMPLATES:
        upload_e_prescription_template()
        upload_e_refferal_template()
        upload_intraocular_pressure_study_template()
        upload_AMD_template()
        upload_e_laboratory_template()

    upload_recepta_full(verbose=True)
    upload_skierowanie_full(verbose=True)
    upload_pomiar_full(verbose=True)
    upload_iniekcja_full(verbose=True)
    upload_wyniki_badan_full(verbose=True)