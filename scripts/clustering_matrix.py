import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE

NUM = "6"

DATA_PATH = f'../processed_data/matrix_{NUM}.pkl'
OUTPUT_PATH = f'../processed_data/clutering_{NUM}.png'



def plot(df):
    # Use KMeans to cluster cells
    kmeans = KMeans(n_clusters=10, random_state=0).fit(df)
    df['cluster'] = kmeans.labels_

    # Use t-SNE for dimensionality reduction
    tsne = TSNE(n_components=2, random_state=0)
    tsne_results = tsne.fit_transform(df.iloc[:, :-1])  # Excluding the 'cluster' column

    # Plot the results
    plt.scatter(tsne_results[:, 0], tsne_results[:, 1], c=df['cluster'], cmap='viridis')
    plt.colorbar()
    plt.title(f'Clustering of {NUM} neighbors')
    plt.xlabel('N/A')
    plt.ylabel('N/A')
    plt.savefig(OUTPUT_PATH, dpi=1000)

def main():
    df = pd.read_pickle(DATA_PATH)
    plot(df)

main()