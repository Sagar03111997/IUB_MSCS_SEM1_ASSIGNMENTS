# def max_moves(nums: list) -> int:
#     maxmoves = 0

#     while (nums[-1] != 0 or nums[-2] != 0):
#         nums.sort()

#         if (nums[0] == 0 and (nums[-1] == 0 or nums[-2] == 0)):
#             break

#         nums[-1] = nums[-1] - 1
#         nums[-2] = nums[-2] - 1
#         maxmoves = maxmoves + 1

#     return maxmoves


# print(max_moves([4,4,6]))
# print(max_moves([2,4,6]))
# print(max_moves([5,1,1]))

from queue import PriorityQueue 
import heapq

class Max_heapify(object):

    def __init__(self, z):
        self.z = z

    def __lt__(self, other):
        return self.z > other.z

    def __str__(self):
        return str(self.z)

def max_moves(nums: list) -> int:
    
    queue = PriorityQueue()
    maxmoves = 1
    
    for i in nums:        
        queue.put(Max_heapify(i))
        
    while True:
        a = queue.get()
        b = queue.get()

        queue.put(Max_heapify(a.z - 1))
        queue.put(Max_heapify(b.z -1))

        if queue.queue[1].z == 0:
            break
        maxmoves += 1

    return maxmoves

print(max_moves([4,4,6]))
print(max_moves([2,4,6]))
print(max_moves([5,1,1]))
