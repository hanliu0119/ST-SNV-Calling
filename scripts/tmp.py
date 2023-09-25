import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

TISSUE_POS_PATH = '/data/maiziezhou_lab/Datasets/ST_datasets/10x_BC_6.5mm_Visium_CytAssist_FFPE/spatial/tissue_positions.csv'
raw_data = pd.read_csv(TISSUE_POS_PATH)

neighbors = ['GCAGTACTCAACGAAG-1', 'TCAATTATACCAGAAC-1', 'AGTGTATGCGCTGCCT-1']

def get_pos(cell):
    filter_df = raw_data[raw_data["barcode"] == cell]
    return [filter_df["pxl_row_in_fullres"].tolist()[0], filter_df["pxl_col_in_fullres"].tolist()[0]]

data = []
for n in neighbors:
    data += [get_pos(n)]

print(data)


def calculate_angle(A, B, C):
    # Function to compute the angle between point A and the line BC
    BA = A - B
    BC = C - B
    cosine_angle = np.dot(BA, BC) / (np.linalg.norm(BA) * np.linalg.norm(BC))
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)

# Unpack the x and y coordinates
vertices = data
x, y = zip(*vertices)
x = list(x)
y = list(y)

# Close the triangle by adding the first vertex again
x.append(vertices[0][0])
y.append(vertices[0][1])

# Plot the triangle with vertices
plt.plot(x, y, '-o')  # '-o' specifies that we want lines and dots

# Calculate and display angles inside the triangle
A, B, C = np.array(vertices)
angle_A = round(calculate_angle(B, A, C), 2)
angle_B = round(calculate_angle(C, B, A), 2)
angle_C = round(calculate_angle(A, C, B), 2)

plt.annotate(f"{angle_A}°", A + [50, -50], fontsize=10, color='red')
plt.annotate(f"{angle_B}°", B + [-150, 0], fontsize=10, color='red')
plt.annotate(f"{angle_C}°", C + [50, 50], fontsize=10, color='red')

# Show plot
plt.grid(True)
# Labeling and displaying the plot
plt.title("Tissue_position")
plt.xlabel("pxl_col_in_fullres")
plt.ylabel("pxl_row_in_fullres")

plt.savefig("scatter_plot_6.png", dpi=1000)