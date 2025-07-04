import random
from tqdm import tqdm
import matplotlib.pyplot as plt
from MonteCarlo import simular_acoes, valor_mao
from MonteCarloTabela import simular_acao_unica
import bot

# Baralho contínuo global
baralho_1 = (
    [2]*4 + [3]*4 + [4]*4 + [5]*4 + [6]*4 +
    [7]*4 + [8]*4 + [9]*4 + [10]*16 + [11]*4
)
baralho_completo = baralho_1 * 8  # 8 baralhos = 416 cartas
baralho_atual = []
contagem_hi_lo = 0  # contagem corrente

def embaralhar_baralho():
    global baralho_atual, contagem_hi_lo
    baralho_atual = baralho_completo.copy()
    random.shuffle(baralho_atual)
    contagem_hi_lo = 0  # zera contagem ao reembaralhar

def verificar_reembaralhamento():
    if len(baralho_atual) < 78:
        embaralhar_baralho()

def comprar_carta():
    verificar_reembaralhamento()
    carta = baralho_atual.pop()
    atualizar_contagem_hi_lo(carta)
    return carta

def atualizar_contagem_hi_lo(carta):
    global contagem_hi_lo
    if carta in [2, 3, 4, 5, 6]:
        contagem_hi_lo += 1
    elif carta in [10, 11]:
        contagem_hi_lo -= 1

def gerar_mao_aleatoria():
    return [comprar_carta(), comprar_carta()]

def gerar_carta_dealer():
    return comprar_carta()

def jogar_mao(mao_jogador, dealer_carta, func_decisao):
    acao = func_decisao(mao_jogador, dealer_carta)

    if func_decisao == acao_montecarlo:
        resultados = simular_acoes(mao_jogador, dealer_carta, n=200)
        res = resultados.get(acao, {'Vitória': 0, 'Empate': 0, 'Derrota': 0})
    elif func_decisao == acao_montecarlo_tabela:
        _, res = simular_acao_unica(mao_jogador, dealer_carta, n=200)
    else:
        resultados_mc = simular_acoes(mao_jogador, dealer_carta, n=200)
        res = resultados_mc.get(acao, {'Vitória': 0, 'Empate': 0, 'Derrota': 0})

    prob = random.uniform(0, 100)
    if prob <= res['Vitória']:
        resultado_final = "Vitória"
    elif prob <= res['Vitória'] + res['Empate']:
        resultado_final = "Empate"
    else:
        resultado_final = "Derrota"

    return resultado_final

def acao_montecarlo(mao, dealer_carta):
    resultados = simular_acoes(mao, dealer_carta, n=200)
    pode_double = len(mao) == 2
    melhor_acao = None
    maior_vitoria = -1.0
    for acao, res in resultados.items():
        if acao.lower() == "double" and not pode_double:
            continue
        if res['Vitória'] > maior_vitoria:
            maior_vitoria = res['Vitória']
            melhor_acao = acao
    return melhor_acao

def acao_montecarlo_tabela(mao, dealer_carta):
    acao, _ = simular_acao_unica(mao, dealer_carta, n=200)
    return acao

def acao_arvore(mao, dealer_carta):
    return bot.jogar(dealer_carta, valor_mao(mao))

def acao_regressao(mao, dealer_carta):
    return bot.jogar(dealer_carta, valor_mao(mao), regressao=True)

def acao_tabela_internet(mao, dealer_carta):
    return bot.jogar_tabela(dealer_carta, valor_mao(mao))

def calcular_aposta_true_count():
    baralhos_restantes = len(baralho_atual) / 52
    true_count = contagem_hi_lo / baralhos_restantes if baralhos_restantes > 0 else 0
    true_count_int = int(true_count)

    if true_count_int < 0:
        return 5  # aposta mínima 1 ficha mesmo com desvantagem
    elif true_count_int == 0:
        return 5
    elif true_count_int == 1:
        return 10
    elif true_count_int == 2:
        return 20
    elif true_count_int == 3:
        return 30
    elif true_count_int >= 4:
        return 100
    else:
        return 1  # fallback padrão

def obter_faixa_tc(true_count):
    if true_count < 0:
        return "TC < 0"
    elif true_count == 0:
        return "TC = 0"
    elif true_count == 1:
        return "TC = 1"
    elif true_count == 2:
        return "TC = 2"
    elif true_count == 3:
        return "TC = 3"
    else:
        return "TC > 3"

def executar_simulacoes(num_maos=500, fichas_iniciais=1000000):
    embaralhar_baralho()
    funcoes = {
        "Monte Carlo": acao_montecarlo,
        "Monte Carlo + Tabela": acao_montecarlo_tabela,
        "Árvore": acao_arvore,
        "Regressão": acao_regressao,
        "Tabela da Internet": acao_tabela_internet
    }

    fichas = {nome: [fichas_iniciais] for nome in funcoes.keys()}
    resultados_por_tc = {
        faixa: {nome: {"Vitória": 0, "Empate": 0, "Derrota": 0, "Total": 0} for nome in funcoes.keys()}
        for faixa in ["TC < 0", "TC = 0", "TC = 1", "TC = 2", "TC = 3", "TC > 3"]
    }

    for _ in tqdm(range(num_maos), desc="Simulando mãos", unit="mão"):
        aposta = calcular_aposta_true_count()

        if aposta == 0:
            # Pula mão sem apostar quando desvantagem (TC < 0)
            continue

        mao_jogador = gerar_mao_aleatoria()
        dealer_carta = gerar_carta_dealer()

        baralhos_restantes = len(baralho_atual) / 52
        true_count = int(contagem_hi_lo / baralhos_restantes) if baralhos_restantes > 0 else 0
        faixa_tc = obter_faixa_tc(true_count)

        for nome, func in funcoes.items():
            resultado = jogar_mao(mao_jogador, dealer_carta, func)
            fichas_atuais = fichas[nome][-1]

            if resultado == "Vitória":
                fichas[nome].append(fichas_atuais + aposta)
                resultados_por_tc[faixa_tc][nome]["Vitória"] += 1
            elif resultado == "Empate":
                fichas[nome].append(fichas_atuais)
                resultados_por_tc[faixa_tc][nome]["Empate"] += 1
            else:
                fichas[nome].append(fichas_atuais - aposta)
                resultados_por_tc[faixa_tc][nome]["Derrota"] += 1

            resultados_por_tc[faixa_tc][nome]["Total"] += 1

    print("\nDesempenho por faixa de True Count:\n")
    for faixa, estrategias in resultados_por_tc.items():
        print(f"--- {faixa} ---")
        for nome, res in estrategias.items():
            total = res["Total"]
            if total == 0:
                continue
            v = res["Vitória"] / total * 100
            e = res["Empate"] / total * 100
            d = res["Derrota"] / total * 100
            print(f"{nome}: Vitória: {v:.1f}%, Empate: {e:.1f}%, Derrota: {d:.1f}% (n={total})")
        print()

    return fichas

if __name__ == "__main__":
    fichas = executar_simulacoes(num_maos=500, fichas_iniciais=1000000)
    fichas_iniciais = 1000000

    plt.figure(figsize=(12, 7))
    for nome, valores in fichas.items():
        valores_relativos = [v - fichas_iniciais for v in valores]
        plt.plot(valores_relativos, label=nome)
    plt.xlabel("Número da mão")
    plt.ylabel("Variação de fichas")
    plt.title("Evolução da variação das fichas por estratégia no Blackjack")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    plt.show()
