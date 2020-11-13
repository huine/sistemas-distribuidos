import requests as req
from queue import Queue, Empty
from multiprocessing import cpu_count
from threading import Thread
from os import makedirs


class Worker(object):
    """Classe worker para realizar as requests."""

    def __init__(self, url, fila, name, q_thread):
        """Construtor do worker."""
        self.url = url
        self.q_thread = q_thread
        self.name = name
        self.file_name = 'output/%s.txt' % name
        self.running = False
        self.fila = fila
        self.retorno = []
        self.max = self.fila.qsize()
        self.ult_print = 0

    def diff(self):
        """."""
        if self.ult_print + (self.max * 0.02) <= len(self.retorno):
            self.ult_print = len(self.retorno)
        else:
            return

        print(
            'Worker %s -> Fila: %s\tProc: %s' % (self.name,
                                                 self.fila.qsize(),
                                                 len(self.retorno))
        )

    def start(self):
        """Inicia a execução do worker."""
        # Criar pasta para o output
        makedirs('output', exist_ok=True)

        print('Iniciando worker %s' % self.name)
        self.running = True

        threads = []
        print('Criando threads worker %s' % self.name)
        for i in range(self.q_thread):
            threads.append(Thread(target=self.request))

        print('Iniciando threads worker %s' % self.name)
        for i in threads:
            i.start()

        while self.fila.qsize() > 0:
            self.diff()
            pass

        self.running = False

        print('Encerrando threads worker %s' % self.name)
        for i in threads:
            i.join()

        print('Gerando output worker %s' % self.name)
        with open(self.file_name, 'w') as f:
            f.writelines(self.retorno)
            f.close()

    def request(self):
        """Funcao das threads de envio do worker."""
        while self.running:
            try:
                item = self.fila.get(timeout=0.5)
            except Empty:
                continue

            self.retorno.append(self.send(item=item))

    def send(self, item):
        """Envia uma request para a url com um item da fila."""
        return '%s - %s\n' % (item, req.post(
            url=self.url, data={'item': item}).text)


def make_worker(url, fila, name, q_thread=cpu_count()):
    """Cria uma instancia do worker."""
    return Worker(
        url=url, fila=fila,
        name=name, q_thread=q_thread
    )
