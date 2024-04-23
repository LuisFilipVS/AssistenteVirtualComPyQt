try:
    from capturaAudio import capturaAudio
    from linguagemNatural import linguagemNatural
    from atuar_sobre_ar_condicionado import *
    from atuar_sobre_gps import *
except:
    from assistente.capturaAudio import capturaAudio
    from assistente.linguagemNatural import linguagemNatural
    from assistente.atuar_sobre_ar_condicionado import *
    from assistente.atuar_sobre_gps import *

import json
import time


'''
Proposta:
    Ligar GPS
    Desligar GPS
    Ligar Ar-Condicionado
    Desligar Ar-Condicionado
    Ajustar temperatura para x graus
'''

#Definição da classe assistente
class assistente():
    def __init__(self, caminho_dataBase="assistente/dados.json", interface=None,iniciar_fala=None, retorno=None):
        self.iniciar_fala = iniciar_fala
        self.retorno = retorno
        self.interface = interface
        self.caminho_dataBase = caminho_dataBase
        with open(caminho_dataBase, "r", encoding="utf-8") as arquivo:
            self.dados = json.load(arquivo)
            self.nome_assistente = self.dados["nome"]
            self.acoes = self.dados["acoes"]

            arquivo.close()

        self.ATUADORES = [
            {
                "nome": "ar-condicionado",
                "iniciar": iniciar_ar_condicionado,
                "parametro_de_atuacao": None,
                "atuar" : atuar_sobre_ar_condicionado,
                "uni_medida" : None
            },
            {
                "nome": "temperatura",
                "iniciar": iniciar_ar_condicionado,
                "parametro_de_atuacao": None,
                "atuar" : atuar_sobre_ar_condicionado,
                "uni_medida" : None
            },
            {
                "nome": "gps",
                "iniciar": iniciar_gps,
                "parametro_de_atuacao": None,
                "atuar" : atuar_sobre_gps
            }
        ]
        pass
    
    #Função que realiza todas as execuções da assistente
    def iniciar(self):
        obter_audio = capturaAudio(interface=self.interface,iniciar_fala=self.iniciar_fala)
        processar_texto = linguagemNatural()
        retorno_assistente = None
        valido, acao, objeto, valor, uni_medida = False, None, None,None,None

        _,traduzido,_,string_captura_audio = obter_audio.obter_string_captura()
        print(string_captura_audio)
        if traduzido:
            tokens = processar_texto.obter_tokens(string_captura_audio)
            tokens = processar_texto.retirar_palavras_de_parada(tokens)


            valido, acao, objeto, valor, uni_medida = self.validar_comando(tokens, self.nome_assistente, self.acoes)
            print(self.validar_comando(tokens, self.nome_assistente, self.acoes))
            
        if valido:
            retorno_assistente = self.executar_comando(acao,objeto,valor, uni_medida)
            try:
                self.retorno.emit(string_captura_audio,retorno_assistente[objeto])
            except:
                pass
            return string_captura_audio, retorno_assistente[objeto]
        else:
            print("comando inválido, tente novamente")
            return None, None
    #Recebe o comando e realiza a execução dele por meio dos atuadores, caso o mesmo seja validado
    def executar_comando(self, acao, objeto, valor=None, uni_medida=None):
        print(f"Executando ação {acao} sobre o objeto {objeto}")
        dicionario_atuadores = {}
        for atuador in self.ATUADORES:
            parametro_de_atuacao = valor
            uni_medida = uni_medida
            funcao_atuacao = atuador["atuar"]
            dicionario_atuadores[atuador["nome"]] = funcao_atuacao(acao, objeto, valor, uni_medida)


        return dicionario_atuadores
    
    #recebe os tokens e valido se o comando é apto para a assistente executar
    def validar_comando(self, tokens, nome_assistente, lista_de_acoes):
        valido, acao, objeto, valor, uni_medida = False, None, None, None, None

        if len(tokens) >= 3:
            if (tokens[0] == self.nome_assistente):
                acao = tokens[1]
                objeto = tokens[2]
                try:
                    valor = tokens[3]
                    uni_medida = tokens[4]
                except:
                    pass
                for acao_prevista in lista_de_acoes:
                    if(acao in acao_prevista["nome"]):
                        if objeto in acao_prevista["objetos"]:
                            valido = True
        return valido, acao, objeto, valor, uni_medida

if __name__ == "__main__":
    assistente = assistente()
    while True:
        assistente.iniciar()
        time.sleep(3)
