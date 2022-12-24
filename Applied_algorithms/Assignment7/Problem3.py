import heapq

def encode(s):

    frequency = {}
    encoded_string = ""

    for char in s:
        if char in frequency:
            frequency[char] += 1 
        else:
            frequency[char] = 1

    h = [[freq, [char, '']] for char, freq in frequency.items()]
    heapq.heapify(h)

    while len(h) != 1:
        first_min = heapq.heappop(h)
        second_min = heapq.heappop(h)

        for encoder1 in first_min[1:]:
            encoder1[1] = "0" + encoder1[1]

        for encoder2 in second_min[1:]:
            encoder2[1] = "1" + encoder2[1]

        heapq.heappush(h, [first_min[0] + second_min[0]] + first_min[1:] + second_min[1:])
    
    encoder = heapq.heappop(h)[1:]
    huffman_dictionary = {}

    for char in encoder:
        huffman_dictionary[char[0]] = char[1]

    encoded_string = ""
    for char in s:
        encoded_string += huffman_dictionary[char]

    return (encoded_string, huffman_dictionary)

def decode(s, d):
    d = {encode: char for char, encode in d.items()} 
    decoded_string = ""
    temp = ""

    for i in range(len(s)):
        temp += s[i]
        if temp in d:
            decoded_string += d[temp]
            temp = ""
            
    return decoded_string

s , d = encode("aabc")
print(s, d)
print(decode(s, d))
