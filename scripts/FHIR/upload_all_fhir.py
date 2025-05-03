from upload_iniekcja import upload_iniekcja_full
from upload_pomiar import upload_pomiar_full
from upload_recepta_fhir import upload_recepta_full
from upload_skierowanie_fhir import upload_skierowanie_full
from upload_wyniki_badan import upload_wyniki_badan_full

if __name__ == "__main__":
    upload_recepta_full()
    upload_skierowanie_full()
    upload_pomiar_full()
    upload_iniekcja_full()
    upload_wyniki_badan_full()