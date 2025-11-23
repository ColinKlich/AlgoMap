import time
import requests
import json

def osrm(G, start_node, end_node):
    """
    Calls the public OSRM API to get a route.
    The graph G is used only to get the coordinates of the start and end nodes.
    """
    start_time = time.time()

    start_coords = G.nodes[start_node]
    end_coords = G.nodes[end_node]
    
    lon1, lat1 = start_coords['x'], start_coords['y']
    lon2, lat2 = end_coords['x'], end_coords['y']

    url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson"

    path = []
    path_geometry = []
    distance = 0
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get('code') == 'Ok' and data.get('routes'):
            route = data['routes'][0]
            distance = route['distance'] # in meters
            
            # The path geometry from OSRM is a GeoJSON LineString
            geometry = route['geometry']['coordinates']
            # OSRM returns [lon, lat], which is what our frontend expects as [x, y]
            # The path_geometry is a list of segments, so we just wrap it in a list.
            path_geometry = [geometry]
            
            # Create a dummy path with the correct length for the table
            path = [0] * (len(geometry) - 1) if len(geometry) > 1 else []

    except Exception as e:
        print(f"OSRM API request failed: {e}")
        path_geometry = []

    end_time = time.time()
    
    # OSRM doesn't give us a path of nodes from our graph,
    # so we return a dummy path for 'path' and 'visited'.
    # The important part is the path_geometry.
    return {
        "path": path,
        "time": (end_time - start_time) * 1000,
        "visited": 0,
        "distance": distance * 0.000621371, # convert to miles
        "path_geometry": path_geometry
    }
