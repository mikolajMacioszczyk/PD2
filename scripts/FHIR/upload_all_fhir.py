from upload_iniekcja import upload_iniekcja_full
from upload_pomiar import upload_pomiar_full
from upload_recepta_fhir import upload_recepta_full
from upload_skierowanie_fhir import upload_skierowanie_full
from upload_wyniki_badan import upload_wyniki_badan_full

if __name__ == "__main__":
    upload_recepta_full(pesel=80010112345, verbose=True)
    upload_skierowanie_full(pesel=80010112346, verbose=True)
    upload_pomiar_full(pesel=80010112349, verbose=True)
    upload_iniekcja_full(pesel=80010112350, verbose=True)
    upload_wyniki_badan_full(pesel=80010112347, verbose=True)