# Porównanie wybranych standardów przechowywania i wymiany danych w systemach medycznych

## Opis projektu

Niniejszy projekt badawczy służy do analizy, porównania i ewaluacji dwóch wiodących standardów reprezentacji danych medycznych – HL7 FHIR oraz openEHR. Środowisko projektowe umożliwia uruchomienie lokalnych instancji serwerów FHIR (HAPI) i openEHR (EHRbase), przeprowadzenie badań oraz przetwarzanie danych z wykorzystaniem skryptów w języku Python.

## Struktura katalogów

``` bash
├── scripts/
│   ├── PB1/                # Skrypty do badań powiązanych z pytaniem badawczym 1
│   ├── PB2/                # Skrypty do badań powiązanych z pytaniem badawczym 2
│   ├── FHIR/               # Skrypty przygotowujące środowisko FHIR
│   ├── OpenEHR/            # Skrypty przygotowujące środowisko openEHR
│   └── configuration/      # Zmienne konfiguracyjne używane w skryptach
│
├── data/                   # Dane wejściowe i wynikowe generowane przez skrypty
│
├── literature/             # Dane i skrypty wykorzystywane do przeglądu literatury nt. popularności standardów
│
├── fhir-docker-compose.yml         # Plik docker-compose uruchamiający serwer HAPI FHIR
├── openehr-docker-compose.yml      # Plik docker-compose uruchamiający serwer EHRbase
├── start-compose.bat               # Skrypt .bat uruchamiający oba serwery równocześnie
├── requirements.txt                # Lista zależności Pythona (pip)
├── .env                            # Zmienne środowiskowe dla serwerów
```

## Wersje oprogramowania

Projekt wykorzystuje następujące wersje oprogramowania:

| Komponent                | Wersja                                                               |
| ------------------------ | -------------------------------------------------------------------- |
| **Docker**               | 28.0.1                                                               |
| **Python**               | 3.13.0                                                               |
| **pip**                  | 25.0                                                                 |
| **FHIR**                 | HL7 FHIR R5                                                          |
| **HAPI FHIR**            | `hapiproject/hapi:v8.0.0-1`                                          |
| **PostgreSQL (FHIR)**    | `postgres:17.4`                                                      |
| **EHRbase**              | `ehrbase/ehrbase:2.16.0`                                             |
| **PostgreSQL (openEHR)** | `ehrbase/ehrbase-v2-postgres:16.2`                                   |

## Instalacja zależności i reprodukcja badań

Przed uruchomieniem skryptów należy zainstalować wymagane pakiety:

``` cmd
pip install -r requirements.txt
```

### Etap przygotowania

Aby uruchomić oba serwery (FHIR i openEHR), wystarczy wykonać skrypt start-compose.bat, który wykorzystuje pliki docker-compose oraz konfigurację z pliku .env.

``` cmd
start-compose.bat
```

Transformacja i wgranie dokumentów medycznych na odpowiednie serwery wykonywana jest za pomocą skrytpów Python znajdujących się w folderze scripts/{standard}.

Dla openEHR: 

``` cmd
cd scripts/FHIR
python upload_all_openehr.py
```

Dla FHIR: 

``` cmd
cd scripts/FHIR
python upload_all_fhir.py
```

### Pytanie badawcze 1

Skrypty umożliwiające reprodukcję PB1 znadjują się w folderze scripts/PB1.
Wyliczenie metryk i testów istotności statystycznej wykonywane jest za pomoca jednego skryptu main.py. W wyniku jego działania zapisywane sa pliki CSV ze wszystkimi rezultatami.

``` cmd
cd scripts/PB1
python main.py
```

### Pytanie badawcze 2

Procedura testów wydajnosciowych dla openEHR i FHIR zapisane jest odpowiednio w skryptach: performance_tests_openehr.pl i performance_tests_fhir.py.
Ich uruchomienie wymaga działającego serwera danego stadnardu. Rekomenduje się uruchomienie testów niezależnie, żeby działanie serwerów nie wpływało na siebie.
W wyniku działania narzedzia Locust zapisywane są wyniki miar statystycznych w plikach CSV.

Dla openEHR: 

``` cmd
cd scripts/PB2
locust -f .\performance_tests_openehr.py  --csv stats/performance_tests_openehr
```

Dla FHIR: 

``` cmd
cd scripts/PB2
locust -f .\performance_tests_fhir.py  --csv stats/performance_tests_fhir
```