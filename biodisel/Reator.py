from TanqueOleo import TanqueOleo
from TanqueNaohEtoh import TanqueNaohEtoh
from network import ServerTCP, ClientUDP, ClientTCP
from threading import Thread
from time import sleep


class Reator(object):
    """."""

    def __init__(self):
        """."""
        self.server_tcp = ServerTCP(port=9002)
        self.client_udp = ClientUDP()
        self.client_tcp = ClientTCP()
        self.tanque_oleo = TanqueOleo()
        self.tanquenaohetoh = TanqueNaohEtoh()
        self.total_processado = 0
        self.running = False
        self.thread_servidor = Thread(
            target=self.start_servidor, name="Thread-servidor-reator",
            daemon=True)

        self.thread_processar = Thread(
            target=self.processar, name="Thread-processo-reator",
            daemon=True)

    def start_servidor(self):
        """."""
        self.server_tcp.start()

    def start(self):
        """."""
        self.insert_log('Iniciando Reator.')
        self.running = True
        self.tanque_oleo.start()
        self.tanquenaohetoh.start()
        self.thread_servidor.start()
        self.thread_processar.start()

    def stop(self):
        """."""
        self.insert_log('Parando Reator.')
        self.running = False
        self.tanque_oleo.stop()
        self.tanquenaohetoh.stop()
        self.server_tcp.stop()
        self.thread_servidor.join()
        self.thread_processar.join()

    def processar(self):
        """."""
        while self.running:
            total = self.tanquenaohetoh.total_naoh +\
                self.tanquenaohetoh.total_etoh +\
                self.tanque_oleo.total

            if total < 5:
                continue
            else:
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

                sleep(1)

    def insert_log(self, item):
        """."""
        self.client_udp.send(item, port=9000)
