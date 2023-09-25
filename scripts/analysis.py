import os
import matplotlib.pyplot as plt

NUM = '17'
SUM_SNP_PATH = f'../Ductal_processed_data/sum_snp_{NUM}.txt'
OUTPUT_FIG_PATH = f'../Ductal_processed_data/histogram_{NUM}.png'

# Initialize an empty list to store numbers
numbers = []

# Open the file in read mode
with open(SUM_SNP_PATH, "r") as file:
    for line in file:
        # Split the line at the colon and extract the second part
        num = int(line.split(":")[1].strip())
        numbers.append(num)

non_zeros = [v for v in numbers if v > 0]
print(len(non_zeros))

print("total number of spots: ", len(numbers))
print("the number of 0's: ", numbers.count(0))
print("max: ", max(numbers))
print("min: ", min(non_zeros))
print("average: ", sum(non_zeros)/len(non_zeros))


# Create a histogram
plt.hist(non_zeros, bins=20, edgecolor='black', alpha=0.7)

# Add title and labels
plt.title("Histogram of snps (" + NUM +") neighbors")
plt.xlabel("the number of snps")
plt.ylabel("number")

# Show the plot
plt.savefig(OUTPUT_FIG_PATH, dpi=1000, bbox_inches='tight')