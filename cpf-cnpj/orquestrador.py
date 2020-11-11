from multiprocessing import Process, cpu_count
from queue import Queue
from itertools import islice
from timeit import default_timer
from time import sleep
from Requester import make_worker
from Server import make_servers
from os import remove, listdir


def chunk(it, size):
    """Particiona uma lista em pedaços do mesmo tamanho."""
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


def open_file(num_chunks=cpu_count()):
    """
    Abre o arquivo e particiona.

    Abre o arquivo de base e particiona ele em N pedaços.
    A quantidade de pedaçoes é definida no paremetro num_chunks.
    Se o parametro não for informado, é tratado como o número de threads
    da cpu.
    """
    with open('BASE.txt', 'r') as f:
        file = [i.replace(' ', '').replace('\n', '')
                for i in f.readlines()]
        f.close()

    return chunk(file, (len(file)//num_chunks + 1))


def unify_output():
    """Unifica todos os arquivos da pastas output."""
    try:
        # Remove o arquivo log.txt caso já exista.
        remove('final.txt')
    except:
        pass

    # Itera sobre os arquivos da pasta output
    for file in listdir('output'):
        # Abre o arquivo de output final
        with open('final.txt', 'a') as final:
            # Abre um arquivo de output do worker e le todas as linhas
            with open('output/' + file, 'r') as tmp:
                lines = tmp.readlines()
                tmp.close()
            # Escreve o conteudo lido no arquivo final
            final.writelines(lines)
            final.close()
        try:
            # remove arquivo que já foi lido.
            remove('output/' + file)
        except:
            pass


if __name__ == '__main__':
    # Número de processos de servidor e de workers
    num_serv_work = 8
    # Número de threads para cada worker
    num_work_thread = 1

    # Pega os dados do arquivo
    print('Carregando o arquivo')
    dados = open_file(num_chunks=num_serv_work)

    # Processos dos servidores de calculos
    print('Iniciando os servidores')
    serv = make_servers(num_server=num_serv_work)

    # Cria os workers para enviar os itens do arquivo para os servidores.
    # Um worker para cada servidor.
    print('Iniciando os workers')
    workers = []
    for index, item in enumerate(dados):
        q = Queue()
        # Move os itens da lista para uma fila
        for j in item:
            q.put_nowait(j)

        workers.append(
            make_worker(
                url='http://localhost:%s/proc' % serv['portas'][index],
                fila=q, name=index, q_thread=num_work_thread)
        )

    # Coloca cada worker em um processo independente
    workers_proc = []
    print('Criando os processos dos workers')
    for r in workers:
        workers_proc.append(Process(target=r.start))

    # Inicia todos os processos dos workers
    print('Iniciando todos os workers')
    for proc in workers_proc:
        proc.start()

    # Aguarda os processos dos workers terminarem
    print('Esperando os processos dos workers')
    for proc in workers_proc:
        proc.join()

    # Encerra todas os processos dos servidores
    print('Finalizando servidores')
    for proc in serv['servidores']:
        proc.terminate()

    # Gerar arquivo único com o output
    print("Unificando o output.")
    unify_output()

    print('Encerrado')
