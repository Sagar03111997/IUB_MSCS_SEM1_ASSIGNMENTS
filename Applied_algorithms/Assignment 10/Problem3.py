def custom_dict(queries, values):
    result_dict = {}
    key, value = 0, 0
    result = []
    for i in range(len(queries)):
        if queries[i] == "Add":
            result_dict[values[i][0]-key] = values[i][1] - value
        elif queries[i] == "Return":
            result.append(result_dict[values[i][0]-key] + value)
        elif queries[i] == "Add_to_keys":
            key += values[i][0]
        elif queries[i] == "Add_to_vals":
            value += values[i][0]
    return result

print(custom_dict(["Add", "Add_to_vals", "Return", "Add", "Add_to_keys", "Add_to_vals", "Return"], [[1,2],[2],[1],[2,3],[1],[-1],[3]]))