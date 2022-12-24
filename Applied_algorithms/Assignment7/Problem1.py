
import heapq

def additional_seats(k, h):
    h.sort(key = lambda x: x[1])

    heap = []

    for trip in h:
        riders, start, end = trip

        if heap:
            while heap and start >= heap[0][0]:
                end, in_car = heapq.heappop(heap)
                k += in_car

        if riders > k:
            return False
        
        k -= riders
        heapq.heappush(heap, [end, riders])
        
    return True

print(additional_seats(4, [[2,1,5],[3,3,7]]))



# import heapq

# def additional_seats(max_seats, h):
#     heap = []

#     for start, end in h:
#         heapq.heappush(heap, (start,1))
#         heapq.heappush(heap, (end, -1))

#     additional_seats = 0
#     seats_occupied = 0

#     for i in range(len(heap)):
#         x = heapq.heappop(heap)
#         seats_occupied += x[1]
#         if seats_occupied > max_seats:
#             additional_seats += 1

#     return additional_seats

# print(additional_seats(2, [[0,2],[1,2],[0,3],[2,3]]))