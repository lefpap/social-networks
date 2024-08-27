from dataclasses import dataclass
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

@dataclass
class GraphMetricts:
    avg_degree: float
    avg_shortest_path_length: float
    avg_clustering_coefficient: float

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
    avg_degree = sum(dict(G.degree()).values()) / G.number_of_nodes()
    try:
        avg_shortest_path_length = nx.average_shortest_path_length(G)
    except nx.NetworkXError:
        avg_shortest_path_length = float('inf')  # If the graph is disconnected
    avg_clustering_coefficient = nx.average_clustering(G)
    
    return GraphMetricts(
        avg_degree=avg_degree, 
        avg_shortest_path_length=avg_shortest_path_length, 
        avg_clustering_coefficient=avg_clustering_coefficient
    )


def plot_degree_distribution(G: nx.Graph):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    degree_count = pd.Series(degree_sequence).value_counts().sort_index()

    plt.figure(figsize=(10, 6))
    plt.bar(degree_count.index, degree_count.values, color='b')
    plt.title("Degree Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Number of Nodes")
    plt.savefig("degree_distribution.png")

    return degree_count

# Main Execution
if __name__ == "__main__":
    file_path = 'ego_sep24.csv'

    # Step 1: Create the network graph
    G = create_network_from_csv(file_path)
    
    # Step 2: Count the number of nodes and edges
    num_nodes, num_edges = count_nodes_and_edges(G)
    print(f"Number of nodes: {num_nodes}")
    print(f"Number of edges: {num_edges}")

    # Step 3: Calculate graph metrics
    metrics = calculate_graph_metrics(G)
    print("Graph Metrics:")
    print(f"  Average Degree: {metrics.avg_degree}")
    print(f"  Characteristic Path Length: {metrics.avg_shortest_path_length}")
    print(f"  Average Clustering Coefficient: {metrics.avg_clustering_coefficient}")

    # Step 4: Plot degree distribution
    degree_distribution = plot_degree_distribution(G)
    print("\nDegree Distribution:")
    print(degree_distribution)
