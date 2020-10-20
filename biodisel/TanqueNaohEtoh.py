from threading import Thread
from time import sleep
import requests as req


class TanqueNaohEtoh(object):
    """."""

    def __init__(self):
        """."""
        self.total_naoh = 0
        self.total_etoh = 0
        self.running = False
        self.thread_naoh = Thread(
            target=self._add_naoh, daemon=True)
        self.thread_etoh = Thread(
            target=self._add_etoh, daemon=True)

    def start(self):
        """."""
        self.insert_log('Iniciando tanque de NaOH/EtOH')
        self.running = True
        self.thread_naoh.start()
        self.thread_etoh.start()

    def stop(self):
        """."""
        self.insert_log('Parando tanque de NaOH/EtOH')
        self.running = False

    def _add_naoh(self):
        """."""
        while self.running:
            self.total_naoh += 0.3
            self.insert_log('Adicionado 0.3L de NaOH no tanque de NaOH/EtOH')
            sleep(1)

    def _add_etoh(self):
        """."""
        while self.running:
            self.total_etoh += 0.1
            self.insert_log('Adicionado 0.1L de EtOH no tanque de NaOH/EtOH')
            sleep(1)

    def remover_naoh(self, qtd):
        """."""
        self.total_naoh -= qtd
        self.insert_log('Removido %sL de NaOH no tanque de NaOH/EtOH' % qtd)

    def remover_etoh(self, qtd):
        """."""
        self.total_etoh -= qtd
        self.insert_log('Removido %sL de EtOH no tanque de NaOH/EtOH' % qtd)

    def inserir_etoh(self, qtd):
        """."""
        self.total_etoh += qtd

    def insert_log(self, item):
        """."""
        req.post(
            url="http://localhost:9000/write",
            data={"texto": item}
        )
