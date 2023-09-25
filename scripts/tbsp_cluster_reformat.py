import pandas as pd

NUM = '6'
# INPUT_PATH = f'./visual_data/GroupCells_{NUM}.txt'
OUTPUT_PATH = f'./visual_data/tbsp_{NUM}.txt'

# # Open the input and output files
# with open(INPUT_PATH, 'r') as infile, open(OUTPUT_PATH, 'w') as outfile:
#     # Loop through each line in the input file
#     for line in infile:
#         # Split the line on whitespace (default behavior of str.split())
#         parts = line.strip().split()
#         # Extract the desired parts of the line
#         cell_name = parts[0].replace('_merge', '')
#         cluster_num = parts[1].split(':')[-1]
#         # Write the reformatted line to the output file
#         outfile.write(f"{cell_name}:{cluster_num}\n")

# # Read the file into a list
# with open(OUTPUT_PATH , 'r') as f:
#     lines = f.readlines()

# # Sort the list
# lines.sort()

# # Write the sorted list back to the file
# with open(OUTPUT_PATH , 'w') as f:
#     f.writelines(lines)

"""
# Initialize lists to store cells and clusters
cells = []
clusters = []

# Read the file
with open(OUTPUT_PATH, 'r') as f:
    for line in f:
        # Split each line at the colon
        cell, cluster = line.strip().split(":")
        cells.append(cell)
        clusters.append(int(cluster))  # Convert cluster to integer

# Create the DataFrame
df = pd.DataFrame({
    'cell': cells,
    'cluster': clusters
})

df.to_csv(f"tbsp_{NUM}.csv", index = False)
"""

