from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QStackedWidget
)
from PySide6.QtCore import Qt
from MonteCarlo import simular_acoes, converter_mao_para_valores, valor_mao
from MonteCarloTabela import simular_acao_unica



class TelaInicial(QWidget):
    def __init__(self, mao_jogador, mao_dealer):
        super().__init__()
        layout = QVBoxLayout()

        # Título
        label_titulo = QLabel("<h2>Resultado dos Códigos:</h2>")
        label_titulo.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(label_titulo)
        layout.addSpacing(20)

        # Preparação das mãos
        mao_jogador_valores = converter_mao_para_valores(mao_jogador)
        dealer_carta_visivel_valor = converter_mao_para_valores([mao_dealer[0]])[0]

        # === Monte Carlo Tradicional ===
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

        # === Monte Carlo com Tabela ===
        acao_tabela, _ = simular_acao_unica(mao_jogador_valores, dealer_carta_visivel_valor, 500)
        label_tabela = QLabel(f"<b>Tabela Matemática:</b> {acao_tabela}")
        label_tabela.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(label_tabela)

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

        # Converter cartas para valores
        mao_jogador_valores = converter_mao_para_valores(mao_jogador)
        mao_dealer_valores = converter_mao_para_valores(mao_dealer)

        # Exibir soma das cartas do jogador e carta visível do dealer
        soma_jogador = sum(mao_jogador_valores)  # soma simples, pode ajustar se quiser considerar soft hand
        dealer_visivel = mao_dealer_valores[0]

        label_info = QLabel(f"<b>Mão do Jogador:</b> {soma_jogador} | <b>Dealer mostra:</b> {dealer_visivel}")
        label_info.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(label_info)

        # Simular ação usando Monte Carlo + tabela
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

        botao_layout.addWidget(btn_inicial)
        botao_layout.addWidget(btn_menu1)
        botao_layout.addWidget(btn_menu2)

        self.stack = QStackedWidget()

        self.tela_inicial = TelaInicial(self.maos_jogador[self.indice_mao_ativa], self.mao_dealer)
        self.tela_menu1 = Menu1(self.maos_jogador[self.indice_mao_ativa], self.mao_dealer)
        self.tela_menu2 = Menu2(self.maos_jogador[self.indice_mao_ativa], self.mao_dealer)  # Nova tela

        self.stack.addWidget(self.tela_inicial)  # índice 0
        self.stack.addWidget(self.tela_menu1)    # índice 1
        self.stack.addWidget(self.tela_menu2)    # índice 2

        main_layout.addLayout(botao_layout)
        main_layout.addWidget(self.stack)

        btn_inicial.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_menu1.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_menu2.clicked.connect(lambda: self.stack.setCurrentIndex(2))  # Conecta o botão à tela 2

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
        self.tela_menu2 = Menu2(self.maos_jogador[self.indice_mao_ativa], self.mao_dealer)  # Atualiza a nova tela

        self.stack.addWidget(self.tela_inicial)  # índice 0
        self.stack.addWidget(self.tela_menu1)    # índice 1
        self.stack.addWidget(self.tela_menu2)    # índice 2

        self.stack.setCurrentIndex(0)
