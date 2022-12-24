from heapq import heappop, heappush

def minimum_range(lists):
    p_queue = []
    maxi = 0
        
    for i in range(len(lists)): 
        heappush(p_queue, (lists[i][0] , i, 0))
        maxi = max(maxi , lists[i][0])
        
    ans = [p_queue[0][0] , maxi]

    while True:
        k, i, j = heappop(p_queue)
              
        if j == len(lists[i]) - 1:
            break
                
        next_num = lists[i][j+1]
        maxi = max(maxi, next_num)
            
        heappush(p_queue, (next_num, i, j+1))
            
        if maxi - p_queue[0][0] < ans[1] - ans[0]:
            ans = [p_queue[0][0], maxi]

    return tuple(ans)

print(minimum_range([[ 3, 6, 8, 10, 15],[ 1, 5, 12 ],[ 4, 8, 15, 16 ],[ 2, 6 ]]))
print(minimum_range([[ 2, 3, 4, 8, 10, 15 ],[ 1, 5, 12 ],[ 7, 8, 15, 16 ],[ 3, 6 ]]))