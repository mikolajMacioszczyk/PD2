import networkx as nx
import json
import statistics
import pandas as pd
from collections import deque
from utils import round_to_significant_figures

VERBOSE = True
DATA_DIRECTORY_PATH = "../../data/"
OUTPUT_FILE_PATH = "results/graphs_metrics.csv"
GROUPED_OUTPUT_FILE_PATH = "results/graphs_metrics_grouped.csv"

def avg_shortest_paths_from_root(G, root_node):
    lengths = nx.single_source_shortest_path_length(G, root_node)
    lengths_without_root = [l for node, l in lengths.items() if node != root_node]
    if lengths_without_root:
        return sum(lengths_without_root) / len(lengths_without_root)
    else:
        return 0

# def dfs_depth(G, node, visited=None):
#     if visited is None:
#         visited = set()
#     visited.add(node)
#     depths = [dfs_depth(G, neighbor, visited.copy()) for neighbor in G.neighbors(node) if neighbor not in visited]
#     return 1 + max(depths, default=0)

def bfs_depth(G, start):
    visited = set()
    queue = deque([(start, 0)])
    max_depth = 0

    while queue:
        node, depth = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        max_depth = max(max_depth, depth)
        for neighbor in G.neighbors(node):
            if neighbor not in visited:
                queue.append((neighbor, depth + 1))

    return max_depth

def collect_graph_stats(file_name):
    G = nx.DiGraph()
    root_node = 1

    with open(file_name, 'r') as graph_file:
        edge_list = json.load(graph_file)
        edge_list = [tuple(edge) for edge in edge_list]
        G.add_edges_from(edge_list)

    try:
        uG = G.to_undirected()
        if nx.is_connected(uG):
            diameter = nx.diameter(uG)
            assortativity = nx.degree_assortativity_coefficient(uG)
    except nx.NetworkXError as x:
        print(f"Exception: {x}")

    degrees = [deg for _, deg in G.degree()]

    if nx.is_directed_acyclic_graph(G):
        max_depth = bfs_depth(G, root_node)
    else:
        max_depth = None

    avg_path_from_root = avg_shortest_paths_from_root(G, root_node)

    return {
        "num_nodes": G.number_of_nodes(),
        "num_edges": G.number_of_edges(),
        "density": nx.density(G),
        "max_degree": max(degrees),
        "average_degree": statistics.mean(degrees),
        "avg_path_from_root": avg_path_from_root,
        "max_depth": max_depth,
        "diameter": diameter,
        "assortativity": assortativity,
    }

def display_graph_stats(graph_name, data):
    print(f'==== Statystyki Grafu {graph_name} ====')
    print(f"Liczba wierzchołków: {data['num_nodes']}")
    print(f"Liczba krawędzi: {data['num_edges']}")
    print(f"Gęstość grafu: {data['density']}")
    print(f"Maksymalny stopień wierzchołka: {data['max_degree']}")
    print(f"Średni stopień wierzchołka: {data['average_degree']}")
    print(f"Maksymalna głębokość: {data['max_depth']}")
    print(f"Średnia długość ścieżki od korzenia: {data['avg_path_from_root']}")
    if data['diameter'] is not None:
        print(f"Średnica grafu: {data['diameter']}")
        print(f"Współczynnik asortatywności: {data['assortativity']}")
    else:
        print('Graf nie jest spójny – średnica i średnia długość ścieżki nie może być policzona.')
    print()

def get_graph_file_path(data_path, medical_document, standard):
    return f"{data_path}{medical_document}/{standard}/results/graph.json"

def get_graph_name(medical_document, standard):
    return f"{medical_document}_{standard}"

def calculate_graphs_metrics():
    input_data = [
        ["recepta", "FHIR"],
        ["recepta", "OpenEHR"],
        ["skierowanie", "FHIR"],
        ["skierowanie", "OpenEHR"],
        ["wyniki_badan", "FHIR"],
        ["wyniki_badan", "OpenEHR"],
        ["pomiar", "FHIR"],
        ["pomiar", "OpenEHR"],
        ["iniekcja", "FHIR"],
        ["iniekcja", "OpenEHR"],
    ]

    stats_list = []
    for item in input_data:
        file_path = get_graph_file_path(DATA_DIRECTORY_PATH, item[0], item[1])
        stats = collect_graph_stats(file_path)
        graph_name = get_graph_name(item[0], item[1])
        
        if VERBOSE:
            display_graph_stats(graph_name, stats)

        final_stats = {}
        final_stats["graph_name"] = graph_name
        final_stats["medical_document"] = item[0]
        final_stats["standard"] = item[1]

        for k, v in stats.items():
            final_stats[k] = round_to_significant_figures(v, 3) if isinstance(v, float) else v

        stats_list.append(final_stats)

    df = pd.DataFrame(stats_list)
    df.to_csv(OUTPUT_FILE_PATH, index=False)
    print(f"Zapisano statystyki do pliku {OUTPUT_FILE_PATH}")

    cols_to_average = [
        "num_nodes", "num_edges", "density", "max_degree", 
        "average_degree", "avg_path_from_root", "max_depth",
        "diameter", "assortativity" 
    ]

    grouped = df.groupby("standard")[cols_to_average].agg(["mean", "var"]).reset_index()
    grouped.columns = [
        "standard" if col[0] == "standard" else f"{'avg_' if col[1]=='mean' else 'var_'}{col[0]}"
        for col in grouped.columns
    ]
    for col in grouped.columns:
        if col != "standard":
            grouped[col] = grouped[col].apply(lambda x: round_to_significant_figures(x, 3))
    grouped.to_csv(GROUPED_OUTPUT_FILE_PATH, index=False)
    print(f"Zapisano statystyki zgrupowane do pliku {GROUPED_OUTPUT_FILE_PATH}")

if __name__ == "__main__":
    calculate_graphs_metrics()