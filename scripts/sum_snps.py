import pandas as pd
import os 

NUM = '17'

DATA_PATH = '../Ductal_processed_data/vcf_tables_' + NUM + '/'
OUTPUT_PATH = '../Ductal_processed_data/sum_snp_' + NUM +'.txt'

def get_filenames(directory_path):
    file_names = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    return file_names



def main():
    filenames = get_filenames(DATA_PATH)
    # print(filenames)
    num_rows = []
    for filename in filenames:
        try:
            df = pd.read_csv(DATA_PATH + filename)
            num_rows += [len(df)]
            with open(OUTPUT_PATH, "a") as file:
                file.write(filename.split(".")[0] + ": " + str(len(df)) + "\n")
        except pd.errors.EmptyDataError:
            print(f"The file '{filename}' is empty.")
            num_rows += [0]
            with open(OUTPUT_PATH, "a") as file:
                file.write(filename.split(".")[0] + ": 0" + "\n")
    return num_rows

num_rows = main()
print(max(num_rows), min(num_rows))