from ehPrimo import alg3
from timeit import default_timer


def buscaPrimos(lista, lim):
    """."""
    r = []
    for item in lista:
        if len(r) >= lim:
            break

        if alg3(item) == 1:
            r.append(item)

    return r


if __name__ == '__main__':
    tmp = []
    for t in range(30):
        QTD = 222
        numeros = list(range(1, (140 * 71) + 1))
        start = default_timer()
        numeros.sort(reverse=True)
        saida = buscaPrimos(numeros, QTD)
        tmp.append(default_timer() - start)
        print(sum(saida[:QTD]))
        
    print('%.5f ms' % (1000 * (sum(tmp) / 30.0)))
