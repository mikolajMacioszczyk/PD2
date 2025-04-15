import networkx as nx
import json
import statistics

DATA_DIRECTORY_PATH = "../../data/"

def get_graph_stats(file_name):
    G = nx.Graph() # DiGraph (diameter and avg_path_length not works)
    with open(file_name, 'r') as graph_file:
        edge_list = json.load(graph_file)
        edge_list = [tuple(edge) for edge in edge_list]
        G.add_edges_from(edge_list)

    if nx.is_connected(G):
        diameter = nx.diameter(G)
        avg_path_length = nx.average_shortest_path_length(G)
    else:
        diameter = None
        avg_path_length = None

    degrees = [deg for _, deg in G.degree()]

    return {
        "num_nodes": G.number_of_nodes(),
        "num_edges": G.number_of_edges(),
        "density": nx.density(G),
        "max_degree": max(degrees),
        "average_degree": statistics.mean(degrees),
        "median_degree": statistics.median(degrees),
        "diameter": diameter,
        "avg_path_length": avg_path_length,
        "assortativity": nx.degree_assortativity_coefficient(G)
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
    print()

def get_and_display_graph_stats(data_path, medical_document, standard):
    graph_stats = get_graph_stats(f"{data_path}{medical_document}/{standard}/results/graph.json")
    display_graph_stats(f"{medical_document} {standard}", graph_stats)

if __name__ == "__main__":
    get_and_display_graph_stats(DATA_DIRECTORY_PATH, "recepta", "FHIR")
    get_and_display_graph_stats(DATA_DIRECTORY_PATH, "recepta", "OpenEHR")
    get_and_display_graph_stats(DATA_DIRECTORY_PATH, "skierowanie", "FHIR")
    get_and_display_graph_stats(DATA_DIRECTORY_PATH, "skierowanie", "OpenEHR")
    get_and_display_graph_stats(DATA_DIRECTORY_PATH, "wyniki_badan", "FHIR")
    get_and_display_graph_stats(DATA_DIRECTORY_PATH, "wyniki_badan", "OpenEHR")
