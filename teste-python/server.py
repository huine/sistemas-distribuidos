from network import ServerTCP
from functions import function as f


if __name__ == "__main__":
    server = ServerTCP(timeout=15)
    server.set_function((f.buscaPrimos,))
    server.start()
