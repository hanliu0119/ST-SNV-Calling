import pandas as pd
import glob

NUM = '17'
DATA_PATH = '../Ductal_processed_data/processed_vcf_tables_' + NUM + '/' 
OUTPUT_PATH = '../Ductal_processed_data/union_set_' + NUM + ".csv"

# Step 1: List of all CSV files
all_files = glob.glob(DATA_PATH + "/*.csv")

list_of_dfs = []

# Read each file into a DataFrame and append to the list
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    list_of_dfs.append(df)

# Step 2: Concatenate all the DataFrames in the list
merged_df = pd.concat(list_of_dfs, axis=0, ignore_index=True)

# Step 3: Drop duplicates
merged_df.drop_duplicates(inplace=True)

# Step 4: Save the final DataFrame as a new CSV
merged_df.to_csv(OUTPUT_PATH, index=False)
