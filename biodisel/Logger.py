from network import ServerUDP
import datetime
from queue import Queue, Empty
import threading


class Logger(ServerUDP):
    """."""

    def __init__(self, log_file='log.txt'):
        """."""
        self.log_file = log_file
        self.timestamp = lambda: str(datetime.datetime.now())
        self.fila = Queue()
        self.running_logger = False
        super().__init__(port=9000)
        self.thread_writer = threading.Thread(
            target=self._write_log, name="Logger-Writer")

    def start_logger(self):
        """."""
        self._trunk_logger()
        self.running_logger = True
        self.thread_writer.start()
        super().set_function((self._input_fila,))
        super().start()

    def stop_logger(self):
        """."""
        self._input_fila('Logger ended')
        while self.fila.empty() is False:
            pass
        self.running_logger = False
        self.thread_writer.join()
        super().stop()

    def _trunk_logger(self):
        """."""
        with open(self.log_file, 'w') as file:
            file.write('%s - %s\n' % (self.timestamp(), 'Logger started.'))
            file.close()

    def _input_fila(self, item):
        """."""
        self.fila.put(item)
        return 'ok'

    def _write_log(self):
        """."""
        while self.running_logger is True:
            try:
                item = self.fila.get(timeout=1)
            except Empty:
                continue

            with open(self.log_file, 'a') as file:
                file.write('%s - %s\n' % (self.timestamp(), item))
                file.close()
