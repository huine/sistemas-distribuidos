from flask import Flask, request
from queue import Queue, Empty
from threading import Thread
from time import sleep
import requests as req


class TanqueBiodisel(object):
    """."""

    def __init__(self):
        """."""
        self.total = 0
        self.secador = lambda qtd: qtd - (qtd*0.015)
        self.fila = Queue()
        self.running = False
        self.thread_secador = Thread(target=self.proc_secador,
                                     daemon=True)

    def start(self):
        """."""
        self.insert_log('Iniciando tanque de BioDisel')
        self.running = True
        self.thread_secador.start()

    def stop(self):
        """."""
        self.insert_log('Parando tanque de BioDisel')
        while self.fila.empty() is False:
            pass
        self.running_tanque = False

    def input_fila(self, item):
        """."""
        self.fila.put(item=item)

    def insert_log(self, item):
        """."""
        req.post(
            url="http://localhost:9000/write",
            data={"texto": item}
        )

    def proc_secador(self):
        """."""
        while self.running:
            try:
                item = self.fila.get(timeout=1)
            except Empty:
                continue

            # 3 lavagens, perdendo 5% a cada lavagem
            # eh equivalente a perder 14,2625%
            item = item - (item*0.142625)

            sleep(item * 3)
            _r = self.secador(item)
            self.total += _r
            self.insert_log(
                "Secador processou %sL de BioDisel para o tanque" % _r)


tanque_biodisel_app = Flask(__name__)
tanque = TanqueBiodisel()


@tanque_biodisel_app.route('/add', methods=['POST'])
def add():
    item = request.form.get('qtd', 0)
    if item:
        tanque.input_fila(item=float(item))
    return ''
