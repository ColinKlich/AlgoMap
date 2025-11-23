import time
import networkx as nx

def bidirectional_dijkstra(G, start, end):
    """
    Wrapper for networkx's bidirectional_dijkstra.
    """
    start_time = time.time()
    
    try:
        # bidirectional_dijkstra returns length and path
        length, path = nx.bidirectional_dijkstra(G, start, end, weight='travel_time')
    except nx.NetworkXNoPath:
        path = []

    end_time = time.time()
    
    # bidirectional_dijkstra does not expose the number of visited nodes.
    # We will return 0 as a placeholder.
    return {
        "path": path,
        "time": (end_time - start_time) * 1000,
        "visited": 0, # Placeholder
    }
