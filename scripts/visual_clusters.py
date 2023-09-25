import pdb
pdb.set_trace()
import pandas as pd
import scanpy as sc
import matplotlib as plt

NUM = '6'
INPUT_TXT_PATH = f'./visual_data/tbsp_{NUM}.txt'

clusters = []
obtained_ndata_index = []
with open(INPUT_TXT_PATH, 'r') as f:
    for line in f:
        # Split the line by the colon and get the second part (index 1)
        index, number = line.strip().split(":")
        clusters.append(int(number))  # Convert the string to an integer and append to the list
        obtained_ndata_index.append(index)

# print(clusters[:10])

H5_PATH = '/data/maiziezhou_lab/hanliu/apps/'
# H5_PATH = '/data/maiziezhou_lab/Datasets/ST_datasets/10x_BC_Ductal_Carcinoma_In_Situ_Invasive_Carcinoma_FFPE/'
# FILENAME = 'Visium_FFPE_Human_Breast_Cancer_filtered_feature_bc_matrix.h5'
FILENAME = 'CytAssist_FFPE_Protein_Expression_Human_Breast_Cancer_filtered_feature_bc_matrix.h5'


adata = sc.read_visium(path = H5_PATH, count_file = FILENAME)
# adata = sc.read_10x_h5(H5_PATH+FILENAME)

print("data read in >> ")
# raw_ndata_index = adata.obs.index.to_list()
# print(adata.obs.index.to_list())


adata_subset = adata[obtained_ndata_index, :]

adata_subset.obs['clusters'] = clusters
adata_subset.obs['array_col'] = [int(v) for v in adata_subset.obs['array_col']]
adata_subset.obs['array_row'] = [int(v) for v in adata_subset.obs['array_row']]
adata_subset.obs['in_tissue'] = [int(v) for v in adata_subset.obs['in_tissue']]
adata_subset.obs['clusters'] = [int(v) for v in adata_subset.obs['clusters']]

# print(adata_subset)
# print(adata_subset.obs[:5])
# print(adata_subset.obsm)
# print(adata_subset.uns)
# print(adata_subset.var)
# print(adata_subset.X)
print(adata_subset.obs[:5])
print(type(adata_subset.obs['clusters'][0]))
print(type(adata_subset.obs['array_col'][0]))
print(type(adata_subset.obs['array_row'][0]))
print(type(adata_subset.obs['in_tissue'][0]))
sc.pl.spatial(adata_subset, color=['clusters'], cmap='viridis', save="filename.png")
# sc.pl.spatil(adata_subset, color='clusters', cmap='viridis', save="filename.png")

# clusters = [0] * len(adata.obs)
# adata.obs['clusters'] = clusters

# print(adata.obs[:5])
# sc.pl.spatial(adata, color='clusters', cmap='viridis', save="filename.png")

