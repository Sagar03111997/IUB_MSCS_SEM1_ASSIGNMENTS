def dfs(node, g, visited, st, st1):
    if node in st1:
        return True
    if node in visited:
        return False
    visited.append(node)
    st1.append(node)
    for v in g[node]:
        if dfs(v, g, visited, st, st1):
                return True
    st.append(node)
    st1.remove(node)
    return False

def get_travel_plan(cities, priorities):
    city_dict = {}
    st1 = []
    visited = []
    st = []
    for c in cities:
        city_dict[c]=[]
    for u,v in priorities:
        city_dict[u].append(v)
    
    for c in city_dict:
        if c not in visited:
            if dfs(c, city_dict, visited, st, st1):
                return []
    for c in cities:
        if c not in st:
            st.append(c)
    return list(reversed(st))

print(get_travel_plan(["NY","IN"],[("NY","IN")]))
print(get_travel_plan(["NY","IN"],[("NY","IN"),("IN","NY")]))
print(get_travel_plan(['London', 'Berlin', 'Medellín', 'São Paulo', 'Prague', 'Ladakh', 'Nice'],[('London', 'Medellín'), ('Medellín', 'São Paulo'), ('Prague', 'Berlin')]))