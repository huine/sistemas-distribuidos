import socket
from threading import *
import pickle
import simplejson as json


class ServerTCP(object):
    """Docstring for ServerTCP."""

    def __init__(self, host=socket.gethostname(), port=5000):
        self.host = host
        self.port = port
        self.run = False
        self.function = None
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as exp:
            print("Falha na criação do socket", exp)

        try:
            self.socket.bind((self.host, self.port))
        except socket.error as exp:
            print("Não foi possivel dar bind no host " +
                  "{host}:{port}".format(host=self.host, port=self.port),
                  exp)

    def start(self):
        """."""
        self.run = True
        self.socket.listen()
        while self.run:
            connection, remote = self.socket.accept()
            Thread(target=self.handle_connection, kwargs={'connection': connection}).start()

    def stop(self):
        """."""
        self.run = False

    def send(self, data, connection):
        """."""
        data = pickle.dumps(json.dumps(data))
        response = len(data).to_bytes(4096, 'big') + data
        connection.sendall(response)

    def receive(self, connection, size=4096):
        """."""
        length = int.from_bytes(connection.recv(4096), 'big')
        fragments = []
        count = 0
        while True:
            if count >= length:
                break
            chunk = connection.recv(size)
            fragments.append(chunk)
            count += len(chunk)
        return json.loads(pickle.loads(b''.join(fragments)))

    def handle_connection(self, connection):
        """."""
        request = self.receive(connection=connection)
        if self.function:
            response = self.function(request)
        else:
            response = 'ok'
        self.send(data=response, connection=connection)
        connection.close()


class ClientTCP(object):
    """."""

    def __init__(self, id):
        """."""
        self.id = id
        self.remote = None
        self.socket = None

    def connect(self, host=socket.gethostname(), port=5000):
        """."""
        self.remote = (host, port)
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as exp:
            print("Falha na criação do socket", exp)
        self.socket.connect(self.remote)

    def send(self, data):
        """."""
        data = pickle.dumps(json.dumps(data))
        request = len(data).to_bytes(4096, 'big') + data
        self.socket.sendall(request)

    def receive(self, size=4096):
        """."""
        # recebe o length
        length = int.from_bytes(self.socket.recv(4096), 'big')
        fragments = []
        count = 0
        while True:
            if count >= length:
                break
            chunk = self.socket.recv(size)
            fragments.append(chunk)
            count += len(chunk)
        self.socket.close()
        return json.loads(pickle.loads(b''.join(fragments)))