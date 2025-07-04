import random

# ====================================
# BLACKJACK: TABELA DE ESTRATÉGIA FIXA
# ====================================

# Tabela de decisão resumida (adicione tudo que precisar)
tabela = {
    (8, 2): 'P', (8, 3): 'P', (8, 4): 'P', (8, 5): 'P', (8, 6): 'P', (8, 7): 'P', (8, 8): 'P', (8, 9): 'P', (8, 10): 'P', (8, 11): 'P',
    (9, 2): 'DB', (9, 3): 'DB', (9, 4): 'DB', (9, 5): 'DB', (9, 6): 'DB', (9, 7): 'P', (9, 8): 'P', (9, 9): 'P', (9, 10): 'P', (9, 11): 'P',
    (10, 2): 'DB', (10, 3): 'DB', (10, 4): 'DB', (10, 5): 'DB', (10, 6): 'DB', (10, 7): 'DB', (10, 8): 'DB', (10, 9): 'DB', (10, 10): 'P', (10, 11): 'P',
    (11, 2): 'DB', (11, 3): 'DB', (11, 4): 'DB', (11, 5): 'DB', (11, 6): 'DB', (11, 7): 'DB', (11, 8): 'DB', (11, 9): 'DB', (11, 10): 'DB', (11, 11): 'DB',
    (17, 2): 'F', (17, 3): 'F', (17, 4): 'F', (17, 5): 'F', (17, 6): 'F', (17, 7): 'F', (17, 8): 'F', (17, 9): 'F', (17, 10): 'F', (17, 11): 'F',
    # Soft
    ('A,6', 2): 'DB', ('A,6', 3): 'DB', ('A,6', 4): 'DB', ('A,6', 5): 'DB', ('A,6', 6): 'DB', ('A,6', 7): 'F', ('A,6', 8): 'P',
    # Par
    ('8,8', 2): 'D', ('8,8', 3): 'D', ('8,8', 4): 'D', ('8,8', 5): 'D', ('8,8', 6): 'D', ('8,8', 7): 'D', ('8,8', 8): 'D', ('8,8', 9): 'D', ('8,8', 10): 'D', ('8,8', 11): 'D',
    ('A,A', 2): 'D', ('A,A', 3): 'D', ('A,A', 4): 'D', ('A,A', 5): 'D', ('A,A', 6): 'D', ('A,A', 7): 'D',
}

# ================================
# Funções de jogo
# ================================

def comprar_carta():
    baralho = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 1]  # A=1, soma ajusta depois
    return random.choice(baralho)

def valor_mao(mao):
    total = sum(mao)
    if 1 in mao and total + 10 <= 21:
        return total + 10  # A vira 11
    return total

def tipo_mao(mao):
    if len(mao) == 2 and mao[0] == mao[1]:
        return 'par'
    elif 1 in mao:
        return 'soft'
    else:
        return 'hard'

def total_mao(mao):
    if tipo_mao(mao) == 'par':
        return f"{mao[0]},{mao[1]}"
    elif tipo_mao(mao) == 'soft':
        return f"A,{sum(mao) - 1}"
    else:
        return valor_mao(mao)

def decisao_tabela(mao, dealer_card):
    dealer = 11 if dealer_card == 1 else dealer_card
    chave = (total_mao(mao), dealer)
    return tabela.get(chave, 'P')

def dealer_joga(mao):
    while valor_mao(mao) < 17:
        mao.append(comprar_carta())
    return mao

# ================================
# Simulação com vários jogadores
# ================================

def simular_jogo(num_jogadores=2):
    # Dealer
    mao_dealer = [comprar_carta(), comprar_carta()]
    dealer_visivel = mao_dealer[0]

    print(f"\n=== Dealer: {mao_dealer} (Visível: {dealer_visivel}) ===\n")

    # Jogadores
    jogadores = []
    for i in range(num_jogadores):
        mao = [comprar_carta(), comprar_carta()]
        jogador = {'mao': mao, 'acoes': [], 'final': None}
        while True:
            acao = decisao_tabela(jogador['mao'], dealer_visivel)
            jogador['acoes'].append((list(jogador['mao']), acao))
            if acao in ['F', 'F/D', 'P/D', 'D', 'DB']:
                break
            jogador['mao'].append(comprar_carta())
            if valor_mao(jogador['mao']) > 21:
                break
        jogadores.append(jogador)

    # Dealer joga
    mao_dealer_final = dealer_joga(mao_dealer)
    dealer_total = valor_mao(mao_dealer_final)

    # Resultados
    for idx, jogador in enumerate(jogadores):
        total = valor_mao(jogador['mao'])
        if total > 21:
            jogador['final'] = 'Perdeu'
        elif dealer_total > 21 or total > dealer_total:
            jogador['final'] = 'Ganhou'
        elif total == dealer_total:
            jogador['final'] = 'Empate'
        else:
            jogador['final'] = 'Perdeu'

    # Mostrar tudo
    for idx, jogador in enumerate(jogadores):
        print(f"--- Jogador {idx+1} ---")
        print(f"Cartas finais: {jogador['mao']} (Total: {valor_mao(jogador['mao'])})")
        print(f"Ações:")
        for m, a in jogador['acoes']:
            print(f"  Mão: {m} => Ação: {a}")
        print(f"Resultado final: {jogador['final']}")
        print()

    print(f"Dealer final: {mao_dealer_final} (Total: {dealer_total})\n")

# ================================
# Rodar exemplo
# ================================

simular_jogo(num_jogadores=2)
