def merge(parent, rank_array, x, y):
    if rank_array[x] < rank_array[y]:
        parent[x] = y
    elif rank_array[x] > rank_array[y]:
        parent[y] = x
    else:
        parent[y] = x
        rank_array[x] += 1

def get_min_cost(n, costs):

    costs = sorted(costs, key = lambda item: item[2])
    traversed =[]
    e = 0
    ans = 0

    for i in range(len(costs)):
        costs[i][0] -= 1
        costs[i][1] -= 1

    parent_list = [i for i in range(n)]
    result = [0 for i in range(n)]
    
    for i in range(len(costs)):
        if e == n-1:
            break

        p, c, l = costs[i]
        p1, p2 = p, c

        while parent_list[p] != p:
            p = parent_list[p]

        while parent_list[c] != c:
            c = parent_list[c]

        if p != c:
            e += 1
            traversed.append((p1, p2, l))
            merge(parent_list, result, p1, p2)

    if len(traversed) != n - 1:
        return -1

    for i in range(len(traversed)):
        _, _, v = traversed[i]
        ans += v
    return ans
  
print(get_min_cost(n = 4, costs = [[1,2,3],[3,4,4]]))
print(get_min_cost(n = 3, costs = [[1,2,4],[1,3,9],[2,3,7]]))