def dfs(node, visited, list1, result):
    visited.append(node)
    result.append(node)
    for i in range(len(list1)):
        for j in range(len(list1[i])):
            if node in list1[i] and list1[i][j] not in visited:
                dfs(list1[i][j], visited, list1, result)
    return result

def get_combined_list(list1):
    visited =[]
    result = []
    for i in range(len(list1)):
        for j in range(len(list1[i])):
            if list1[i][j] not in visited:
                result.append(dfs(list1[i][j], visited ,list1,[]))
    return result

print(get_combined_list([['oranges','dogs', 'apples'],['peach', 'mango'],['dogs', 'cats']]))