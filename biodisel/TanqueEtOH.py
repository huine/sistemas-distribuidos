from flask import Flask, request, jsonify
from queue import Queue, Empty
from threading import Thread
from time import sleep
import requests as req


class TanqueEtOH(object):
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
        self.insert_log('Iniciando tanque de EtOH')
        self.running = True
        self.thread_secador.start()

    def stop(self):
        """."""
        self.insert_log('Parando tanque de EtOH')
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
                item = float(self.fila.get(timeout=1))
            except Empty:
                continue

            sleep(item * 0.3)
            _r = self.secador(item)
            self.total += _r
            self.insert_log(
                "Secador processou %.3fL de EtOH para o tanque" % _r)

    def enviar_etoh(self):
        """."""
        if self.total > 0:
            ret = jsonify(self.total)
            s = "Tanque de EtOH enviou %.3fL para o tanque de NaOH/EtOH"
            self.insert_log(s % self.total)
            self.total = 0
        else:
            ret = jsonify(0)

        return ret

tanque_etoh_app = Flask(__name__)
tanque = TanqueEtOH()


@tanque_etoh_app.route('/add', methods=['POST'])
def add():
    item = request.form.get('qtd', 0)
    if item:
        tanque.input_fila(item=item)
    return ''


@tanque_etoh_app.route('/etoh', methods=['POST'])
def get_etoh():
    return tanque.enviar_etoh()
