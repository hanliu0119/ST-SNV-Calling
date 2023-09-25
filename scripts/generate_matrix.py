import pandas as pd
import os 

NUM = '17'
CELLS_VCF_PATH = '../Ductal_processed_data/processed_vcf_tables_' + NUM + '/'
UNION_SET_PATH = '../Ductal_processed_data/union_set_' + NUM + '.csv'
OUTPUT_PATH = '../Ductal_processed_data/matrix_' + NUM + '.pkl'


def merge_dfs(df_a, df_b):
    # Merge the two dataframes on all columns and keep the index of df_a
    merged_df = pd.merge(df_a, df_b, how='inner', left_on=df_a.columns.tolist(), right_on=df_b.columns.tolist())

    # Create a list of 1's and 0's based on the index
    result = [1 if index in merged_df.index else 0 for index in df_a.index]
    return result
    
def get_filenames(directory_path):
    file_names = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    return file_names

def main():

    filenames = get_filenames(CELLS_VCF_PATH)
    union_df = pd.read_csv(UNION_SET_PATH)
    results = []
    for filename in filenames:
        cell_df = pd.read_csv(CELLS_VCF_PATH + filename)
        print(filename, len(cell_df), len(union_df))
        results += [merge_dfs(union_df, cell_df)]

    cols = ['snp'+ str(v) for v in range(len(union_df))]
    rows = [x.split(".")[0] for x in filenames]
    df = pd.DataFrame(results, index=rows, columns=cols)
    sparse_df = df.astype(pd.SparseDtype("int", 0))
    sparse_df.to_pickle(OUTPUT_PATH)

main()