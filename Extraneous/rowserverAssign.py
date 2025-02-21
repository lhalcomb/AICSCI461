def distribute_rows(servers, customers_per_row):
    # Initialize servers with empty lists and zero loads
    server_loads = [0] * servers
    server_rows = [[] for _ in range(servers)]

    # Pair rows with customer counts and sort descending
    rows = sorted(enumerate(customers_per_row, start=1), key=lambda x: -x[1])

    # Greedy balancing algorithm
    for row, customers in rows:
        # Find the server with the least load
        min_server = min(range(servers), key=lambda i: server_loads[i])
        # Assign row to that server
        server_rows[min_server].append(row)
        server_loads[min_server] += customers

    return server_rows, rows, server_loads

# Example input
servers = 2
customers_per_row = [2, 0, 8, 5, 1]

# Get the row assignments
assignments, rows, server_loads = distribute_rows(servers, customers_per_row)
print(rows) 
print('\n')
print(server_loads)

# Output the assignments
for i, rows in enumerate(assignments, start=1):
    print(f"Server {i}: Rows {rows}")
