from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QStackedWidget
)
from PySide6.QtCore import Qt
from MonteCarlo import simular_acoes, converter_mao_para_valores, valor_mao
from MonteCarloTabela import simular_acao_unica

import bot

class TelaInicial(QWidget):
    def __init__(self, mao_jogador, mao_dealer):
        super().__init__()
        layout = QVBoxLayout()

        label_titulo = QLabel("<h2>Método/Ação Sugerida:</h2>")
        label_titulo.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(label_titulo)
        layout.addSpacing(20)

        mao_jogador_valores = converter_mao_para_valores(mao_jogador)
        dealer_carta_visivel_valor = converter_mao_para_valores([mao_dealer[0]])[0]

        resultados = simular_acoes(mao_jogador_valores, dealer_carta_visivel_valor, 500)
        pode_double = len(mao_jogador) == 2

        melhor_acao = None
        maior_vitoria = -1.0
        for acao, res in resultados.items():
            if acao.lower() == "double" and not pode_double:
                continue
            if res['Vitória'] > maior_vitoria:
                maior_vitoria = res['Vitória']
                melhor_acao = acao

        label_mc = QLabel(f"<b>Monte Carlo:</b> {melhor_acao}")
        label_mc.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(label_mc)

        acao_tabela, _ = simular_acao_unica(mao_jogador_valores, dealer_carta_visivel_valor, 500)
        label_tabela = QLabel(f"<b>Tabela Matemática:</b> {acao_tabela}")
        label_tabela.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(label_tabela)

        acao_tabela_internet = bot.jogar_tabela(dealer_carta_visivel_valor, valor_mao(mao_jogador_valores))
        label_tabela_internet = QLabel(f'<b>Tabela da Internet:</b> {acao_tabela_internet}')
        label_tabela_internet.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(label_tabela_internet)

        acao_arvore = bot.jogar(dealer_carta_visivel_valor, valor_mao(mao_jogador_valores))
        label_arvore = QLabel(f'<b>Arvore de Decisão:</b> {acao_arvore}')
        label_arvore.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(label_arvore)

        acao_regressao = bot.jogar(dealer_carta_visivel_valor, valor_mao(mao_jogador_valores), regressao=True)
        label_regressao = QLabel(f'<b>Regressão Logística:</b> {acao_regressao}')
        label_regressao.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(label_regressao)

        layout.addStretch()
        self.setLayout(layout)


class Menu1(QWidget):
    def __init__(self, mao_jogador, mao_dealer):
        super().__init__()
        layout = QVBoxLayout()

        titulo = QLabel("<h2>Monte Carlo</h2>")
        titulo.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(titulo)

        mao_jogador_valores = converter_mao_para_valores(mao_jogador)
        dealer_carta_visivel_valor = converter_mao_para_valores([mao_dealer[0]])[0]

        resultados = simular_acoes(mao_jogador_valores, dealer_carta_visivel_valor, 500)

        soma_jogador = valor_mao(mao_jogador_valores)
        dealer_valor = converter_mao_para_valores([mao_dealer[0]])[0]
        resumo = f"<b>Mão do Jogador:</b> {soma_jogador} | <b>Dealer mostra:</b> {dealer_valor}<br><br>"

        pode_double = len(mao_jogador) == 2

        melhor_acao = None
        maior_vitoria = -1.0
        for acao, res in resultados.items():
            if acao.lower() == "double" and not pode_double:
                continue
            if res['Vitória'] > maior_vitoria:
                maior_vitoria = res['Vitória']
                melhor_acao = acao

        for acao, res in resultados.items():
            if acao.lower() == "double" and not pode_double:
                continue
            destaque = "<b> ← Melhor ação!</b>" if acao == melhor_acao else ""
            resumo += f"<b>Ação: {acao}</b>{destaque}<br>"
            resumo += f"&nbsp;&nbsp;Vitória: {res['Vitória']:.2f}%<br>"
            resumo += f"&nbsp;&nbsp;Empate : {res['Empate']:.2f}%<br>"
            resumo += f"&nbsp;&nbsp;Derrota: {res['Derrota']:.2f}%<br><br>"

        resultado_label = QLabel()
        resultado_label.setTextFormat(Qt.TextFormat.RichText)
        resultado_label.setText(resumo)
        resultado_label.setWordWrap(True)

        layout.addWidget(resultado_label)
        layout.addStretch()
        self.setLayout(layout)


class Menu2(QWidget):
    def __init__(self, mao_jogador, mao_dealer):
        super().__init__()
        layout = QVBoxLayout()

        label_titulo = QLabel("<h2>Monte Carlo + Tabela</h2>")
        label_titulo.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(label_titulo)

        mao_jogador_valores = converter_mao_para_valores(mao_jogador)
        mao_dealer_valores = converter_mao_para_valores(mao_dealer)

        soma_jogador = sum(mao_jogador_valores)
        dealer_visivel = mao_dealer_valores[0]

        label_info = QLabel(f"<b>Mão do Jogador:</b> {soma_jogador} | <b>Dealer mostra:</b> {dealer_visivel}")
        label_info.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(label_info)

        acao, resultados = simular_acao_unica(mao_jogador_valores, dealer_visivel, n=500)

        label_acao = QLabel(f"Ação recomendada: <b>{acao}</b>")
        label_acao.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(label_acao)

        label_vitoria = QLabel(f"Vitória: {resultados['Vitória']:.2f}%")
        layout.addWidget(label_vitoria)

        label_empate = QLabel(f"Empate: {resultados['Empate']:.2f}%")
        layout.addWidget(label_empate)

        label_derrota = QLabel(f"Derrota: {resultados['Derrota']:.2f}%")
        layout.addWidget(label_derrota)

        layout.addStretch()
        self.setLayout(layout)


class Menu3(QWidget):
    def __init__(self, mao_jogador, mao_dealer):
        super().__init__()
        layout = QVBoxLayout()

        titulo = QLabel("<h2>Tabela Internet</h2>")
        titulo.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(titulo)

        descricao = QLabel("Aqui será exibida a recomendação baseada na tabela padrão da internet.")
        descricao.setWordWrap(True)
        layout.addWidget(descricao)

        layout.addStretch()
        self.setLayout(layout)


class Menu4(QWidget):
    def __init__(self, mao_jogador, mao_dealer):
        super().__init__()
        layout = QVBoxLayout()

        titulo = QLabel("<h2>Árvore de Decisão</h2>")
        titulo.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(titulo)

        descricao = QLabel("Aqui será exibida a decisão baseada em árvore de decisão treinada.")
        descricao.setWordWrap(True)
        layout.addWidget(descricao)

        layout.addStretch()
        self.setLayout(layout)


class Menu5(QWidget):
    def __init__(self, mao_jogador, mao_dealer):
        super().__init__()
        layout = QVBoxLayout()

        titulo = QLabel("<h2>Regressão Logística</h2>")
        titulo.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(titulo)

        descricao = QLabel("Aqui será exibida a sugestão com base na regressão logística.")
        descricao.setWordWrap(True)
        layout.addWidget(descricao)

        layout.addStretch()
        self.setLayout(layout)


class Menu6(QWidget):
    def __init__(self, mao_jogador, mao_dealer):
        super().__init__()
        layout = QVBoxLayout()

        titulo = QLabel("<h2>Regressão Logística com Contagem de Cartas</h2>")
        titulo.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(titulo)

        descricao = QLabel("Aqui será exibida a sugestão da regressão logística considerando o true count.")
        descricao.setWordWrap(True)
        layout.addWidget(descricao)

        layout.addStretch()
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, maos_jogador, mao_dealer, indice_mao_ativa=0):
        super().__init__()
        self.setWindowTitle("Menu de Dicas")

        self.maos_jogador = maos_jogador
        self.mao_dealer = mao_dealer
        self.indice_mao_ativa = indice_mao_ativa

        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        botao_layout = QHBoxLayout()
        btn_inicial = QPushButton("Resultados")
        btn_menu1 = QPushButton("Monte Carlo")
        btn_menu2 = QPushButton("Tabela + Monte Carlo")
        btn_menu3 = QPushButton("Tabela Internet")
        btn_menu4 = QPushButton("Árvore")
        btn_menu5 = QPushButton("Regressão Logística")
        btn_menu6 = QPushButton("Regressão Logística com CC")

        for btn in [btn_inicial, btn_menu1, btn_menu2, btn_menu3, btn_menu4, btn_menu5, btn_menu6]:
            botao_layout.addWidget(btn)

        self.stack = QStackedWidget()

        self.tela_inicial = TelaInicial(self.maos_jogador[self.indice_mao_ativa], self.mao_dealer)
        self.tela_menu1 = Menu1(self.maos_jogador[self.indice_mao_ativa], self.mao_dealer)
        self.tela_menu2 = Menu2(self.maos_jogador[self.indice_mao_ativa], self.mao_dealer)
        self.tela_menu3 = Menu3(self.maos_jogador[self.indice_mao_ativa], self.mao_dealer)
        self.tela_menu4 = Menu4(self.maos_jogador[self.indice_mao_ativa], self.mao_dealer)
        self.tela_menu5 = Menu5(self.maos_jogador[self.indice_mao_ativa], self.mao_dealer)
        self.tela_menu6 = Menu6(self.maos_jogador[self.indice_mao_ativa], self.mao_dealer)

        self.stack.addWidget(self.tela_inicial)  # índice 0
        self.stack.addWidget(self.tela_menu1)    # índice 1
        self.stack.addWidget(self.tela_menu2)    # índice 2
        self.stack.addWidget(self.tela_menu3)    # índice 3
        self.stack.addWidget(self.tela_menu4)    # índice 4
        self.stack.addWidget(self.tela_menu5)    # índice 5
        self.stack.addWidget(self.tela_menu6)    # índice 6

        main_layout.addLayout(botao_layout)
        main_layout.addWidget(self.stack)

        btn_inicial.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_menu1.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_menu2.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        btn_menu3.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        btn_menu4.clicked.connect(lambda: self.stack.setCurrentIndex(4))
        btn_menu5.clicked.connect(lambda: self.stack.setCurrentIndex(5))
        btn_menu6.clicked.connect(lambda: self.stack.setCurrentIndex(6))

    def atualizar_maos(self, maos_jogador, mao_dealer, indice_mao_ativa):
        self.maos_jogador = maos_jogador
        self.mao_dealer = mao_dealer
        self.indice_mao_ativa = indice_mao_ativa

        for i in reversed(range(self.stack.count())):
            widget = self.stack.widget(i)
            self.stack.removeWidget(widget)
            widget.deleteLater()

        self.tela_inicial = TelaInicial(self.maos_jogador[self.indice_mao_ativa], self.mao_dealer)
        self.tela_menu1 = Menu1(self.maos_jogador[self.indice_mao_ativa], self.mao_dealer)
        self.tela_menu2 = Menu2(self.maos_jogador[self.indice_mao_ativa], self.mao_dealer)
        self.tela_menu3 = Menu3(self.maos_jogador[self.indice_mao_ativa], self.mao_dealer)
        self.tela_menu4 = Menu4(self.maos_jogador[self.indice_mao_ativa], self.mao_dealer)
        self.tela_menu5 = Menu5(self.maos_jogador[self.indice_mao_ativa], self.mao_dealer)
        self.tela_menu6 = Menu6(self.maos_jogador[self.indice_mao_ativa], self.mao_dealer)

        self.stack.addWidget(self.tela_inicial)  # índice 0
        self.stack.addWidget(self.tela_menu1)    # índice 1
        self.stack.addWidget(self.tela_menu2)    # índice 2
        self.stack.addWidget(self.tela_menu3)    # índice 3
        self.stack.addWidget(self.tela_menu4)    # índice 4
        self.stack.addWidget(self.tela_menu5)    # índice 5
        self.stack.addWidget(self.tela_menu6)    # índice 6

        self.stack.setCurrentIndex(0)
