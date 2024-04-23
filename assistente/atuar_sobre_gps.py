def iniciar_gps():
    pass

def atuar_sobre_gps(acao,objeto,_a,_b):
    resultado = None
    if acao in ['ligar','ativar'] and objeto == 'gps':
        print("ligando o GPS")
        resultado = "ligando o GPS"
    elif acao in ['desligar','desativar'] and objeto == 'gps':
        print("Desligando o GPS")
        resultado = "Desligando o GPS"

    return resultado
