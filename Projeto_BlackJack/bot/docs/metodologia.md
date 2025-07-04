...

## MATERIAIS E MÉTODOS

Para o desenvolvimento do simulador, foi utilizada a linguagem de programação
Python na sua versão 3.13.5, com o auxílio das bibliotecas PySide 6.9.1 para a
implementação da interface gráfica, Scikit Learn 1.7.0, Pandas 2.3.0 e Numpy
2.3.1 para o tratamento dos dados de treino e treinamento dos modelos de
machine learning, além do uso da plataforma Jupyter Notebook para a
visualização dos dados. Os dados de treino foram elaborados por Ho (2021),
licensiados sob domínio público e obtidos através da plataforma Kaggle.

...

### Tratamento do conjunto de dados

O conjunto de dados utilizado para o treinamento dos modelos de inteligência
artificial apresenta o resultado de 50 milhões de partidas simuladas, em um
arquivo no formato CSV, onde foram utilizados 8 baralhos comuns de 52 cartas
cada (2 a 10, Ás, Rei, Dama e Valete para os naipes Copas, Espadas, Ouro e
Paus), com uma penetração máxima de 338 cartas até o reembaralhamento. Os dados
foram organizados de forma que cada linha representa uma partida, e cada coluna
uma das variáveis da partida, sendo elas: "shoe_id" (qual dos 8 baralhos foi
utilizado na partida), "cards_remaning" (número de cartas restantes na pilha),
"dealer_up" (carta visível do _dealer_), "initial_hand" (duas cartas iniciais
do jogador), "dealer_final" (as cartas do _dealer_ no final da partida),
"dealer_final_value" (soma dos pontos das cartas do _dealer_), "player_final"
(as cartas do jogador no final da partida), "player_final_value" (a soma dos
pontos das cartas do jogador no final da partida), "actions_taken" (conjunto
de ações tomadas pelo jogador durante a partida, sendo representadas por uma
letra entre "H", "S", "D", "P", "R", "I" e "N"), "run_count" e "true_count"
(que representam valores obtidos através da estratégia de _card-counting_) e,
por fim, "win" (taxa de lucro relativa a aposta inicial).

Isto posto, das colunas presentes no arquivo CSV original, foram utilizadas
apenas "dealer_final", "player_final", "actions_taken" e "win" (e "true_count"
para o treinamento de modelos utilizando a estratégia de _card-counting_).
Foram consideradas apenas as primeiras 25000 partidas a fim de manter o escopo
da aplicação reduzido, e evitar o _over-fitting_ dos modelos em relação aos
dados, e então filtramos as partidas para considerarmos apenas aquelas que
obtiveram resultado positivo (em que a coluna _"win"_ seja maior ou igual a 1).

Assim sendo, para facilitar o treinamento dos modelos de IA, dividimos cada
linha do conjunto de dados em várias linhas que possuam apenas uma ação, a soma
dos valores das cartas na mão do jogador no momento em que a ação foi tomada, a
carta relevada do _dealer_ e o resultado _"win"_ através do excerto de código
apresentado na figura ?.

```
# Divide as ações dos players em vários estados de jogo
for i in range(0, len(df.index)):
    linha = df.loc[i]

    for j in range(0, len(linha['actions_taken'])):
        mao = linha['player_final'][j]
        acoes = linha['actions_taken'][j]

        for k in range(0, len(acoes)):
            acao = acoes[k]

            df = pd.concat([df, pd.DataFrame([{'dealer_final': linha['dealer_final'], 'player_final': sum(mao[:2+k]), 'actions_taken': acoes[k], 'win': linha['win']}])], ignore_index=True)
```
Figura ?: Trecho do código utilizado para o tratamento dos dados

Finalmente, os dados são emabaralhados e dividos em subconjuntos de treino
(80% do conjunto de dados) e teste (20% do conjunto de dados) através do método
_train_test_split()_ da biblioteca Scikit Learn. Por fim, estes subconjuntos
são embaralhados de forma aleatória.

### Treinamento dos modelos de Machine Learning

Como modelos de machine learning, optou-se pelo uso dos modelos de
classificação baseados em Regressão Logística e Árvore de Decisão implementados
na biblioteca Scikit Learn. Cada um foi treinado duas vezes, uma ignorando e a
outra levando em consideração a estratégia de _card-counting_. Como conjunto de
características, foram utilziadas as colunas "dealer_final", "player_final" e
"true_count", com o valor da coluna "win" sendo utilizado como peso para as
amostras e a coluna "actions_taken" como a saída esperada. Por fim, obteve-se
a precisão dos modelos de classificação em relação ao subconjunto de dados de
teste através do método "score()", e então os modelos foram exportados no
formato de arquivos PKL através do método "pickle.dump()", parte da
biblioteca-padrão da linguagem Python, para que possa ser integrado ao
simulador.

### RESULTADOS

...

## Treinamento dos Modelos de Machine Learning

Após o treinamento, podemos observar a precisão dos modelos, em relação aos
subconjuntos de dados teste, na tabela ?.

| Modelo              | Estratégia de Card Counting | Precisão obtida |
| ------------------- | --------------------------- | --------------- |
| Regressão Logística | Não                         | 78,34 %         |
| Regressão Logística | Sim                         | 77,91 %         |
| Árvore de Decisão   | Não                         | 91,94 %         |
| Árvore de Decisão   | Sim                         | 90,15 %         |

Tabela ?: Pontuação dos modelos em relação ao conjunto de dados de teste

Podemos observar que há uma pequena diferença entre a precisão dos modelos com
e sem card-counting, provavelmente decorrente do embaralhamento da ordem das
linhas dos casos de treino e de teste, mas que não representa uma diferença
significativa na prática. Assim sendo, podemos, também, visualizar o aumento de
precisão do modelo de Árvore de Decisão em relação ao modelo de Regressão
Logística proveniente da forma como estes tratam as fronteiras entre os dados.
Uma vez que o modelo de Árvore de Decisão define as classes de forma
determinística, e a Regressão Linear, de forma probabilística. 

...

## REFERÊNCIAS

HO, Dennis. _50 Million Blackjack Hands_. 2021. Disponível em: https://www.kaggle.com/datasets/dennisho/blackjack-hands/. Acesso em: 13 jun. 2025.

_1. Supervised Learning - scikit-learn 1.7.0 documentation_. 2025. https://scikit-learn.org/stable/supervised_learning.html. Acesso em: 3 jul. 2025.
