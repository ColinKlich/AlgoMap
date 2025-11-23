# python3 -c "from graph_builder import build_city_graph; build_city_graph('Houston, Texas')"

import osmnx as ox
import networkx as nx
import json
import os
from encoder import CustomJSONEncoder

def get_graph_filename(place_name):
    return f"data/{place_name.lower().replace(', ', '_').replace(' ', '_')}.json"

def build_city_graph(place_name):
    print(f"Downloading: {place_name}")
    G = ox.graph_from_place(place_name, network_type="drive")
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)

    if not os.path.exists("data"):
        os.makedirs("data")

    data = nx.node_link_data(G, edges="edges")
    filename = get_graph_filename(place_name)
    with open(filename, "w") as f:
        json.dump(data, f, cls=CustomJSONEncoder)

    print(f"Graph saved to {filename}")
    return G

def get_graph_filename_from_point(lat, lon):
    return f"data/graph_{lat:.2f}_{lon:.2f}.json"

def build_graph_from_point(lat, lon, distance_km=10):
    print(f"Downloading graph for location: ({lat}, {lon})")
    G = ox.graph_from_point((lat, lon), dist=distance_km * 1000, network_type="drive")
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)

    if not os.path.exists("data"):
        os.makedirs("data")

    data = nx.node_link_data(G, edges="edges")
    filename = get_graph_filename_from_point(lat, lon)
    with open(filename, "w") as f:
        json.dump(data, f, cls=CustomJSONEncoder)

    print(f"Graph saved to {filename}")
    return G
