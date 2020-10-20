from random import uniform
from time import sleep
from threading import Thread
import requests as req

class TanqueOleo(object):
    """."""

    def __init__(self):
        """."""
        self.total = 0
        self.running = False
        self.thread_oleo = Thread(
            target=self._add_oleo, daemon=True)

    def start(self):
        """inicia os atributos da classe"""
        self.insert_log('Iniciando tanque de óleo')
        self.running = True
        self.thread_oleo.start()

    def stop(self):
        """Finaliza os atributos da classe"""
        self.insert_log('Parando tanque de óleo')
        self.running = False
        self.thread_oleo.join()

    def _add_oleo(self):
        """Adiciona entre 1 e 2 litros de oleo a cada 5s"""
        while self.running:
            add = round(uniform(1, 2), 3)
            self.total += add
            self.insert_log('Adicionado %.3fL de óleo no tanque de óleo.' % add)
            sleep(0.5)

    def remover(self, qtd):
        """Remove qtd do total de oleo"""
        self.total -= qtd
        self.insert_log('Removido %.3fL de óleo do tanque de óleo.' % qtd)

    def insert_log(self, item):
        """Envia o texto para o log"""
        req.post(
            url="http://localhost:9000/write",
            data={"texto": item}
        )
