import networkx as nx
import json
import statistics
import pandas as pd
from datetime import datetime

VERBOSE = True
DATA_DIRECTORY_PATH = "../../data/"
OUTPUT_FILE_PREFIX = "graphs_statistics"

def dfs_depth(G, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    depths = [dfs_depth(G, neighbor, visited.copy()) for neighbor in G.neighbors(node) if neighbor not in visited]
    return 1 + max(depths, default=0)

def collect_graph_stats(file_name):
    G = nx.DiGraph()

    with open(file_name, 'r') as graph_file:
        edge_list = json.load(graph_file)
        edge_list = [tuple(edge) for edge in edge_list]
        G.add_edges_from(edge_list)

    try:
        uG = G.to_undirected()
        if nx.is_connected(uG):
            diameter = nx.diameter(uG)
            avg_path_length = nx.average_shortest_path_length(uG)
            assortativity = nx.degree_assortativity_coefficient(uG)
            cycles = len(list(nx.cycle_basis(uG))) # simple_cycles for undirected
    except nx.NetworkXError as x:
        print(f"Exception: {x}")

    degrees = [deg for _, deg in G.degree()]

    if nx.is_directed_acyclic_graph(G):
        depth = dfs_depth(G, 1)
    else:
        depth = None

    return {
        "num_nodes": G.number_of_nodes(),
        "num_edges": G.number_of_edges(),
        "density": nx.density(G),
        "max_degree": max(degrees),
        "average_degree": statistics.mean(degrees),
        "median_degree": statistics.median(degrees),
        "diameter": diameter,
        "avg_path_length": avg_path_length,
        "assortativity": assortativity,
        "cycles": cycles,
        "depth": depth
    }

def display_graph_stats(graph_name, data):
    print(f'==== Statystyki Grafu {graph_name} ====')
    print(f"Liczba wierzchołków: {data['num_nodes']}")
    print(f"Liczba krawędzi: {data['num_edges']}")
    print(f"Gęstość grafu: {data['density']}")
    print(f"Maksymalny stopień wierzchołka: {data['max_degree']}")
    print(f"Średni stopień wierzchołka: {data['average_degree']}")
    print(f"Mediana stopnia wierzchołka: {data['median_degree']}")
    if data['diameter'] is not None:
        print(f"Średnica grafu: {data['diameter']}")
        print(f"Średnia długość ścieżki: {data['avg_path_length']}")
    else:
        print('Graf nie jest spójny – średnica i średnia długość ścieżki nie może być policzona.')
    print(f"Współczynnik asortatywności: {data['assortativity']}")
    print(f"Liczba cykli: {data['cycles']}")
    print(f"Głębokość: {data['depth']}")
    print()

def get_graph_file_path(data_path, medical_document, standard):
    return f"{data_path}{medical_document}/{standard}/results/graph.json"

def get_graph_name(medical_document, standard):
    return f"{medical_document}_{standard}"

if __name__ == "__main__":
    input_data = [
        ["recepta", "FHIR"],
        ["recepta", "OpenEHR"],
        ["skierowanie", "FHIR"],
        ["skierowanie", "OpenEHR"],
        ["wyniki_badan", "FHIR"],
        ["wyniki_badan", "OpenEHR"],
        ["pomiar", "FHIR"],
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
            final_stats[k] = round(v, 3) if isinstance(v, float) else v

        stats_list.append(final_stats)

    df = pd.DataFrame(stats_list)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = f"{OUTPUT_FILE_PREFIX}_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"Zapisano statystyki do pliku {filename}")

    cols_to_average = [
        "num_nodes", "num_edges", "density", "max_degree", 
        "average_degree", "median_degree", "diameter", 
        "avg_path_length", "assortativity", "cycles", "depth"
    ]
    grouped = df.groupby("standard")[cols_to_average].mean().reset_index()
    grouped = grouped.round(3)
    grouped_filename = f"{OUTPUT_FILE_PREFIX}_grouped_{timestamp}.csv"
    grouped.to_csv(grouped_filename, index=False)
    print(f"Zapisano statystyki zgrupowane do pliku {grouped_filename}")
