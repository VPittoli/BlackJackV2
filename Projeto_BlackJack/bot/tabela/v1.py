import random

# Funções para lidar com cartas
def comprar_carta():
    baralho = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]  # 10=10,J,Q,K | 11=A
    return random.choice(baralho)

def valor_mao(mao):
    total = sum(mao)
    # Se estourou e tem Ás, transforma Ás de 11 para 1
    while total > 21 and 11 in mao:
        mao[mao.index(11)] = 1
        total = sum(mao)
    return total

# Estrategia 1: Tabela 
def decisao_tabela(mao, carta_dealer):
    total = valor_mao(mao)
    if total >= 17:
        return 'F'
    elif total >= 13 and carta_dealer in [2, 3, 4, 5, 6]:
        return 'F'
    elif total == 12 and carta_dealer in [4, 5, 6]:
        return 'F'
    else:
        return 'P'

# Estrategia 2: "IA" simplificada sem card counting
def decisao_ia(mao):
    total = valor_mao(mao)
    if total >= 17:
        return 'F'
    else:
        return 'P'

# Dealer joga
def jogar_dealer(mao):
    while valor_mao(mao) < 17:
        mao.append(comprar_carta())
    return mao

# Simula uma partida usando uma estrategia
def jogar_partida(estrategia):
    mao_jogador = [comprar_carta(), comprar_carta()]
    mao_dealer = [comprar_carta(), comprar_carta()]
    carta_dealer_visivel = mao_dealer[0]

    # Jogador joga
    while True:
        if estrategia == 'tabela':
            acao = decisao_tabela(mao_jogador, carta_dealer_visivel)
        elif estrategia == 'ia':
            acao = decisao_ia(mao_jogador)
        if acao == 'F':
            break
        mao_jogador.append(comprar_carta())
        if valor_mao(mao_jogador) > 21:
            break

    # Dealer joga se jogador não estourou
    if valor_mao(mao_jogador) <= 21:
        mao_dealer = jogar_dealer(mao_dealer)

    total_jogador = valor_mao(mao_jogador)
    total_dealer = valor_mao(mao_dealer)

    if total_jogador > 21:
        resultado = 'Perdeu'
    elif total_dealer > 21 or total_jogador > total_dealer:
        resultado = 'Ganhou'
    elif total_jogador == total_dealer:
        resultado = 'Empate'
    else:
        resultado = 'Perdeu'

    return {
        'mao_jogador': mao_jogador,
        'mao_dealer': mao_dealer,
        'total_jogador': total_jogador,
        'total_dealer': total_dealer,
        'resultado': resultado
    }

# Simulação de comparação
print("\n Partida usando TABELA:")
resultado_tabela = jogar_partida('tabela')
print(resultado_tabela)

print("\n Partida usando IA sem Card Counting:")
resultado_ia = jogar_partida('ia')
print(resultado_ia)
