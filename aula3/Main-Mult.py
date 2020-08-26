from random import shuffle
from multiprocessing import Queue, Process, cpu_count
from itertools import islice
from ehPrimo import alg3
from timeit import default_timer


def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


def buscaPrimos(lista):
    """."""
    for item in lista:
        if alg3(item) == 1:
            Q.put_nowait(item)

if __name__ == '__main__':
    tmp = []
    # for t in range(30):
    QTD = 222
    numeros = list(range(1, (140 * 71) + 1))
    shuffle(numeros)
    Q = Queue()
    jobs = []
    start = default_timer()
    for i in list(chunk(numeros, (len(numeros)//cpu_count() + 1))):
        P = Process(target=buscaPrimos, args=(i, ))
        jobs.append(P)
        P.start()

    for proc in jobs:
        proc.join()

    primos = []
    while Q.empty() is False:
        primos.append(Q.get())
    primos.sort()
    tmp.append(default_timer() - start)
    with open('lista_primos.txt', 'w') as f:
        f.write(str(primos))
        
    print('%.5f ms' % (1000 * (sum(tmp) / 30.0)))
