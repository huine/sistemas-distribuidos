import socket
import threading
import pickle
import simplejson as json
from collections.abc import Iterable
from copy import deepcopy
from queue import Queue
from os import getpid
from psutil import Process
from datetime import datetime


def _make_id():
    """."""
    with open('/dev/random', 'rb') as f:
        return f.read(10).hex()


class ServerTCP(object):
    """ServerTCP object."""

    def __init__(self, host=socket.gethostname(), port=5000, timeout=0,
                 backlog=50):
        """."""
        self.host = host
        self.port = port
        self.run = False
        self.id = _make_id()
        self.timeout = timeout
        self.backlog = backlog
        self._list_connection = Queue()
        self._num_connections = 0
        self._last_connection = None
        self._server_startup = None
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as exp:
            print("Socket creation failed.", str(exp))

        try:
            self.socket.bind((self.host, self.port))
        except socket.error as exp:
            print("Connection to {host}:{port} failed".format(
                host=self.host, port=self.port), str(exp))

    def start(self):
        """Make the server start listening."""
        self.run = True
        self._server_startup = datetime.now()
        threading.Thread(target=self._terminate_threads,
                         daemon=True,
                         name='Clean-Connections-Thread').start()
        if self.timeout:
            threading.Thread(target=self._timeout_server,
                             daemon=True,
                             name='Timeout-Server-Thread').start()

        self.socket.listen(self.backlog)
        while self.run:
            connection, remote = self.socket.accept()
            _t = threading.Thread(
                target=self._handle_connection,
                kwargs={'connection': connection})
            _t.start()
            self._list_connection.put(_t)

    def stop(self):
        """Stop server."""
        self.run = False
        threading.Thread(target=self._terminate_server,
                         daemon=True,
                         name='Terminate-Server-Thread').start()

    def _terminate_server(self):
        """."""
        last_print = None
        while True:
            if self._num_connections > 0 and\
                    (last_print is None or
                     last_print != self._num_connections):
                last_print = self._num_connections
                print('Waiting to close {0} pending connections.'.format(
                    self._num_connections))

            if self._num_connections == 0 and\
                    self._list_connection.empty():
                print('Terminating server.')
                pid = getpid()
                proc = Process(pid)
                proc.terminate()
                break

    def _timeout_server(self):
        """."""
        while True:
            if self._last_connection is None:
                diff_time = (datetime.now() -
                             self._server_startup).total_seconds()
            else:
                diff_time = (datetime.now() -
                             self._last_connection).total_seconds()

            if diff_time > self.timeout:
                print('Server wait time timed out.')
                self.stop()
                break

    def _terminate_threads(self):
        """Finish rogue threads."""
        while True:
            _t = self._list_connection.get()
            _t.join()
            self._list_connection.task_done()

    def send(self, data, connection):
        """Send data to the connected client."""
        data = pickle.dumps(json.dumps(data))
        response = len(data).to_bytes(4096, 'big') + data
        connection.sendall(response)

    def receive(self, connection, size=4096):
        """Receive data from the client."""
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

    def set_function(self, functions):
        """
        Set the _functions attribute.

        Accepts a list, tuple or iterable object with functions as it's itens.
        """
        if not isinstance(functions, Iterable):
            raise TypeError('Function is not iterable according ' +
                            'to collections.abc.Iterable')

        for f in functions:
            if not callable(f):
                raise TypeError('Itens should be callable')

        self._functions = functions

    def _handle_connection(self, connection):
        """Handle the connection with the client."""
        self._num_connections += 1
        try:
            request = self.receive(connection=connection)

            if getattr(self, '_functions', None):
                response = []
                for function in self._functions:
                    try:
                        _req = deepcopy(request)
                        response.append(function(_req))
                    except Exception as err:
                        response.append(str(err))
            else:
                response = 'ok'
            self.send(data=response, connection=connection)
        finally:
            connection.close()
            self._last_connection = datetime.now()
            self._num_connections -= 1


class ClientTCP(object):
    """ClientTCP object."""

    def __init__(self):
        """."""
        self.id = _make_id()
        self.remote = None
        self.socket = None

    def connect(self, host=socket.gethostname(), port=5000):
        """Connect to the server."""
        self.remote = (host, port)
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as exp:
            print("Socket creation failed.", str(exp))
        self.socket.connect(self.remote)

    def send(self, data):
        """Send data to the connected server."""
        data = pickle.dumps(json.dumps(data))
        request = len(data).to_bytes(4096, 'big') + data
        self.socket.sendall(request)

    def receive(self, size=4096):
        """Receive data from server and close the connection."""
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


class ServerUDP(object):
    """ServerUDP object."""

    def __init__(self, host=socket.gethostname(), port=5000, timeout=0,
                 size=4096):
        """."""
        self.host = host
        self.port = port
        self.run = False
        self.id = _make_id()
        self.timeout = timeout
        self.size = size
        self._list_connection = Queue()
        self._num_connections = 0
        self._last_connection = None
        self._server_startup = None
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as exp:
            print("Socket creation failed.", str(exp))

        try:
            self.socket.bind((self.host, self.port))
        except socket.error as exp:
            print("Connection to {host}:{port} failed".format(
                host=self.host, port=self.port), str(exp))

    def start(self):
        """Make the server start listening."""
        self.run = True
        self._server_startup = datetime.now()
        threading.Thread(target=self._terminate_threads,
                         daemon=True,
                         name='Clean-Connections-Thread').start()
        if self.timeout:
            threading.Thread(target=self._timeout_server,
                             daemon=True,
                             name='Timeout-Server-Thread').start()

        while self.run:
            data, remote = self.receive()
            _t = threading.Thread(target=self._handle_connection,
                                  kwargs={'remote': remote, 'data': data})
            _t.start()
            self._list_connection.put(_t)

    def stop(self):
        """Stop server."""
        self.run = False
        threading.Thread(target=self._terminate_server,
                         daemon=True,
                         name='Terminate-Server-Thread').start()

    def _terminate_server(self):
        """."""
        last_print = None
        while True:
            if self._num_connections > 0 and\
                    (last_print is None or
                     last_print != self._num_connections):
                last_print = self._num_connections
                print('Waiting to close {0} pending connections.'.format(
                    self._num_connections))

            if self._num_connections == 0 and\
                    self._list_connection.empty():
                print('Terminating server.')
                pid = getpid()
                proc = Process(pid)
                proc.terminate()
                break

    def _timeout_server(self):
        """."""
        while True:
            if self._last_connection is None:
                diff_time = (datetime.now() -
                             self._server_startup).total_seconds()
            else:
                diff_time = (datetime.now() -
                             self._last_connection).total_seconds()

            if diff_time > self.timeout:
                print('Server wait time timed out.')
                self.stop()
                break

    def _terminate_threads(self):
        """Finish rogue threads."""
        while True:
            _t = self._list_connection.get()
            _t.join()
            self._list_connection.task_done()

    def send(self, data, remote):
        """Send data to the connected client."""
        self.socket.sendto(pickle.dumps(json.dumps(data)), remote)

    def receive(self):
        """Receive data from the client."""
        request, remote = self.socket.recvfrom(self.size)
        return (json.loads(pickle.loads(request)), remote)

    def set_function(self, functions):
        """
        Set the _functions attribute.

        Accepts a list, tuple or iterable object with functions as it's itens.
        """
        if not isinstance(functions, Iterable):
            raise TypeError('Function is not iterable according ' +
                            'to collections.abc.Iterable')

        for f in functions:
            if not callable(f):
                raise TypeError('Itens should be callable')

        self._functions = functions

    def _handle_connection(self, remote, data):
        """Handle the connection with the client."""
        self._num_connections += 1
        try:
            if getattr(self, '_functions', None):
                response = []
                for function in self._functions:
                    try:
                        _req = deepcopy(data)
                        response.append(function(_req))
                    except Exception as err:
                        response.append(str(err))
            else:
                response = 'ok'
            self.send(data=response, remote=remote)
        finally:
            self._last_connection = datetime.now()
            self._num_connections -= 1


class ClientUDP(object):
    """ClientUDP object."""

    def __init__(self):
        """."""
        self.id = _make_id()
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as exp:
            print("Socket creation failed.", str(exp))

    def send(self, data, host=socket.gethostname(), port=5000):
        """Send data to the connected server."""
        remote = (host, port)
        self.socket.sendto(pickle.dumps(json.dumps(data)), remote)

    def receive(self, size=4096):
        """Receive data from server and close the connection."""
        # recebe o length
        response, remote = self.socket.recvfrom(size)
        self.socket.close()
        return json.loads(pickle.loads(response))
