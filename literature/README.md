# Popularność standardów danych medycznych w literaturze naukowej

## Dane

Zebrane dane z bibliotek cyfrowych:
- Institute of Electrical and Electronics Engineers,
- PubMed,
- Scopus,
znajdują się w folderze data

## Selekcja kolumn i złączenie danych

Za selekcje kolumn z wyeksportowanych plików i przekszałcenie ich nazw do wspólnego formatu odpowiadają skrypty:
- format-ieee.py
- format-pubmed.py
- format-scopus.py

Za złączenie wyników i usunięcie duplikatów odpowiada skrypt 'merge-literature.py'

## Konfiguraca

Skrypty wykonywane są na danych w folderze, którego ścieżkę wyspecyfikować można w conf.py