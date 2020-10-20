from TanqueOleo import TanqueOleo
from TanqueNaohEtoh import TanqueNaohEtoh
from threading import Thread
from time import sleep
import requests as req


class Reator(object):
    """."""

    def __init__(self):
        """."""
        self.tanque_oleo = TanqueOleo()
        self.tanquenaohetoh = TanqueNaohEtoh()
        self.total_processado = 0
        self.running = False
        self.thread_processar = Thread(
            target=self.processar, daemon=True)
        self.thread_tanque = Thread(
            target=self.buscar_tanque, daemon=True)

    def start(self):
        """."""
        self.insert_log('Iniciando Reator.')
        self.running = True
        self.tanque_oleo.start()
        self.tanquenaohetoh.start()
        self.thread_processar.start()
        self.thread_tanque.start()

    def stop(self):
        """."""
        self.insert_log('Parando Reator.')
        self.running = False
        self.tanque_oleo.stop()
        self.tanquenaohetoh.stop()

    def processar(self):
        """."""
        while self.running:
            total = self.tanquenaohetoh.total_naoh +\
                self.tanquenaohetoh.total_etoh +\
                self.tanque_oleo.total

            if total > 5:
                total = 5

            if self.tanquenaohetoh.total_naoh >= total/4.0 and\
                    self.tanquenaohetoh.total_etoh >= total/2.0 and\
                    self.tanque_oleo.total >= total/4.0:
                self.tanquenaohetoh.remover_naoh(total/4.0)
                self.tanquenaohetoh.remover_etoh(total/2.0)
                self.tanque_oleo.remover(total/4.0)
                string = 'Reator processou {0}L de óleo, {1}L de EtOH, ' +\
                    '{2}L de NaOH.'
                self.insert_log(
                    string.format(total/4.0, total/2.0, total/4.0))

                sleep(total * (1.0/5.0))

                req.post(url="http://localhost:9003/add", data={"qtd": total})
                self.insert_log("Enviado %sL para o decantador" % total)

    def insert_log(self, item):
        """."""
        req.post(
            url="http://localhost:9000/write",
            data={"texto": item}
        )

    def buscar_tanque(self):
        """."""
        while self.running:
            r = req.post(url="http://localhost:9002/etoh").json()
            if not r:
                sleep(3)
            else:
                self.tanquenaohetoh.inserir_etoh(r)
