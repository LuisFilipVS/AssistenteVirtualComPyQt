from nltk import word_tokenize, corpus

'''
Classe que utiliza a biblioteca nltk para fazer tratamento de linguagem natural
'''

#Definição da classe
class linguagemNatural():
    def __init__(self, idioma="portuguese"):
        self.idioma = idioma
        self.palavras_de_parada = set(corpus.stopwords.words(self.idioma))

        pass
    #Recebe a string e retorna uma lista com os tokens da mesma
    def obter_tokens(self, texto):
        return word_tokenize(texto.lower())
    
    #Recebe a lista de tokens e retira dela as palavras que não são interessantes para 
    #processamento da linguagem natural
    def retirar_palavras_de_parada(self, tokens, palavras_de_parada=None):
        if palavras_de_parada is None:
            palavras_de_parada = self.palavras_de_parada
        token_filtrados = []
        for item in tokens:
            if item not in palavras_de_parada:
                token_filtrados.append(item)
        #Realização de conversão de ar condicinado para ar-condicionado, caso houver
        for item in token_filtrados:
            if item == 'condicionado':
                try:
                    if token_filtrados[(token_filtrados.index(item)- 1)] == 'ar':
                        token_filtrados[token_filtrados.index(item)- 1] = 'ar-condicionado'
                        token_filtrados.remove('condicionado')
                except Exception as e:
                    pass
        return token_filtrados

if __name__ == "__main__":
    texto = linguagemNatural()
    tokens = texto.obter_tokens("Dinorá ligar o ar condicionado")
    print(tokens)
    print(texto.retirar_palavras_de_parada(tokens))
    
    pass