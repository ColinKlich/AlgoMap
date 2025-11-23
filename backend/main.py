# uvicorn main:app --reload --port 8000

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import networkx as nx
import os
import osmnx as ox
from geopy.geocoders import Nominatim

from algorithms.bfs import bfs
from algorithms.dijkstra import dijkstra
from algorithms.astar import astar
from algorithms.osrm import osrm
from graph_builder import build_graph_from_point, get_graph_filename_from_point

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

G = None
geolocator = Nominatim(user_agent="AlgoMap", timeout=10)

@app.get("/geocode")
def geocode(q: str):
    location = geolocator.geocode(q)
    if location:
        return {"lat": location.latitude, "lon": location.longitude}
    return {"error": "Location not found"}


@app.get("/graph")
def get_graph(lat: float, lon: float):
    global G
    filename = get_graph_filename_from_point(lat, lon)

    if os.path.exists(filename):
        with open(filename) as f:
            G = nx.node_link_graph(json.load(f), edges="edges")
        print(f"Loaded graph from {filename}")
    else:
        G = build_graph_from_point(lat, lon)

    return {"nodes": G.nodes}


# In main.py, update the /nearest-node endpoint
@app.get("/nearest-node")
def get_nearest_node(lat: float, lon: float):
    if G is None:
        return {"node": None, "error": "Graph not loaded"}
    try:
        node = ox.distance.nearest_nodes(G, lon, lat)
        if isinstance(node, (list, tuple)) and len(node) > 0:
            node = node[0]  # Take the first node if it returns a list
        return {"node": node}
    except Exception as e:
        print(f"Error finding nearest node: {e}")
        return {"node": None, "error": str(e)}

@app.post("/run")
def run(payload: dict):
    if G is None:
        return {"error": "Graph not loaded"}
        
    start = payload["start"]
    end = payload["end"]

    results = {}
    for algo_name, algo_func in [("bfs", bfs), ("dijkstra", dijkstra), ("astar", astar), ("osrm", osrm)]:
        result = algo_func(G, start, end)

        if algo_name == "osrm":
            # OSRM result is already processed
            results[algo_name] = result
            continue

        path = result["path"]
        
        path_geometry = []
        total_distance_meters = 0
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i+1]
            edge_data = G.get_edge_data(u, v)
            if edge_data:
                # Find the edge with the minimum length, in case of parallel edges
                min_length_edge = min(edge_data.values(), key=lambda x: x['length'])
                total_distance_meters += min_length_edge['length']
                
                if 'geometry' in min_length_edge:
                    geometry = min_length_edge['geometry']
                    if hasattr(geometry, 'coords'):  # It's a LineString
                        path_geometry.append(list(geometry.coords))
                    else:  # It's already a list
                        path_geometry.append(geometry)
        
        result["path_geometry"] = path_geometry
        result["distance"] = total_distance_meters * 0.000621371 # convert to miles
        results[algo_name] = result

    return results
