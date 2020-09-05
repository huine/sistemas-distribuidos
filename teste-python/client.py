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

    def __init__(self, lista, id):
        """."""
        self.lista = lista
        super().__init__(id)

    def inicia(self, results):
        """."""
        super().connect()
        super().send(self.lista)
        response = super().receive()
        for i in range(len(response)):
            results[i] = response[i]


if __name__ == "__main__":
    tmp = []
    for j in range(30):
        numeros = list(range(1, (140 * 71) + 1))
        shuffle(numeros)
        clients = []
        jobs = []
        output = []

        for i in list(chunk(numeros, (len(numeros)//cpu_count() + 1))):
            with open('/dev/random', 'rb') as f:
                id_client = f.read(10).hex()
            clients.append(
                (
                    client(lista=i, id=id_client),
                    Array('Q', len(i))
                )
            )

        start = default_timer()
        for item in clients:
            P = Process(target=item[0].inicia, kwargs={'results': item[1]})
            jobs.append(P)
            P.start()

        for proc in jobs:
            proc.join()

        for item in clients:
            output.extend([i for i in item[1] if i > 0])
        output.sort(reverse=True)
        tmp.append(default_timer() - start)

    print('%.5f ms' % (1000 * (sum(tmp) / 30.0)))
