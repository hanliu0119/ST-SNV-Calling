import pandas as pd
from io import StringIO
import os 
import glob

NUM = '17'
INPUT_DATA_PATH = f'../Ductal_data/output_VCF_{NUM}/'
OUTPUT_DATA_PATH = f'../Ductal_processed_data/vcf_tables_{NUM}/'


def get_folder_names(directory_path):
    # List all entries in the directory
    all_entries = os.listdir(directory_path)
    
    # Filter only the folders (directories)
    return [entry for entry in all_entries if os.path.isdir(os.path.join(directory_path, entry))]


def vcf_to_dataframe(vcf_filename):
    # Skip meta-information lines
    try:
        with open(vcf_filename, 'r') as f:
            lines = [line for line in f if not line.startswith('##')]
    except FileNotFoundError:
        print(f"The file '{vcf_filename}' does not exist.")
        return pd.DataFrame()  # return an empty dataframe
        
    if not lines:
        print(f"The VCF file '{vcf_filename}' has no content or only contains meta-information lines.")
        return pd.DataFrame()  # return an empty dataframe

    # Use pandas to convert VCF lines to a DataFrame
    df = pd.read_csv(
        StringIO(''.join(lines)),
        dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str,
               'QUAL': str, 'FILTER': str, 'INFO': str},
        sep='\t'
    ).rename(columns={'#CHROM': 'CHROM'})
    
    return df

def main():
    # retrieve all the paths
    # paths = get_folder_names(INPUT_DATA_PATH)
    paths = os.listdir(INPUT_DATA_PATH)
    print(paths)
    for path in paths:
        vcf_filename = INPUT_DATA_PATH + path + '/new_rg.vcf'
        print(vcf_filename)
        df = vcf_to_dataframe(vcf_filename)
        df.to_csv(OUTPUT_DATA_PATH + path + ".csv", index=False)

main()