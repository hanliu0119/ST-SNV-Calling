'''
    This is the main file of the ST-SNV calling Project
'''

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import glob
'''
    Parameters Settings >>>
'''
# 6: 330
# 12: 540
# 18: 620

# calculate euclidian pixel for each cell
RAD_LIM = 330
NEIGHBOR_LIM = 6
# TISSUE_POS_PATH = '/data/maiziezhou_lab/Datasets/ST_datasets/10x_BC_6.5mm_Visium_CytAssist_FFPE/spatial/tissue_positions.csv'
TISSUE_POS_PATH = '/data/maiziezhou_lab/Datasets/ST_datasets/10x_BC_Ductal_Carcinoma_In_Situ_Invasive_Carcinoma_FFPE/spatial/tissue_positions_list.csv'

# merge neighbor bams with center bams
NEIGHBOR_PIXEL_PATH = 'Ductal_Neighbors_pixels_revised_test_' + str(NEIGHBOR_LIM) +'.csv'
BAM_PATH = '/data/maiziezhou_lab/Datasets/ST_datasets/10x_BC_Ductal_Carcinoma_In_Situ_Invasive_Carcinoma_FFPE/split_by_cell/bam_bycell/'
# SNV calling
MERGED_BAM_PATH = '/data/maiziezhou_lab/hanliu/apps/ST-SNV_Calling/Ductal_data/merged_BAM_' + str(NEIGHBOR_LIM)
OUT_VCF_PATH = '/data/maiziezhou_lab/hanliu/apps/ST-SNV_Calling/Ductal_data/output_VCF_' + str(NEIGHBOR_LIM)
# OUT_VCF_PATH = '/data/maiziezhou_lab/hanliu/output_VCF'
REFERENCE = '/data/maiziezhou_lab/Softwares/refdata-GRCh38-2.1.0/fasta/genome.fa'
'''
    Parameters Settings <<<
'''

def cal_euclidian_pixel(rad_lim, neighbor_lim, path):
    data = pd.read_csv(path)
    names = data['barcode'].values
    col = data['pxl_col_in_fullres'].values
    row = data['pxl_row_in_fullres'].values
    flag = data['in_tissue'].values
    # create data phrame for the final output
    edges = 0
    all_points = np.column_stack((row, col))
    df_names = ['Center', 'Neighbors', 'Distance']
    df = pd.DataFrame(columns = df_names)
    # initialize parameters to calculate number of edge cells
    num_neighbors = 0
    num = 0

    for i in range(len(names)):
    # only enter calculation if the cell is in tissue
        if(flag[i] == 1):
            num += 1
            point = [row[i], col[i]]
            # calculate distances from all points
            dist = np.linalg.norm(all_points - point, axis = 1)
            # find all indices where the dist from current point to that cell is within the set limits
            idx = np.where((0.0 < dist) & (dist < rad_lim) & (flag == 1))[0]
            neighbors = [names[j] for j in idx]
            neighbor_dist = [dist[j] for j in idx]
            # if the point does not contain as much neighbors as we hoped, we say it is an "edge" cell
            num_neighbors += len(neighbors)
            if(len(neighbors) < neighbor_lim):
                edges += 1
            
            # optional testing, if need to test radius
            if(len(neighbors) > neighbor_lim):
                print('wrong')

            new_data = {'Center': names[i], 'Neighbors': neighbors, 'Distance': neighbor_dist}
            new_data = pd.DataFrame(new_data)
            df = pd.concat([df, new_data], ignore_index = True)
    # final summary
    avg_neigh = num_neighbors / num
    # print("Total of " + str(num) + ' center cells. Detected ' + str(edges) + ' edges.')
    # print('Average number of neighbors per cell is ' + str(avg_neigh) + ' neighbors.')
    df.to_csv(NEIGHBOR_PIXEL_PATH, index = False)

def merge_bam_files(bam_files, prev):
    name = 'Ductal_data/merged_BAM_' + str(NEIGHBOR_LIM) + '/' + prev + '_merge.bam'
    # merge BAM files
    merge_command = ['samtools', 'merge', '-o', name] + bam_files
    subprocess.run(merge_command)
    # index merged BAM file
    index_command = ['samtools', 'index', name]
    subprocess.run(index_command)

def merge_bam(neighbor_fileName, path):
    data = pd.read_csv(neighbor_fileName)
    center = data['Center'].values
    neighbors = data['Neighbors'].values

    bam_files_map = {}
    for val, neigh in zip(center, neighbors):
        if val not in bam_files_map:
            bam_files_map[val] = []
        bam_files_map[val].append(path + neigh + '.bam')

    with ThreadPoolExecutor(max_workers=30) as executor:
        for center, bam_files in bam_files_map.items():
            executor.submit(merge_bam_files, bam_files, center)

def sort_bams(directory):
    # Get list of all files in the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    # Sort files by size
    sorted_files = sorted(files, key=lambda x: os.path.getsize(os.path.join(directory, x)))
    sorted_files = [f for f in sorted_files if f.endswith('.bam')]
    
    return sorted_files

def process_bam_file(bam_file):
    command = f'sh bam2vcf.sh {MERGED_BAM_PATH}/{bam_file} {OUT_VCF_PATH} {REFERENCE}'
    print(command)
    subprocess.run(command, shell=True, check=True)

def main():
    # # calculate the distance
    print("calculating euclidian pixel >>>")
    cal_euclidian_pixel(RAD_LIM, NEIGHBOR_LIM, TISSUE_POS_PATH)
    # merge the bams
    print("MERGING BAMS >>>")
    merge_bam(NEIGHBOR_PIXEL_PATH, BAM_PATH)

    # Sort bams by size
    sorted_bam_files = sort_bams(MERGED_BAM_PATH)

    
    MAX_THREADS = 30
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(process_bam_file, sorted_bam_files)

if __name__ == "__main__":
    main()


# sh bam2vcf.sh ./data/merged_BAM/ACTTGACTGAGCACGA-1_merge.bam out_vcf /data/maiziezhou_lab/Softwares/refdata-GRCh38-2.1.0/fasta/genome.fa