from flask import Flask, request
from queue import Queue, Empty
from datetime import datetime
from threading import Thread


class Logger(object):
    """."""

    def __init__(self):
        self.log_file = 'log.txt'
        self.timestamp = lambda: str(datetime.now())
        self.fila = Queue()
        self.running = False
        self.thread_writer = Thread(
            target=self.write_log, daemon=True)

    def start(self):
        """."""
        self.running = True
        self.trunk_logger()
        self.thread_writer.start()

    def stop(self):
        """."""
        self.fila_input('Logger ended')
        while not self.fila.empty():
            pass
        self.running = False

    def trunk_logger(self):
        """."""
        with open(self.log_file, 'w') as file:
            file.write('%s - %s\n' % (self.timestamp(), 'Logger started.'))
            file.close()

    def fila_input(self, item):
        """."""
        self.fila.put(item=item)

    def write_log(self):
        """."""
        while self.running:
            try:
                item = self.fila.get(timeout=1)
            except Empty:
                continue

            with open(self.log_file, 'a') as file:
                file.write('%s - %s\n' % (self.timestamp(), item))
                file.close()


print(__name__)
logger_app = Flask(__name__)
logger = Logger()


@logger_app.route('/write', methods=['POST'])
def write():
    """."""
    item = request.form.get('texto', '')
    if item:
        logger.fila_input(item=item)
    return ''
