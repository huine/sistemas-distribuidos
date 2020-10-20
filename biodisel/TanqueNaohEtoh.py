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
        #Cria thread para NaOh
        self.thread_naoh = Thread(
            target=self._add_naoh, daemon=True)
        #Cria thread para Etoh
        self.thread_etoh = Thread(
            target=self._add_etoh, daemon=True)

    def start(self):
        """Inicia atributos da classe"""
        self.insert_log('Iniciando tanque de NaOH/EtOH')
        self.running = True
        self.thread_naoh.start()
        self.thread_etoh.start()

    def stop(self):
        """Finaliza atributos da classe"""
        self.insert_log('Parando tanque de NaOH/EtOH')
        self.running = False

    def _add_naoh(self):
        """Adiciona 0.3litros de NaOh por seg"""
        while self.running:
            self.total_naoh += 0.3
            self.insert_log('Adicionado 0.3L de NaOH no tanque de NaOH/EtOH')
            sleep(0.1)

    def _add_etoh(self):
        """Adiciona 0.1litros de EtOh por seg"""
        while self.running:
            self.total_etoh += 0.1
            self.insert_log('Adicionado 0.1L de EtOH no tanque de NaOH/EtOH')
            sleep(0.1)

    def remover_naoh(self, qtd):
        """Remove qtd do total de NaOh"""
        self.total_naoh -= qtd
        self.insert_log('Removido %.3fL de NaOH no tanque de NaOH/EtOH' % qtd)

    def remover_etoh(self, qtd):
        """Remove qtd do total de EtOh"""
        self.total_etoh -= qtd
        self.insert_log('Removido %.3fL de EtOH no tanque de NaOH/EtOH' % qtd)

    def inserir_etoh(self, qtd):
        """Insere qtd em total EtOh"""
        self.total_etoh += qtd

    def insert_log(self, item):
        """."""
        req.post(
            url="http://localhost:9000/write",
            data={"texto": item}
        )
