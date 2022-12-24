def find_largest_integer(n):
    a_str = str(n)
    a_list = list(a_str)
    i = 0
    g = i+1
    result = []
    
    while i < len(a_list):
        if g < len(a_list):
            first, second = a_list[i], a_list[g]
            a_list[g], a_list[i] = first, second
            val = int("".join(a_list))
            if val < n:
                result.append(val)
                a_list = list(a_str)
            else:
                a_list = list(a_str)
            g += 1
        else:
            i += 1
            g = i + 1

    if result == []:
        return n

    return max(result)

print(find_largest_integer(8423))

def find_largest_integer(n):
    num_len = len(str(n))
    num_str = list(str(n))
    
    ind = s_digit = -1
 
    for i in range(num_len - 2, -1, -1):
        if int(num_str[i]) > int(num_str[i + 1]):
            ind = i
            break

    for i in range(num_len - 1, ind, -1):
        if (ind > -1 and int(num_str[i]) >= int(num_str[s_digit]) and int(num_str[i]) < int(num_str[ind])):
            s_digit = i

        elif (s_digit == -1 and int(num_str[i]) < int(num_str[ind])):
            s_digit = i
     
    if ind == -1:
        return int("". join("-1"))
    else:
        num_str[ind], num_str[s_digit] = num_str[s_digit], num_str[ind]

    return int("". join(num_str))

print(find_largest_integer(18256))
print(find_largest_integer(572))
