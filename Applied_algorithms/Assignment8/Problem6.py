def find_circle_A(B):
    n = len(B)
    f = True

    if n % 3 == 2:
        f = False

    sum1 = 0
    for nums in B:
        sum1 += nums
    sum2 = sum1 / 3

    result1 = helper_find_circle_A(sum2, B, 0)
    result2 = helper_find_circle_A(sum2, B, 1)

    A = [0 for i in range(n)]

    if f:
        A[n-1] = result2
        A[n-2] = result1
    else:
        A[n-1] = B[n-2] - result1
        A[n-2] = result2 - A[n-1]

    A[0] = B[n-1] - A[n-1] - A[n-2]
    A[1] = B[0] - A[n-1] - A[0]

    for i in range(2, n-2):
        A[i] = B[i-1] - A[i-1] - A[i-2]

    return A

def helper_find_circle_A(result, B, i):
    while i < len(B) - 2:
        result -= B[i]
        i += 3
    return int(result)

print(find_circle_A([179,129,62,144,182]))