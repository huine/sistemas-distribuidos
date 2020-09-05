cpdef int alg3(int n):
    if n <= 1 or (n != 2 and n % 2 == 0):
        return 0

    cdef int primo = 1
    cdef int d = 3
    while primo and d <= (n / 2):
        if n % d == 0:
            primo = 0
            break
        d += 2

    return primo