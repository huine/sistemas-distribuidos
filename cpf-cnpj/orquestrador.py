from queue import Queue, Empty
from multiprocessing import cpu_count, Value
from threading import Thread
from timeit import default_timer
import funcoes


def open_file(num_linhas=0):
    """
    Abre o arquivo e particiona.

    Abre o arquivo de base e particiona ele em N pedaços.
    A quantidade de pedaçoes é definida no paremetro num_chunks.
    Se o parametro não for informado, é tratado como o número de threads
    da cpu.
    """
    print('Carregando o arquivo')
    with open('BASE.txt', 'r') as f:
        file = [i.replace(' ', '').replace('\n', '')
                for i in f.readlines()]
        f.close()

    if num_linhas:
        file = file[:num_linhas]

    print("Total de entradas: %s" % len(file))

    return file


class Worker(object):
    """Docstring for Worker."""

    def __init__(self, fila, total, num_threads=cpu_count()):
        """."""
        self.fila = fila
        self.total = total
        self.num_threads = num_threads
        self.ult_print = Value('i', 0)
        self.threads = []
        self.output = []
        self.running = False

    def diff(self):
        """."""
        offset = (self.total * 0.01)
        # offset = 100
        if self.ult_print.value + offset <= len(self.output):
            with self.ult_print.get_lock():
                self.ult_print.value = len(self.output)

            print('Faltam:\t%s' % (self.total - len(self.output)))

    def start(self):
        """."""
        self.running = True

        print('Criando as threads do worker')
        for i in range(self.num_threads):
            self.threads.append(Thread(target=self.processar))

        print('Iniciando as threads do worker')
        for t in self.threads:
            t.start()

        while self.fila.empty() is False:
            # self.diff()
            pass

        self.running = False

        print('Encerrando as threads do worker')
        for t in self.threads:
            t.join()

    def processar(self):
        """."""
        while self.running:
            try:
                item = self.fila.get(timeout=0.5)
            except Empty:
                continue

            item = [int(i) for i in item]

            if len(item) == 9:
                resp = funcoes.calcular_cpf(item)
            else:
                resp = funcoes.calcular_cnpj(item)

            self.output.append(resp)


def iniciar(num_threads, file):
    """."""
    fila = Queue()
    print('Gerando fila')
    for item in file:
        fila.put(item)

    worker = Worker(
        fila=fila, total=fila.qsize(),
        num_threads=num_threads)

    start = default_timer()
    worker.start()
    execucao = default_timer() - start

    print('Tempo de execução: %.5f s' % execucao)
    with open('output.txt', 'w') as f:
        f.writelines(worker.output)
        f.close()

    print('Terminou')

    return execucao


def trunk_media():
    with open('media.txt', 'w') as f:
        f.write('')
        f.close()


if __name__ == '__main__':
    file = open_file()
    times = []
    for i in range(100):
        tmp = iniciar(num_threads=8, file=file)
        times.append(tmp)

    media = sum(times)/len(times)
    print("Tempo Médio: %.10f ms\n" % (media*1000))
    # trunk_media()
    # file = open_file(num_linhas=50000)
    # for num in [2**i for i in range(1,7)]:
    #     times = []
    #     for i in range(100):
    #         tmp = iniciar(num_threads=num, file=file)
    #         times.append(tmp)

    #     media = sum(times)/len(times)
    #     s = "Threads: %s\tTempo: %.5f\n" % (num, media)
    #     with open('media.txt', 'a') as m:
    #         m.write(s)

    # print('Fim')
