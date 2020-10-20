# Instalar e executar
Para instalar, basta entrar na pasta `sistemas-distribuidos/biodisel/` e executar o código abaixo:
```
pip install -r requirements.txt
```
Assim que terminar de instalar, basta executar o `Orquestrador.py`
```
python Orquestrador.py
```
Isso vai iniciar todos os servidores e todas as threads de execução.
Todo o output da simulação é gravado no arquivo `log.txt`.
Esse arquivo é truncado sempre que uma nova simulação é executada.

Por enquanto, a simulção está rodando apenas por 90 segundos, mas esse tempo de execução pode ser alterado mudando esse trecho de código:
```Python
 while (datetime.now() - start).total_seconds() < 90:
 ```

