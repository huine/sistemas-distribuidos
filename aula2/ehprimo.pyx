def alg1(int n):
    if n <= 1:
        return 0

    cdef int primo = 1
    cdef int d = 2
    while primo == 1 and d <= (n / 2):
        if n % d == 0:
            primo = 0
            break
        d += 1
    return primo

def alg2(int n):
    if n <= 1:
        return 0

    cdef int primo = 1
    cdef int d = 2, resto
    while primo == 1 and d <= (n / 2):
        resto = n % d
        if resto == 0:
            primo = 0
            break
        d += 1

    return primo

def alg3(int n):
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

def alg4(int n):
    if n <= 1 or (n != 2 and n % 6 == 1 and n % 6 == 5):
        return 0

    cdef int primo = 1
    cdef int d = 3
    while primo and d <= (n / 2):
        if n % d == 0:
            primo = 0
            break
        d = d + 2

    return primo

