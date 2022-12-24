def SymmetricPairs(Array_Pairs):
    result_dict = {}
    result = []
    for num in Array_Pairs:
        if num[1] in result_dict and num[0] in result_dict[num[1]]:
            result.append([num[1],num[0]])
        else:
            if num[0] not in result_dict:
                result_dict[num[0]] = [num[1]]
            else:
                result_dict[num[0]].append(num[1])
    return result

print(SymmetricPairs([[11, 20], [40, 30], [10, 5]]))
print(SymmetricPairs([[11, 20], [30, 40], [5, 10], [40, 30], [10, 5]]))