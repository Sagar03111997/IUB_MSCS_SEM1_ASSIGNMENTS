def all_routes_to_dest(n ,connections, begin, end):
    adj_matrix = [[-1 for i in range(n)] for j in range(n)]

    for i in range(len(connections)):
        l, m = connections[i][0], connections[i][1]
        adj_matrix[l][m] = 1

    visited_nodes = [False for i in range(n)]
    queue = []
    queue.append(begin)
    result = 0
    count = 0

    while(queue):
        u = queue.pop(0)
        visited_nodes[u] = True
        if u == end:
            result += 1
            visited_nodes[u] = False

        for i in range(n):
            if adj_matrix[u][i] == 1 and visited_nodes[i] == False:
                queue.append(i)

    for i in range(n):
        if adj_matrix[begin][i] == 1:
            count += 1

    if result == count:
        return True
    return False

print(all_routes_to_dest(4, [[0,1],[0,2],[1,3],[2,3]], 0, 3))
print(all_routes_to_dest(4, [[0,1],[0,3],[1,2],[2,1]], 0, 3))