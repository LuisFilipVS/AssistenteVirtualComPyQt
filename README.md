# Assistente Virtual com PyQt5

Este é um projeto de assistente virtual com interface Gráfica com Python
A princípio começou com avaliação de uma disciplina da faculdade e eu decidi dar seguimento ao projeto
E claro, todo(a) assistente precisa de um nome, então escolhi, de forma peculiar, dar o nome de ***Dinorá***

## Funcionamento

* O programa inicializa com uma interface gráfica e aguarda solicitações.
* As solicitações são realizadas por meio de reconhecimento de voz e precisam sempre ao inicio, chamarp pelo nome da assistente
* As solicitações reconhecidas(A principio) são devolvidas na interface
  por meio de texto simulando um chat.
* A assistente reconhece comandos de:
    1. Ligar e desligar ar-condicionado
    2. Ligar e desligar GPS
    3. Ajustar temperatura para determinada quantidade de graus
    Ex. "Dinorah, ligar o gps"

## Inicialização

* Primeiramente, instale as dependências necessárias contidos no arquivo requirements

~~~bash
pip install -r requirements.txt
~~~

* Caso você esteja usando sistema operacional Linux, poderá ocorrer alguns erros na instalação
  da dependência pyaudio, logo, poderá ser corrigido com os comandos abaixo:

~~~bash
sudo apt-get install python3-pyaudio
sudo apt-get install portaudio19-dev python-all-dev python3-all-dev
~~~

* Inicialize o programa por meio do arquivo app.py, contido na raiz

~~~bash
python app.py
~~~

* Ao iniciar a interface gráfica, aperte o botão "Iniciar" e aguarde o sinal para realizar uma solicitação
