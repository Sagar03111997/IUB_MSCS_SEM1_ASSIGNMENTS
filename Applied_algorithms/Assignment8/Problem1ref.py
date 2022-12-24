def maxEmployees(list1, list2):
    list1.sort()
    list2.sort()

    j = 0
    i = 0
    count = 0
    result = []
    final = []
    temp1 = []

    while True:
        if list1[i] <= list2[j]:
            count += 1
            result.append(list1[i])
            result.append(count)
            final.append(result)
            result = []
            i += 1
        elif list1[i] > list2[j]:
            count -= 1
            temp = final.pop()
            temp1.append(temp[-2])
            temp1.append(temp[-1])
            temp[-2], temp[-1] = list2[j], count
            final.append(temp1)
            temp1 = []
            final.append(temp)
            j += 1
        

print(maxEmployees([1, 2, 4, 7, 8, 12], [3, 8, 7, 12, 10, 15]))