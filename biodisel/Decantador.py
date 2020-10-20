from flask import Flask, request
from threading import Thread
from queue import Queue, Empty
from time import sleep
import requests as req


class Decantador(object):
    """."""

    def __init__(self):
        """."""
        self.running = False
        self.glicerina = 0
        self.fila = Queue()
        self.thread_processar = Thread(
            target=self.processar, daemon=True)

    def start(self):
        """."""
        self.insert_log("Iniciando o decantador")
        self.running = True
        self.thread_processar.start()

    def stop(self):
        """."""
        self.insert_log("Parando o decantador")
        while self.fila.empty() is False:
            pass
        self.running = False

    def proc_reator(self, item):
        """."""
        if self.running:
            self.fila.put(item)
            self.insert_log("Decantador recebeu %sL" % item)
        return

    def processar(self):
        while self.running:
            try:
                to_proc = self.fila.get(timeout=1)
            except Empty:
                continue

            sleep((to_proc/3.0)*5.0)

            self.glicerina += to_proc*0.05
            self.insert_log(
                "Adicionado %sL de glicerina no tanque." % (to_proc*0.05))

            req.post(url="http://localhost:9002/add",
                     data={"qtd": to_proc*0.13})
            self.insert_log(
                "Enviado %sL de EtOH para o secador." % (to_proc*0.13))

            req.post(url="http://localhost:9004/add",
                     data={"qtd": to_proc*0.82})
            self.insert_log(
                "Enviado %sL de solução para lavagem." % (to_proc*0.82))

    def insert_log(self, item):
        """."""
        req.post(
            url="http://localhost:9000/write",
            data={"texto": item}
        )


decantador_app = Flask(__name__)
decantador = Decantador()


@decantador_app.route('/add', methods=['POST'])
def add():
    item = request.form.get('qtd', 0)
    if item:
        decantador.proc_reator(item=float(item))
    return ''
