from network import ServerTCP
from ehPrimo import alg3

def buscaPrimos(lista):
    """."""
    array = []
    for item in lista:
        if alg3(item) == 1:
            array.append(item)
    return array


def teste(item):
    item['response-teste'] = 20
    return item


if __name__ == "__main__":
    server = ServerTCP()
    server.function = buscaPrimos
    server.start()
