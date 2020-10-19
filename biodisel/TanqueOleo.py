from random import uniform
from time import sleep
from threading import Thread
from network import ClientUDP


class TanqueOleo(object):
    """."""

    def __init__(self):
        """."""
        self.total = 0
        self.running = False
        self.client_udp = ClientUDP()
        self.thread_oleo = Thread(
            target=self._add_oleo, name="Tanque-Oleo-Adder")

    def start(self):
        """."""
        self.insert_log('Iniciando tanque de óleo')
        self.running = True
        self.thread_oleo.start()

    def stop(self):
        """."""
        self.insert_log('Parando tanque de óleo')
        self.running = False
        self.thread_oleo.join()

    def _add_oleo(self):
        """."""
        while self.running:
            add = uniform(1, 2)
            self.total += add
            self.insert_log('Adicionado %sL de óleo no tanque de óleo.' % add)
            sleep(5)

    def remover(self, qtd):
        """."""
        self.total -= qtd
        self.insert_log('Removido %sL de óleo do tanque de óleo.' % qtd)

    def insert_log(self, item):
        """."""
        self.client_udp.send(item, port=9000)
