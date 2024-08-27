from dataclasses import dataclass
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

@dataclass
class GraphMetricts:
    avg_degree: float
    avg_shortest_path_length: float
    avg_clustering_coefficient: float

    def __str__(self) -> str:
        return f"Graph Metrics: \n" \
               f"  Average Degree: {self.avg_degree} \n" \
               f"  Characteristic Path Length: {self.avg_shortest_path_length} \n" \
               f"  Average Clustering Coefficient: {self.avg_clustering_coefficient}"
    

def create_network_from_csv(file_path: str) -> nx.Graph:
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Create a directed graph from the data
    G = nx.from_pandas_edgelist(df, source='source', target='target', create_using=nx.Graph())
    
    return G

def count_nodes_and_edges(G: nx.Graph) -> tuple:
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    return num_nodes, num_edges

def calculate_graph_metrics(G: nx.Graph) -> GraphMetricts:
    avg_degree = np.mean([degree for node, degree in G.degree()])
    
    return GraphMetricts(
        avg_degree=avg_degree,
        avg_shortest_path_length=nx.average_shortest_path_length(G), 
        avg_clustering_coefficient=nx.average_clustering(G)
    )


def plot_network_graph(G: nx.Graph):
    plt.figure()
    pos = nx.spring_layout(G)
    nodes = nx.draw_networkx_nodes(G, pos, alpha=0.8)
    nodes.set_edgecolor('k')
    nx.draw_networkx_labels(G, pos, font_size=8)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.2)
    plt.show()


def plot_degree_distribution(G: nx.Graph):
    degree_sequence = sorted([degree for node, degree in G.degree()], reverse=True)
    degree_count = pd.Series(degree_sequence).value_counts().sort_index()

    plt.figure(figsize=(10, 6))
    plt.bar(degree_count.index, degree_count.values, color='b', alpha=0.7)
    plt.title("Degree Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Number of Nodes")
    plt.show()

# Main Execution
if __name__ == "__main__":
    file_path = 'ego_sep24.csv'

    G = create_network_from_csv(file_path)

    num_nodes, num_edges = count_nodes_and_edges(G)
    print(f"Number of nodes: {num_nodes}")
    print(f"Number of edges: {num_edges}")

    metrics = calculate_graph_metrics(G)
    print(metrics)

    plot_network_graph(G)
    plot_degree_distribution(G)