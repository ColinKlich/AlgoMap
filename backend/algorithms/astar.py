import heapq
from geopy.distance import geodesic
import time

def heuristic(a, b, G):
    c1 = (G.nodes[a]["y"], G.nodes[a]["x"])
    c2 = (G.nodes[b]["y"], G.nodes[b]["x"])
    return geodesic(c1, c2).meters

def reconstruct_path(parent, start, goal):
    path = []
    cur = goal
    while cur != start:
        if cur not in parent:
            return []
        path.append(cur)
        cur = parent[cur]
    path.append(start)
    return path[::-1]


def astar(G, start, goal):
    start_time = time.perf_counter()

    pq = [(0, start)]
    g_cost = {node: float("inf") for node in G.nodes()}
    g_cost[start] = 0
    parent = {}
    steps = []

    goal_reached = False
    while pq:
        _, node = heapq.heappop(pq)
        steps.append(("visit", node))

        if node == goal:
            goal_reached = True
            break

        for nbr in G.neighbors(node):
            w = G[node][nbr][0]["length"]
            new_g = g_cost[node] + w

            if new_g < g_cost[nbr]:
                g_cost[nbr] = new_g
                f = new_g + heuristic(nbr, goal, G)
                parent[nbr] = node
                heapq.heappush(pq, (f, nbr))
                steps.append(("frontier", nbr))

    path = []
    if goal_reached:
        path = reconstruct_path(parent, start, goal)

    path_length = 0
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i+1]
        edge_data = G.get_edge_data(u, v)
        if edge_data:
            key = list(edge_data.keys())[0]
            path_length += edge_data[key].get('length', 0)

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    return {
        "steps": steps,
        "path": path,
        "time": execution_time,
        "length": path_length,
    }
