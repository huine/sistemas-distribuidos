from network import ClientTCP
from multiprocessing import Process, cpu_count, Array
from itertools import islice
from random import shuffle, randint
from timeit import default_timer


def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


class client(ClientTCP):
    """."""

    def __init__(self, lista):
        """."""
        self.lista = lista
        super().__init__()

    def inicia(self):
        """."""
        super().connect()
        super().send(self.lista)
        response = super().receive()
        return response

    def parse_multiprocessing(self, results):
        """."""
        response = self.inicia()
        for i in range(len(response[0])):
            results[i] = response[0][i]


if __name__ == "__main__":
    # c = client(lista={})
    # print(c.inicia())
    # tmp = []
    # for j in range(30):
    # numeros = list(range(1, (140 * 71) + 1))
    numeros = list(range(500000))
    shuffle(numeros)
    clients = []
    jobs = []
    output = []

    for i in list(chunk(numeros, (len(numeros)//cpu_count() + 1))):
        clients.append(
            (
                client(lista=i),
                Array('Q', len(i))
            )
        )

    # start = default_timer()
    for item in clients:
        P = Process(target=item[0].parse_multiprocessing,
                    kwargs={'results': item[1]})
        jobs.append(P)
        P.start()

    for proc in jobs:
        proc.join()

    for item in clients:
        output.extend([i for i in item[1] if i > 0])
    output.sort(reverse=True)
    print(output[:222])
    # tmp.append(default_timer() - start)

    # print('%.5f ms' % (1000 * (sum(tmp) / 30.0)))
