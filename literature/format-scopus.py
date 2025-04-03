import pandas as pd
from conf import BASE_DIR

input_file = f"{BASE_DIR}scopus.csv"
output_file = f'{BASE_DIR}formated-scopus.csv'

try:
    df = pd.read_csv(input_file)
    
    required_columns = ["Title", 'Authors', 'Year', 'DOI']
    columns_to_save = ["Title", 'Authors', 'Publication Year', 'DOI']
    available_columns = [col for col in required_columns if col in df.columns]

    if not available_columns:
        print("Brak wymaganych kolumn w pliku CSV.")
    else:
        df.rename(columns={'Year': 'Publication Year'}, inplace=True)
        available_columns_to_save = [col for col in columns_to_save if col in df.columns]

        df[available_columns_to_save].to_csv(output_file, index=False)
        print(f"Zapisano kolumny {available_columns_to_save} do pliku '{output_file}'.")

except FileNotFoundError:
    print(f"Plik '{input_file}' nie został znaleziony.")
except Exception as e:
    print(f"Wystąpił błąd: {e}")