from threading import Lock, Thread
from time import sleep
from queue import Queue, Empty, Full
import random
from timeit import default_timer
from os import getpid
from psutil import Process


class Barbeiro(Thread):

    def __init__(self, nome, cadeiras):
        """."""
        super().__init__()
        self.nome = nome
        self.running = False
        self.tempo_dormindo = 0
        self.fila = Queue(cadeiras)

    def run(self):
        """."""
        while(self.running):
            # Pega um cliente na fila ou
            # dorme ate um cliente chegar
            start = default_timer()
            cliente = self.fila.get()
            self.tempo_dormindo += default_timer() - start
            print('Atendendo o cliente: %s' % cliente.nome)
            # Trabalha entre 2 e 3 segundos (stand in para 20~30 minutos)
            sleep(random.uniform(2, 3))
            # Encerra a thread do cliente que foi atendido
            cliente.join()
            global clientes_atendidos
            clientes_atendidos += 1


class Cliente(Thread):

    def __init__(self, nome, barbeiro):
        """."""
        super().__init__()
        self.nome = nome
        self.barbeiro = barbeiro

    def run(self):
        """."""
        print("%s indo ao barbeiro" % self.nome)
        try:
            self.barbeiro.fila.put(self, timeout=2.5)
        except Full:
            global clientes_recusados
            clientes_recusados += 1


if __name__ == "__main__":
    clientes_atendidos = 0
    clientes_recusados = 0
    barbeiro = Barbeiro(nome="Barbeiro", cadeiras=5)
    barbeiro.running = True
    barbeiro.start()
    for i in range(10):
        cliente = Cliente(nome=str(i), barbeiro=barbeiro)
        cliente.start()
        # Gera um cliente a cada 3 segundo(Stand in para 30 minutos)
        # [2 clientes por hora]
        sleep(3)

    while not barbeiro.fila.empty():
        # Espera a fila de clientes esvaziar antes de encerrar o programa
        pass

    barbeiro.running = False

    print('clientes_atendidos: %s' % clientes_atendidos)
    print('clientes_recusados: %s' % clientes_recusados)
    print('barbeiro dormindo: %.5f s' % barbeiro.tempo_dormindo)

    pid = getpid()
    proc = Process(pid)
    proc.terminate()