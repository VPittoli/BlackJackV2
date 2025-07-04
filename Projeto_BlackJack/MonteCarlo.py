import random

baralho_base = [2,3,4,5,6,7,8,9,10,10,10,10,11] * 32

def valor_mao(mao):
    total = 0
    for carta in mao:
        if isinstance(carta, list):
            # Se tiver sub-lista, achata ela recursivamente
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

def simular_acoes(mao_jogador_inicial, dealer_carta_visivel, n=10000):
    acoes = {
        "HIT": lambda baralho: simular_hit(baralho, mao_jogador_inicial, dealer_carta_visivel),
        "STAND": lambda baralho: simular_stand(baralho, mao_jogador_inicial, dealer_carta_visivel),
        "DOUBLE": lambda baralho: simular_double(baralho, mao_jogador_inicial, dealer_carta_visivel),
        "SPLIT": lambda baralho: simular_split(baralho, mao_jogador_inicial, dealer_carta_visivel)
    }

    resultados = {}

    for acao, func in acoes.items():
        if acao == "SPLIT" and mao_jogador_inicial[0] != mao_jogador_inicial[1]:
            continue

        vitoria = empate = derrota = 0
        for _ in range(n):
            res = func(baralho_base)
            if res == "vitoria":
                vitoria += 1
            elif res == "empate":
                empate += 1
            else:
                derrota += 1
        total = vitoria + empate + derrota
        resultados[acao] = {
            "Vitória": vitoria / total * 100,
            "Empate": empate / total * 100,
            "Derrota": derrota / total * 100
        }

    return resultados

def converter_mao_para_valores(mao_string):
    mapa_valores = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
        '8': 8, '9': 9, '10': 10, 'V': 10, 'D': 10, 'R': 10, 'A': 11
    }
    valores = []
    for carta in mao_string:
        if carta.startswith('10'):
            val = '10'
        else:
            val = carta[:-1]
        valores.append(mapa_valores[val])
    return valores
