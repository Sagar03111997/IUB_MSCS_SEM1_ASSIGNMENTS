# def shortest_superstring(array):
#     while(True):
#         if len(array) == 1:
#             break
#         max1 = -1
#         p1 , p2 = 0,0
#         result = ""
#         for i in range(len(array) - 1):
#             for j in range(i+1, len(array)):

#                 a, b = array[i], array[j]
#                 merged = super_string_helper(a, b)
#                 c = len(a) + len(b) - len(merged)

#                 if c > max1:
#                     max1 = c
#                     p1, p2 = i, j
#                     result = merged

#         str1 = array[p1]
#         str2 = array[p2]
#         array.remove(str1)
#         array.remove(str2)
#         array.append(result)

#     return array[0]

# def super_string_helper(s1,s2):
#     max1, max2 = 0, 0
#     count = 1

#     while len(s1) - count >= 0 and count <= len(s2):
#         if s1[len(s1)-count:] == s2[0:count]:
#             max1 = count
#         count += 1

#     count = 1
#     while len(s2) - count >=0 and count <= len(s1):
#         if s2[len(s1)-count:] == s1[0:count]:
#             max2 = count
#         count += 1
    
#     if max1 >= max2:
#         return s1[:len(s1)-max1] + s2

#     return s2[:len(s2)-max2] + s1

def shortest_superstring(array):
    while(True):
        if len(array) == 1:
            break
        max1 = -1
        p1 , p2 = 0,0
        result = ""
        for i in range(len(array) - 1):
            for j in range(i+1, len(array)):

                a, b = array[i], array[j]
                # merged = super_string_helper(a, b)

                max1, max2 = 0, 0
                count = 1

                while len(a) - count >= 0 and count <= len(b):
                    if a[len(a)-count:] == b[0:count]:
                        max1 = count
                    count += 1

                count = 1
                while len(b) - count >=0 and count <= len(a):
                    if b[len(a)-count:] == a[0:count]:
                        max2 = count
                    count += 1
                
                if max1 >= max2:
                    merged = a[:len(a)-max1] + b

                merged = b[:len(b)-max2] + a

                c = len(a) + len(b) - len(merged)

                if c > max1:
                    max1 = c
                    p1, p2 = i, j
                    result = merged

        str1 = array[p1]
        str2 = array[p2]
        array.remove(str1)
        array.remove(str2)
        array.append(result)

    return array[0]

# def super_string_helper(s1,s2):
#     max1, max2 = 0, 0
#     count = 1

#     while len(s1) - count >= 0 and count <= len(s2):
#         if s1[len(s1)-count:] == s2[0:count]:
#             max1 = count
#         count += 1

#     count = 1
#     while len(s2) - count >=0 and count <= len(s1):
#         if s2[len(s1)-count:] == s1[0:count]:
#             max2 = count
#         count += 1
    
#     if max1 >= max2:
#         return s1[:len(s1)-max1] + s2

#     return s2[:len(s2)-max2] + s1

print(shortest_superstring(["CATGC", "CTAAGT", "GCTA", "TTCA", "ATGCATC"]))