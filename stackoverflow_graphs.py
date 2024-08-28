import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Constants
DATA_COUNT = 20_000
TIME_INTERVAL_SLICES = 4

def load_data():
    '''Φόρτωση των δεδομένων από το αρχείο και διαχωρισμός τους σε χρονικά διαστήματα'''
    
    # Φόρτωση των δεδομένων
    data = pd.read_csv('data\sx-stackoverflow-a2q.txt.gz', compression='gzip', sep=' ', header=None, names=['source', 'target', 'timestamp'])
    data = data.head(DATA_COUNT)
    
    # Διαχωρισμός των δεδομένων σε χρονικά διαστήματα
    time_intervals = pd.qcut(data['timestamp'], TIME_INTERVAL_SLICES, labels=False)
    data['time_interval'] = time_intervals
    
    return data


def create_graph_data(data):
    '''Δημιουργία γράφων από τα δεδομένα και υπολογισμός κόμβων και ακμών'''
   
    graphs = []
    node_counts = []
    edge_counts = []

    for i in range(TIME_INTERVAL_SLICES):
        # Φιλτράρισμα των δεδομένων για το τρέχον χρονικό διάστημα
        interval_data = data[data['time_interval'] == i]
        
        # Δημιουργία γράφου από τα δεδομένα
        G = nx.from_pandas_edgelist(interval_data, source='source', target='target', create_using=nx.DiGraph())
        graphs.append(G)
        
        # Σύνολο κόμβων και ακμών
        node_counts.append(G.number_of_nodes())
        edge_counts.append(G.number_of_edges())
    
    return graphs, node_counts, edge_counts


def plot_evolution_over_time(node_counts, edge_counts):
    '''Απεικόνιση της εξέλιξης των κόμβων και των ακμών με το χρόνο'''

    plt.figure(figsize=(10, 6))
    plt.plot(range(1, TIME_INTERVAL_SLICES + 1), node_counts, label='Number of Nodes')
    plt.plot(range(1, TIME_INTERVAL_SLICES + 1), edge_counts, label='Number of Edges')
    plt.xlabel('Time Interval')
    plt.ylabel('Count')
    plt.title('Evolution of Nodes and Edges Over Time')
    plt.legend()
    plt.show()


def plot_degree_distribution(graphs):
    '''Απεικόνιση της κατανομής των βαθμών των κόμβων για κάθε χρονικό διάστημα'''

    for i, G in enumerate(graphs):
        degrees = [G.degree(n) for n in G.nodes()]
        plt.figure(figsize=(10, 6))
        plt.hist(degrees, bins=30)
        plt.title(f'Degree Distribution for Interval {i + 1}')
        plt.xlabel('Degree')
        plt.ylabel('Frequency')
        plt.show()


def print_connected_components(graphs):
    '''Εκτύπωση του αριθμού των συνδεδεμένων συνιστωσών για κάθε χρονικό διάστημα'''

    for i, G in enumerate(graphs):
        if nx.is_connected(G.to_undirected()):
            print(f"Interval {i + 1}: All users are connected.")
        else:
            components = nx.number_connected_components(G.to_undirected())
            print(f"Interval {i + 1}: Number of connected components = {components}")


def print_common_nodes(graphs):
    '''Εκτύπωση του πλήθους των κοινών κόμβων μεταξύ διαδοχικών χρονικών διαστημάτων'''

    common_nodes = []
    for i in range(TIME_INTERVAL_SLICES - 1):
        common = len(set(graphs[i].nodes()).intersection(set(graphs[i + 1].nodes())))
        common_nodes.append(common)

    print("Common nodes between consecutive intervals:", common_nodes)


if __name__ == "__main__":
    # Φόρτωση και προετοιμασία των δεδομένων
    data = load_data()
    
    # Δημιουργία γράφων και υπολογισμός κόμβων και ακμών
    graphs, node_counts, edge_counts = create_graph_data(data)
    
    # Διάγραμμα εξέλιξης κόμβων και ακμών
    plot_evolution_over_time(node_counts, edge_counts)
    
    # Διάγραμμα κατανομής βαθμών
    plot_degree_distribution(graphs)
    
    # Έλεγχος σύνδεσης χρηστών και υπολογισμός συνδεδεμένων συνιστωσών
    print_connected_components(graphs)
    
    # Υπολογισμός πλήθους κοινών κόμβων
    print_common_nodes(graphs)
