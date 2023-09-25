import pandas as pd
import os 

NUM = '17'

DATA_PATH = f'../Ductal_processed_data/vcf_tables_{NUM}/'
OUTPUT_PATH = f'../Ductal_processed_data/processed_vcf_tables_{NUM}/'

def get_filenames(directory_path):
    file_names = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    return file_names

def retrive_snp(directory_path, filenames):
    for filename in filenames:
        try:
            df = pd.read_csv(directory_path + filename)
            selected_data = df[['CHROM', 'POS', 'REF', 'ALT', '20']].values.tolist()
            df = pd.DataFrame(selected_data, columns=['CHROM', 'POS', 'REF', 'ALT', '20'])
            df['20'] = df['20'].str.split(':').str[0]

            # Task 2: Replace values
            replacements = {'1/1': '0/1', '1/0': '0/1', '1/2': '0/1'}
            df['20'] = df['20'].replace(replacements)

            # Task 3: Remove duplicates
            df = df.drop_duplicates()
            df.to_csv(OUTPUT_PATH + "processed_" + filename, index=False)
            print("processed: ",directory_path + filename)

        except pd.errors.EmptyDataError:
            print(f"The file '{filename}' is empty.")

def main():
    filenames = get_filenames(DATA_PATH)
    print(filenames)
    retrive_snp(DATA_PATH, filenames)

main()