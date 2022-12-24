 
from sys import maxsize
 
# Function to find the maximum contiguous subarray
# and print its starting and end index
 
 
def maxSubArraySum(data):
    result = []
 
    max_so_far = -maxsize - 1
    max_ending_here = 0
    start = 0
    end = 0
    s = 0
 
    for i in range(len(data)):
 
        max_ending_here += data[i]
 
        if max_so_far < max_ending_here:
            max_so_far = max_ending_here
            start = s
            end = i
 
        if max_ending_here < 0:
            max_ending_here = 0
            s = i+1
    result.append
 
 
# Driver program to test maxSubArraySum
a = [-2, -3, 4, -1, -2, 1, 5, -3]
maxSubArraySum(a, len(a))