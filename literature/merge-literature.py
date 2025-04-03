import pandas as pd
from conf import BASE_DIR, STANDARD

scopusFile = f'{BASE_DIR}formated-scopus.csv'
pubmedFile = f'{BASE_DIR}formated-pubmed.csv'
ieeeFile = f'{BASE_DIR}formated-ieee.csv'
merged_sorted_output_file = f'{BASE_DIR}{STANDARD}_merged_sorted.csv'
count_by_year_file = f'{BASE_DIR}{STANDARD}_publication_count_by_year.csv'

scopusDf = pd.read_csv(scopusFile)
pubmedDf = pd.read_csv(pubmedFile)
ieeDf = pd.read_csv(ieeeFile)

mergedDf = pd.concat([scopusDf, pubmedDf, ieeDf], ignore_index=True)

before = len(mergedDf)

mergedDf = mergedDf.drop_duplicates(subset='DOI')

after = len(mergedDf)

mergedDf['Publication Year'] = pd.to_numeric(mergedDf['Publication Year'], errors='coerce')
df = mergedDf.sort_values(by='Publication Year')

df.to_csv(merged_sorted_output_file, index=False)

year_counts = df['Publication Year'].value_counts().sort_index()
year_counts_df = year_counts.reset_index()
year_counts_df.columns = ['Publication Year', 'Number of Publications']
year_counts_df.to_csv(count_by_year_file, index=False)

print(f"Gotowe! Usunięto {before - after} duplikatów na podstawie DOI, zapisano łącznie {after} publikacji w pliku {merged_sorted_output_file}")
print(f"Liczba publikacji na rok została zapisana w pliku {count_by_year_file}")
