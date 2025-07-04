import random

# Baralho base 8 decks
baralho_base = [2,3,4,5,6,7,8,9,10,10,10,10,11] * 32

# --- Tabelas de estratégia ---

split_table = {
    (11, 11): {2: "SPLIT", 3: "SPLIT", 4: "SPLIT", 5: "SPLIT", 6: "SPLIT", 7: "SPLIT", 8: "SPLIT", 9: "SPLIT", 10: "SPLIT", 11: "SPLIT"},
    (2, 2):     {2: "SPLIT", 3: "SPLIT", 4: "SPLIT", 5: "SPLIT", 6: "SPLIT", 7: "SPLIT", 8: "HIT", 9: "HIT", 10: "HIT", 11: "HIT"},
    (3, 3):     {2: "SPLIT", 3: "SPLIT", 4: "SPLIT", 5: "SPLIT", 6: "SPLIT", 7: "SPLIT", 8: "HIT", 9: "HIT", 10: "HIT", 11: "HIT"},
    (4, 4):     {2: "HIT", 3: "HIT", 4: "HIT", 5: "SPLIT", 6: "SPLIT", 7: "HIT", 8: "HIT", 9: "HIT", 10: "HIT", 11: "HIT"},
    (5, 5):     {2: "DOUBLE", 3: "DOUBLE", 4: "DOUBLE", 5: "DOUBLE", 6: "DOUBLE", 7: "DOUBLE", 8: "DOUBLE", 9: "DOUBLE", 10: "DOUBLE", 11: "DOUBLE"},
    (6, 6):     {2: "SPLIT", 3: "SPLIT", 4: "SPLIT", 5: "SPLIT", 6: "SPLIT", 7: "HIT", 8: "HIT", 9: "HIT", 10: "HIT", 11: "HIT"},
    (7, 7):     {2: "SPLIT", 3: "SPLIT", 4: "SPLIT", 5: "SPLIT", 6: "SPLIT", 7: "SPLIT", 8: "HIT", 9: "HIT", 10: "HIT", 11: "HIT"},
    (8, 8):     {2: "SPLIT", 3: "SPLIT", 4: "SPLIT", 5: "SPLIT", 6: "SPLIT", 7: "SPLIT", 8: "SPLIT", 9: "SPLIT", 10: "STAND", 11: "STAND"},
    (9, 9):     {2: "SPLIT", 3: "SPLIT", 4: "SPLIT", 5: "SPLIT", 6: "SPLIT", 7: "STAND", 8: "SPLIT", 9: "SPLIT", 10: "STAND", 11: "STAND"},
    (10, 10):   {2: "STAND", 3: "STAND", 4: "STAND", 5: "STAND", 6: "STAND", 7: "STAND", 8: "STAND", 9: "STAND", 10: "STAND", 11: "STAND"},
}

estrategia_hard = {
    (5, 2): "HIT", (5, 3): "HIT", (5, 4): "HIT", (5, 5): "HIT", (5, 6): "HIT", (5, 7): "HIT", (5, 8): "HIT", (5, 9): "HIT", (5, 10): "HIT", (5, 11): "HIT",
    (6, 2): "HIT", (6, 3): "HIT", (6, 4): "HIT", (6, 5): "HIT", (6, 6): "HIT", (6, 7): "HIT", (6, 8): "HIT", (6, 9): "HIT", (6, 10): "HIT", (6, 11): "HIT",
    (7, 2): "HIT", (7, 3): "HIT", (7, 4): "HIT", (7, 5): "HIT", (7, 6): "HIT", (7, 7): "HIT", (7, 8): "HIT", (7, 9): "HIT", (7, 10): "HIT", (7, 11): "HIT",
    (8, 2): "HIT", (8, 3): "HIT", (8, 4): "HIT", (8, 5): "HIT", (8, 6): "HIT", (8, 7): "HIT", (8, 8): "HIT", (8, 9): "HIT", (8, 10): "HIT", (8, 11): "HIT",
    (9, 2): "DOUBLE", (9, 3): "DOUBLE", (9, 4): "DOUBLE", (9, 5): "DOUBLE", (9, 6): "DOUBLE", (9, 7): "HIT", (9, 8): "HIT", (9, 9): "HIT", (9, 10): "HIT", (9, 11): "HIT",
    (10, 2): "DOUBLE", (10, 3): "DOUBLE", (10, 4): "DOUBLE", (10, 5): "DOUBLE", (10, 6): "DOUBLE", (10, 7): "DOUBLE", (10, 8): "DOUBLE", (10, 9): "DOUBLE", (10, 10): "HIT", (10, 11): "HIT",
    (11, 2): "DOUBLE", (11, 3): "DOUBLE", (11, 4): "DOUBLE", (11, 5): "DOUBLE", (11, 6): "DOUBLE", (11, 7): "DOUBLE", (11, 8): "DOUBLE", (11, 9): "DOUBLE", (11, 10): "DOUBLE", (11, 11): "DOUBLE",
    (12, 2): "HIT", (12, 3): "HIT", (12, 4): "STAND", (12, 5): "STAND", (12, 6): "STAND", (12, 7): "HIT", (12, 8): "HIT", (12, 9): "HIT", (12, 10): "HIT", (12, 11): "HIT",
    (13, 2): "STAND", (13, 3): "STAND", (13, 4): "STAND", (13, 5): "STAND", (13, 6): "STAND", (13, 7): "HIT", (13, 8): "HIT", (13, 9): "HIT", (13, 10): "HIT", (13, 11): "HIT",
    (14, 2): "STAND", (14, 3): "STAND", (14, 4): "STAND", (14, 5): "STAND", (14, 6): "STAND", (14, 7): "HIT", (14, 8): "HIT", (14, 9): "HIT", (14, 10): "HIT", (14, 11): "HIT",
    (15, 2): "STAND", (15, 3): "STAND", (15, 4): "STAND", (15, 5): "STAND", (15, 6): "STAND", (15, 7): "HIT", (15, 8): "HIT", (15, 9): "HIT", (15, 10): "HIT", (15, 11): "HIT",
    (16, 2): "STAND", (16, 3): "STAND", (16, 4): "STAND", (16, 5): "STAND", (16, 6): "STAND", (16, 7): "HIT", (16, 8): "HIT", (16, 9): "HIT", (16, 10): "HIT", (16, 11): "HIT",
    (17, 2): "STAND", (17, 3): "STAND", (17, 4): "STAND", (17, 5): "STAND", (17, 6): "STAND", (17, 7): "STAND", (17, 8): "STAND", (17, 9): "STAND", (17, 10): "STAND", (17, 11): "STAND",
    (18, 2): "STAND", (18, 3): "STAND", (18, 4): "STAND", (18, 5): "STAND", (18, 6): "STAND", (18, 7): "STAND", (18, 8): "STAND", (18, 9): "STAND", (18, 10): "STAND", (18, 11): "STAND",
    (19, 2): "STAND", (19, 3): "STAND", (19, 4): "STAND", (19, 5): "STAND", (19, 6): "STAND", (19, 7): "STAND", (19, 8): "STAND", (19, 9): "STAND", (19, 10): "STAND", (19, 11): "STAND",
    (20, 2): "STAND", (20, 3): "STAND", (20, 4): "STAND", (20, 5): "STAND", (20, 6): "STAND", (20, 7): "STAND", (20, 8): "STAND", (20, 9): "STAND", (20, 10): "STAND", (20, 11): "STAND",
}

estrategia_soft = {
    (13, 2): "HIT", (13, 3): "HIT", (13, 4): "HIT", (13, 5): "HIT", (13, 6): "DOUBLE", (13, 7): "STAND", (13, 8): "STAND", (13, 9): "STAND",
    (14, 2): "HIT", (14, 3): "HIT", (14, 4): "DOUBLE", (14, 5): "DOUBLE", (14, 6): "DOUBLE", (14, 7): "DOUBLE", (14, 8): "STAND", (14, 9): "STAND",
    (15, 2): "DOUBLE", (15, 3): "DOUBLE", (15, 4): "DOUBLE", (15, 5): "DOUBLE", (15, 6): "DOUBLE", (15, 7): "DOUBLE", (15, 8): "STAND", (15, 9): "STAND",
    (16, 2): "DOUBLE", (16, 3): "DOUBLE", (16, 4): "DOUBLE", (16, 5): "DOUBLE", (16, 6): "DOUBLE", (16, 7): "DOUBLE", (16, 8): "STAND", (16, 9): "STAND",
    (17, 2): "DOUBLE", (17, 3): "DOUBLE", (17, 4): "DOUBLE", (17, 5): "DOUBLE", (17, 6): "DOUBLE", (17, 7): "DOUBLE", (17, 8): "STAND", (17, 9): "STAND",
    (18, 2): "HIT", (18, 3): "HIT", (18, 4): "HIT", (18, 5): "HIT", (18, 6): "HIT", (18, 7): "STAND", (18, 8): "STAND", (18, 9): "STAND",
    (19, 2): "HIT", (19, 3): "HIT", (19, 4): "HIT", (19, 5): "HIT", (19, 6): "HIT", (19, 7): "HIT", (19, 8): "STAND", (19, 9): "STAND",
    (20, 2): "HIT", (20, 3): "HIT", (20, 4): "HIT", (20, 5): "HIT", (20, 6): "HIT", (20, 7): "HIT", (20, 8): "STAND", (20, 9): "STAND",
}

# --- Funções de jogo / simulação ---

def valor_mao(mao):
    total = 0
    for carta in mao:
        if isinstance(carta, list):
            total += valor_mao(carta)
        else:
            total += carta
    ases = mao.count(11)
    while total > 21 and ases > 0:
        total -= 10
        ases -= 1
    return total

def dealer_joga(mao, baralho):
    while valor_mao(mao) < 17:
        mao.append(baralho.pop())
    return mao

def resultado(jogador_mao, dealer_mao):
    vj = valor_mao(jogador_mao)
    vd = valor_mao(dealer_mao)
    if vj > 21:
        return "derrota"
    if vd > 21:
        return "vitoria"
    if vj > vd:
        return "vitoria"
    if vj == vd:
        return "empate"
    return "derrota"

def continuar_jogo_hit(mao, baralho):
    while valor_mao(mao) < 17:
        mao.append(baralho.pop())
    return mao

def simular_hit(baralho, mao_jogador_inicial, dealer_carta_visivel):
    baralho = baralho.copy()
    random.shuffle(baralho)

    jogador = mao_jogador_inicial.copy()
    dealer = [dealer_carta_visivel, baralho.pop()]

    jogador.append(baralho.pop())
    jogador = continuar_jogo_hit(jogador, baralho)

    dealer = dealer_joga(dealer, baralho)

    return resultado(jogador, dealer)

def simular_stand(baralho, mao_jogador_inicial, dealer_carta_visivel):
    baralho = baralho.copy()
    random.shuffle(baralho)

    jogador = mao_jogador_inicial.copy()
    dealer = [dealer_carta_visivel, baralho.pop()]

    dealer = dealer_joga(dealer, baralho)

    return resultado(jogador, dealer)

def simular_double(baralho, mao_jogador_inicial, dealer_carta_visivel):
    baralho = baralho.copy()
    random.shuffle(baralho)

    jogador = mao_jogador_inicial.copy()
    dealer = [dealer_carta_visivel, baralho.pop()]

    jogador.append(baralho.pop())

    dealer = dealer_joga(dealer, baralho)

    return resultado(jogador, dealer)

def simular_split(baralho, mao_jogador_inicial, dealer_carta_visivel):
    baralho = baralho.copy()
    random.shuffle(baralho)

    dealer = [dealer_carta_visivel, baralho.pop()]

    mao1 = [mao_jogador_inicial[0], baralho.pop()]
    mao2 = [mao_jogador_inicial[1], baralho.pop()]

    while valor_mao(mao1) < 17:
        mao1.append(baralho.pop())
    while valor_mao(mao2) < 17:
        mao2.append(baralho.pop())

    dealer = dealer_joga(dealer, baralho)

    r1 = resultado(mao1, dealer)
    r2 = resultado(mao2, dealer)

    if r1 == "vitoria" or r2 == "vitoria":
        return "vitoria"
    if r1 == "empate" or r2 == "empate":
        return "empate"
    return "derrota"

# --- Funções de estratégia ---

def mao_eh_soft(mao):
    total = sum(mao)
    if 11 in mao and total <= 21:
        return True
    return False

def decidir_acao(mao_jogador, dealer_carta_visivel):
    dealer_valor = dealer_carta_visivel
    mao = mao_jogador.copy()

    # Tentar split
    if len(mao) == 2 and mao[0] == mao[1]:
        par = (mao[0], mao[1])
        if par in split_table and dealer_valor in split_table[par]:
            return split_table[par][dealer_valor]

    # Soft?
    if mao_eh_soft(mao):
        total_soft = sum(mao)
        key = (total_soft, dealer_valor)
        if key in estrategia_soft:
            return estrategia_soft[key]

    # Hard
    total_hard = sum(mao)
    key = (total_hard, dealer_valor)
    if key in estrategia_hard:
        return estrategia_hard[key]

    return "HIT"

def simular_acao_unica(mao_jogador_inicial, dealer_carta_visivel, n=1000):
    acao = decidir_acao(mao_jogador_inicial, dealer_carta_visivel)
    resultados = {"Vitória": 0, "Empate": 0, "Derrota": 0}

    for _ in range(n):
        if acao == "SPLIT":
            res = simular_split(baralho_base, mao_jogador_inicial, dealer_carta_visivel)
        elif acao == "DOUBLE":
            res = simular_double(baralho_base, mao_jogador_inicial, dealer_carta_visivel)
        elif acao == "HIT":
            res = simular_hit(baralho_base, mao_jogador_inicial, dealer_carta_visivel)
        else:  # STAND
            res = simular_stand(baralho_base, mao_jogador_inicial, dealer_carta_visivel)

        if res == "vitoria":
            resultados["Vitória"] += 1
        elif res == "empate":
            resultados["Empate"] += 1
        else:
            resultados["Derrota"] += 1

    total = n
    for k in resultados:
        resultados[k] = resultados[k] / total * 100

    return acao, resultados

# --- Teste rápido ---

if __name__ == "__main__":
    mao = [6, 6]
    dealer = 5
    acao, res = simular_acao_unica(mao, dealer, 10000)
    print(f"Ação: {acao}")
    print(f"Vitória: {res['Vitória']:.2f}%")
    print(f"Empate: {res['Empate']:.2f}%")
    print(f"Derrota: {res['Derrota']:.2f}%")
