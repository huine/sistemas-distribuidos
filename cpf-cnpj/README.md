# Instalar e executar
Para instalar, basta entrar na pasta `sistemas-distribuidos/cpf-cnpj/` e executar o código abaixo:
```Shell
pip install -r requirements.txt
```
Assim que a instalação da dependencias terminar, é necessário compilar o arquivo `funcoes.pyx` usando o `Cython`.
Para realizar essa operação execute essa linha
```Shell
python setup.py build_ext --inplace
```
Assim que a compilação for encerrada, basta executar o arquivo `orquestrador.py` para rodar a solução.
```Shell
python orquestrador.py
```
Isso vai iniciar o processo de validação dos dados inseridos na base de dados.
Ao final, será exebido o tempo de execução em segundos e o arquivo `output.txt` com os números processados estará disponível na mesma pasta.

# BASE.txt
Como o arquivo BASE.txt é grande demais para subir no repositório, é necessário fazer o download dele de forma separada.
Depois de conseguir o arquivo, basta copia-lo para a pasta `sistemas-distribuidos/cpf-cnpj/`.
É importante que isso seja feito antes de excutar a solução.