import pickle
import pandas as pd

from .tabela import v2

# Carrega os modelos de IA assim que importado
arvore = pickle.load(open('bot/out/arvore.pkl', 'rb'))
arvore_count = pickle.load(open('bot/out/arvore_count.pkl', 'rb'))
reglog = pickle.load(open('bot/out/reglog.pkl', 'rb'))
reglog_count = pickle.load(open('bot/out/reglog_count.pkl', 'rb'))


def jogar(dealer, player, count=None, regressao=False) -> str:
    '''
    Prevê as jogadas. Retorna uma das strings "pedir", "double", "split" ou "parar". 

    Argumentos:
    - dealer: inteiro que representa o valor da carta virada do dealer
    - player: inteiro que representa o valor somado das cartas do jogador
    - count: (opcional) inteiro que representa o valor do true count
    - regressao: usa o método de regressão linear ao invés da árvore de decisão
    '''

    df = pd.DataFrame([(dealer, player)], columns=['dealer_final', 'player_final'])
        
    r = ''

    if count != None:
        df['true_count'] = count

        if regressao:
            r = reglog_count.predict(df)

        else:
            r = arvore_count.predict(df)

    elif regressao:
        r = reglog.predict(df)

    else:
        r = arvore.predict(df)
        
    match r:
        case 'H':
            return 'HIT'

        case 'D':
            return 'DOUBLE'
            
        case 'P':
            return 'SPLIT'
            
        case 'S':
            return 'STAND'

def jogar_tabela(dealer, player, ace=False, dupla=False) -> str:
    if dupla and not ace:
        player = [int(player / 2), int(player / 2)]

    elif dupla and ace:
        player = [1, 1]

    elif ace:
        player = [1, player-11]

    else:
        player = [player]

    match v2.decisao_tabela(dealer=dealer, cartas=player):
        case 'P':
            return 'HIT'
    
        case 'DB':
            return 'DOUBLE'

        case 'F':
            return 'STAND'

        case 'D':
            return 'SPLIT'
        
        case 'P/D':
            return 'HIT ou STAND'

def main():
    print(jogar(10, 7))
    print(jogar(4, 16))
    print(jogar_tabela('A', [10, 6]))
    print(jogar(5, 10))


if __name__ == '__main__':
    main()
