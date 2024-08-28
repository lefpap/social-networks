from dataclasses import dataclass
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

@dataclass
class GraphMetrics:
    avg_degree: float
    avg_shortest_path_length: float
    avg_clustering_coefficient: float

    def __str__(self) -> str:
        return (f"Graph Metrics: \n"
                f"  Average Degree: {self.avg_degree:.2f} \n"
                f"  Characteristic Path Length: {self.avg_shortest_path_length:.2f} \n"
                f"  Average Clustering Coefficient: {self.avg_clustering_coefficient:.2f}")

def create_network_from_csv(file_path: str) -> nx.Graph:
    '''Δημιουργία ενός κατευθυνόμενου γράφου από τα δεδομένα του αρχείου CSV'''
   
    df = pd.read_csv(file_path)
    G = nx.from_pandas_edgelist(df, source='source', target='target', create_using=nx.Graph())
    
    return G

def count_nodes_and_edges(G: nx.Graph) -> tuple:
    '''Καταμέτρηση των κόμβων και των ακμών στο γράφο'''

    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    return num_nodes, num_edges

def calculate_graph_metrics(G: nx.Graph) -> GraphMetrics:
    '''Υπολογισμός των μετρικών του γράφου'''
    avg_degree = np.mean([degree for node, degree in G.degree()])
    
    return GraphMetrics(
        avg_degree=avg_degree,
        avg_shortest_path_length=nx.average_shortest_path_length(G),
        avg_clustering_coefficient=nx.average_clustering(G)
    )

def plot_network_graph(G: nx.Graph):
    '''Απεικόνιση γράφου'''
    plt.figure()
    pos = nx.spring_layout(G)
    nodes = nx.draw_networkx_nodes(G, pos, alpha=0.8)
    nodes.set_edgecolor('k')
    nx.draw_networkx_labels(G, pos, font_size=8)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.2)
    plt.show()

def plot_degree_distribution(G: nx.Graph):
    '''Απεικόνιση της κατανομής των βαθμών των κόμβων'''
    degree_sequence = sorted([degree for node, degree in G.degree()], reverse=True)
    degree_count = pd.Series(degree_sequence).value_counts().sort_index()

    plt.figure(figsize=(10, 6))
    plt.bar(degree_count.index, degree_count.values, color='b', alpha=0.7)
    plt.title("Degree Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Number of Nodes")
    plt.show()

if __name__ == "__main__":
    file_path = 'data/ego_sep24.csv'

    # 1) Δημιουργία του γράφου από το CSV
    G = create_network_from_csv(file_path)

    # 2) Καταμέτρηση των κόμβων και ακμών στο δίκτυο
    num_nodes, num_edges = count_nodes_and_edges(G)
    print(f"Number of nodes: {num_nodes}")
    print(f"Number of edges: {num_edges}")

    # 3) Υπολογισμός και εμφάνιση των μετρικών του γράφου
    metrics = calculate_graph_metrics(G)
    print(metrics)

    # 1) Απεικόνιση του γράφου
    plot_network_graph(G)

    # 4) Απεικόνιση της κατανομής των βαθμών και παρατηρήσεις
    plot_degree_distribution(G)
