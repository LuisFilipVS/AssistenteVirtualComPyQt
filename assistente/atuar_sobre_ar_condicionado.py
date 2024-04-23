STAUTS_AR_CONDICIONADO = False

def iniciar_ar_condicionado():
    pass

def atuar_sobre_ar_condicionado(acao, objeto, parametro_de_atuacao, uni_medida):
    global STAUTS_AR_CONDICIONADO
    resultado = None
    if (parametro_de_atuacao and uni_medida) is None:
        if acao in ['ligar', 'ativar'] and objeto == 'ar-condicionado':
            STAUTS_AR_CONDICIONADO = True
            print("Ligando o ar-condicionado")
            resultado = "Ligando o ar-condicionado"
        if acao in ['desligar', 'desativar'] and objeto == 'ar-condicionado':
            STAUTS_AR_CONDICIONADO = False
            print("Desligando o ar-condicionado")
            resultado = "Desligando o ar-condicionado"
    elif (parametro_de_atuacao and uni_medida) is not None:
        if acao in ['ajustar','mudar','alterar'] and objeto == 'temperatura':
            aux = ""
            if not STAUTS_AR_CONDICIONADO:
                print("Ligando a ar-condicionado")
                aux = "Estou ligando o ar-condicionado e "
                STAUTS_AR_CONDICIONADO = True
            print(f'Ajustando a temperatura do ar-condicionado para {parametro_de_atuacao} graus {uni_medida}')
            resultado = aux + f'Ajustando a temperatura do ar-condicionado para {parametro_de_atuacao} graus {uni_medida}'
    
    return resultado
