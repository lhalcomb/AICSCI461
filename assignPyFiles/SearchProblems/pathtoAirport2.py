import heapq

def a_star(node_connections, start, end):
    # Create a graph from the connections dictionary
    graph = {}
    for (node1, node2), distance in node_connections.items():
        if node1 not in graph:
            graph[node1] = []
        if node2 not in graph:
            graph[node2] = []
        graph[node1].append((node2, distance))
        graph[node2].append((node1, distance))  # Assuming undirected graph

    # Heuristic function (straight-line distance, set to 0 for simplicity)
    def heuristic(node):
        return 0

    # Priority queue for A*
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))

    # Cost to reach each node
    g_cost = {start: 0}

    # To reconstruct the path
    came_from = {}

    while priority_queue:
        current_cost, current_node = heapq.heappop(priority_queue)

        # If we reach the goal, reconstruct and return the path
        if current_node == end:
            path = []
            while current_node:
                path.append(current_node)
                current_node = came_from.get(current_node)
            return path[::-1]  # Reverse the path to get start -> end

        # Explore neighbors
        for neighbor, distance in graph[current_node]:
            tentative_g_cost = g_cost[current_node] + distance

            # If this path to the neighbor is better, record it
            if neighbor not in g_cost or tentative_g_cost < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g_cost
                f_cost = tentative_g_cost + heuristic(neighbor)
                heapq.heappush(priority_queue, (f_cost, neighbor))
                came_from[neighbor] = current_node

    # If we exhaust the priority queue without finding the end, return failure
    return None

# Example usage
node_connections = {
    ("1", "10"): 0.7, 
    ("1", "9"): 1.3, 
    ("2", "3"): 1.5, 
    ("3", "4"): 2.4, 
    ("3", "2"): 1.5,
    ("3", "7"): 2.3,
    ("3", "13"): 4.0, 
    ("4", "5"): 4.0, 
    ("4", "7"): 0.7, 
    ("4", "3"): 2.4,
    ("5", "6"): 2.1, 
    ("5", "8"): 0.8, 
    ("5", "4"): 4.0,
    ("6", "12"): 1.8, 
    ("7", "9"): 1.9, 
    ("7", "8"): 4.7,
    ("7", "3"): 2.3, 
    ("8", "11"): 1.8, 
    ("8", "7"): 4.7,
    ("9", "14"): 2.3,
    ("9", "7"): 1.9, 
    ("10", "11"): 0.8, 
    ("10", "15"): 2.2, 
    ("11", "12"): 2.7, 
    ("11", "16"): 2.3, 
    ("11", "17"): 4.3, 
    ("12", "17"): 3.0, 
    ("13", "14"): 1.5, 
    ("14", "15"): 2.3, 
    ("15", "16"): 0.8, 
    ("15", "19"): 1.7, 
    ("16", "17"): 2.9, 
    ("16", "20"): 1.5, 
    ("17", "21"): 1.6, 
    ("18", "14"): 1.5, 
    ("18", "19"): 2.1, 
    ("19", "20"): 0.9, 
    ("20", "21"): 2.1, 
}

start = "1"
end = "2"
path = a_star(node_connections, start, end)
print("Path:", path)
print("Total Cost:", sum(node_connections.get((path[i], path[i + 1]), 0) for i in range(len(path) - 1)))
print( 1.3 + 1.9 + 2.3 + 1.5)
