def maxEmployees(list1, list2):
    a = b = 0 
    list1 = merge_sort(list1)
    list2 = merge_sort(list2)

    n = len(list1)
    i = j = 0
    max_a = 0
    employee_sheet = []

    while i < n and j < n:
        if list1[i] < list2[j]:
            a += 1
            employee_sheet.append(a)
            i += 1
            if a > max_a:
                max_a = a
        elif list1[i] == list2[j]:
            a += 1
            employee_sheet.append(a)
            i += 1
            if a > max_a:
                max_a = a
            a -= 1
            j += 1
        elif list1[i] > list2[j]: 
            a -= 1
            j += 1
    a = max_a
    
    for emp in employee_sheet:
        if emp == max_a:
            b += 1
                  
    return (a,b)

def merge_sort(array):
    if len(array) == 1:
        return array
    else:
        mid = len(array) // 2
        left = array[:mid]
        right = array[mid:]
    
        merge_sort(left)
        merge_sort(right)
        
        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                array[k] = left[i]
                i += 1
            else:
                array[k] = right[j]
                j += 1
            k += 1
        
        while i < len(left):
            array[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            array[k] = right[j]
            j += 1
            k += 1

        return array
    
print(maxEmployees([1, 2, 4, 7, 8, 12], [3, 7, 8, 12, 10, 15 ]))