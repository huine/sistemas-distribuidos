from flask import Flask, Response, request
from multiprocessing import Process, cpu_count
from copy import copy
import logging

log = logging.getLogger('werkzeug')
log.disabled = True


class EndpointAction(object):
    """Wrapper para tratar a request e responder o worker."""

    def __init__(self, action):
        """Construtor."""
        self.action = action

    def __call__(self, *args):
        """."""
        answer = self.action()
        self.response = Response(answer, status=200, headers={})
        return self.response


class FlaskAppWrapper(object):
    """Configuração do servidor e seus endpoints."""

    def __init__(self, name):
        """Construtor."""
        self.app = Flask(name)

    def run(self, conf={}):
        """Inicia o servidor Flask."""
        self.app.run(**conf)

    def add_all_endpoints(self):
        """Cria todos os endpoints do servidor."""
        self.add_endpoint(endpoint="/proc",
                          endpoint_name="/proc", handler=self.proc)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None,
                     methods=['POST']):
        """Adiciona um endpoint."""
        self.app.add_url_rule(
            endpoint, endpoint_name, EndpointAction(handler), methods=methods)

    @staticmethod
    def calcular_cpf(cpf):
        """Calcula os digitos de um cpf."""
        cpf = copy(cpf)
        r1 = range(10, 1, -1)
        r2 = range(11, 1, -1)

        v1 = 11 - (sum(item[0] * item[1] for item in zip(cpf, r1)) % 11)
        if v1 >= 10:
            v1 = 0

        cpf.append(v1)

        v2 = 11 - (sum(item[0] * item[1] for item in zip(cpf, r2)) % 11)
        if v2 >= 10:
            v2 = 0

        return '%s%s' % (v1, v2)

    @staticmethod
    def calcular_cnpj(cnpj):
        """Calcula os digitos de um cnpj."""
        cnpj = copy(cnpj)
        seq = [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5]

        v1 = 11 - (sum(item[0] * item[1] for item in zip(cnpj, seq)) % 11)
        if v1 >= 10:
            v1 = 0

        seq.append(6)
        cnpj.append(v1)

        v2 = 11 - (sum(item[0] * item[1] for item in zip(cnpj, seq)) % 11)
        if v2 >= 10:
            v2 = 0

        return '%s%s' % (v1, v2)

    def proc(self):
        """Função do endpoint que decide se é cnpj ou cpf."""
        item = [int(i) for i in request.form.get('item', '')]

        if len(item) == 9:
            _r = self.calcular_cpf(cpf=item)
        else:
            _r = self.calcular_cnpj(cnpj=item)

        return _r


def make_servers(num_server=cpu_count(), port_base=9000):
    """Cria instancias do servidor e executa em processos independentes."""
    # Define o range de portas
    portas = list(range(port_base, port_base + num_server))

    # Cria as instancias e inicia os processos
    servidores = []
    for porta in portas:
        server = FlaskAppWrapper('proc-%s' % porta)
        server.add_all_endpoints()
        p = Process(
            target=server.run,
            kwargs={
                'conf': {'host': '0.0.0.0',
                         'port': porta,
                         'threaded': False}
            },
        )
        p.start()
        servidores.append(p)

    # Retorna a lista de portas usadas e a lista de processos criados
    return {'portas': portas, 'servidores': servidores}


if __name__ == '__main__':
    serv = make_servers(4, 9000)
    print('portas: %s' % str(serv['portas']))
    while True:
        pass
