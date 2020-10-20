import Logger
import TanqueEtOH
import Decantador
import TanqueBiodisel
from Reator import Reator
from datetime import datetime
from threading import Thread
from time import sleep
import requests as req

def insert_log(item):
    """."""
    req.post(
        url="http://localhost:9000/write",
        data={"texto": item}
    )

if __name__ == "__main__":
    thread_logger = Thread(
        target=Logger.logger_app.run,
        kwargs={'host': '0.0.0.0', 'port': 9000, 'threaded': True},
        daemon=True)

    thread_tanque_etoh = Thread(
        target=TanqueEtOH.tanque_etoh_app.run,
        kwargs={'host': '0.0.0.0', 'port': 9002, 'threaded': True},
        daemon=True)

    thread_decantador = Thread(
        target=Decantador.decantador_app.run,
        kwargs={'host': '0.0.0.0', 'port': 9003, 'threaded': True},
        daemon=True)

    thread_biodisel = Thread(
        target=TanqueBiodisel.tanque_biodisel_app.run,
        kwargs={'host': '0.0.0.0', 'port': 9004, 'threaded': True},
        daemon=True)

    thread_logger.start()
    thread_tanque_etoh.start()
    thread_decantador.start()
    thread_biodisel.start()
    sleep(1)

    reator = Reator()

    Logger.logger.start()
    TanqueEtOH.tanque.start()
    reator.start()
    Decantador.decantador.start()
    TanqueBiodisel.tanque.start()
    
    # 360s(6 minutos) = 3600s(1 hora)
    start = datetime.now()
    while (datetime.now() - start).total_seconds() < 360:
        pass

    reator.stop()
    TanqueEtOH.tanque.stop()
    Decantador.decantador.stop()
    TanqueBiodisel.tanque.stop()

    insert_log('Total Biodisel: %.3fL' % TanqueBiodisel.tanque.total)
    insert_log('Total Glicerina: %.3fL' % Decantador.decantador.glicerina)
    etoh = TanqueEtOH.tanque.total + reator.tanquenaohetoh.total_etoh
    insert_log('Total EtOH restante: %.3fL' % etoh)
    insert_log('Total NaOH restante: %.3fL' % reator.tanquenaohetoh.total_naoh)
    insert_log('Total Óleo restante: %.3fL' % reator.tanque_oleo.total)

    Logger.logger.stop()
    while Logger.logger.fila.empty() is False:
        pass
