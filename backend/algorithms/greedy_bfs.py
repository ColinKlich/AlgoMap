import time
import networkx as nx
from geopy.distance import great_circle

def heuristic(G, u, v):
    """
    Heuristic function for Greedy Best-First Search (great-circle distance).
    """
    return great_circle((G.nodes[u]['y'], G.nodes[u]['x']), (G.nodes[v]['y'], G.nodes[v]['x'])).kilometers

def greedy_bfs(G, start, end):
    """
    Greedy Best-First Search algorithm.
    """
    start_time = time.time()
    
    visited = set()
    # Priority queue: (heuristic_value, node)
    pq = [(heuristic(G, start, end), start)]
    # Path reconstruction dictionary
    parent = {start: None}

    path_found = False
    while pq:
        # Get the node with the smallest heuristic value
        _, current_node = min(pq, key=lambda x: x[0])
        pq = [item for item in pq if item[1] != current_node]

        if current_node == end:
            path_found = True
            break

        if current_node in visited:
            continue
        
        visited.add(current_node)

        for neighbor in G.neighbors(current_node):
            if neighbor not in visited:
                parent[neighbor] = current_node
                pq.append((heuristic(G, neighbor, end), neighbor))

    end_time = time.time()

    path = []
    if path_found:
        node = end
        while node is not None:
            path.insert(0, node)
            node = parent[node]

    return {
        "path": path,
        "time": (end_time - start_time) * 1000,  # in milliseconds
        "visited": len(visited),
    }
