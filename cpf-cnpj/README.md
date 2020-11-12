# Instalar e executar
Para instalar, basta entrar na pasta `sistemas-distribuidos/cpf-cnpj/` e executar o código abaixo:
```
pip install -r requirements.txt
```
Assim que terminar de instalar, basta executar o `orquestrador.py`
```
python orquestrador.py
```
Isso vai iniciar todos os servidores e workers.
Todo o output da aplicação é gravado no arquivo `log.txt`.
Esse arquivo é truncado sempre que a aplicação é executada.

# BASE.txt
Como o arquivo BASE.txt é grande demais para subir no repositório, é necessário fazer o download dele de forma separada.
Depois de conseguir o arquivo, basta copia-lo para a pasta `sistemas-distribuidos/cpf-cnpj/`