from collections import deque
import time

def bfs(G, start, goal):
    start_time = time.perf_counter()

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

    visited = set()
    queue = deque([start])
    parent = {}
    steps = []

    goal_reached = False
    while queue:
        node = queue.popleft()
        steps.append(("visit", node))

        if node == goal:
            goal_reached = True
            break

        for nbr in G.neighbors(node):
            if nbr not in visited:
                visited.add(nbr)
                parent[nbr] = node
                queue.append(nbr)
                steps.append(("frontier", nbr))
    
    path = []
    if goal_reached:
        path = reconstruct_path(parent, start, goal)

    path_length = 0
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i+1]
        # We need to get the length of the edge. In a multigraph, we take the first one.
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
