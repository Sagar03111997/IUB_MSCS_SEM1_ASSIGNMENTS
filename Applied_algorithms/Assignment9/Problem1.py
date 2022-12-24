def can_color(adj_matrix):
    color_list = [-1] * len(adj_matrix)
    color_list[0] = 1
    result = []
    result.append(0)

    while result:
        u = result.pop()
        if adj_matrix[u][u] == 1:
            return False
        for v in range(len(adj_matrix)):
            if adj_matrix[u][v] == 1 and color_list[v] == -1:
                color_list[v] = 1 - color_list[u]
                result.append(v)
            elif adj_matrix[u][v] == 1 and color_list[v] == color_list[u]:
                return False

    return True
    

print(can_color([[0,1,1,0], [1,0,0,1], [1,0,0,1],[0, 1, 1, 0]]))