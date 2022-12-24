def partition(num_list, left, right):

    pivot = left + (right - left) // 2
    num_list[left],num_list[pivot] = num_list[pivot], num_list[left] 
    pivot = left
    left += 1

    while right >= left :
        while left <= right and num_list[left] <= num_list[pivot]:
            left += 1
        while left <= right and num_list[right] > num_list[pivot]:
            right -= 1

        if left <= right:
            num_list[left] , num_list[right] = num_list[right], num_list[left] 
            left += 1
            right -= 1
        else:
            break

    num_list[pivot], num_list[right] = num_list[right] , num_list[pivot]

    return right


def quicksort_helper(num_list ,left, right):
    if left >= right:
        return  
    if right - left == 1:
        if num_list[right] < num_list[left]:
            num_list[right], num_list[left] = num_list[left] , num_list[right]
            return           

    pivot = partition(num_list, left, right)

    quicksort_helper(num_list, left, pivot -1)
    quicksort_helper(num_list, pivot+1,right) 

    return num_list        

def quicksort(num_list):
    return quicksort_helper(num_list, 0, len(num_list) - 1)

num_list = [3,7,2,8,1,6,8,9,6,9]
print(quicksort(num_list))
num_list = [7,7,3,2,1]
print(quicksort(num_list))


