from tkinter import *
from tkinter import ttk
from db import cursor, conexao
from random import randint
from typing import Optional


class Game:

    def __init__(self, root):
        """ Função que inicia a tela principal.
        """
        self.comando = ""
        self.root = root
        self.janelaPrincipal()

        # Configuração da janela
        self.largura = 650
        self.altura = 440

        # Obtém as dimensões da tela
        self.largura_tela = self.root.winfo_screenwidth()
        self.altura_tela = self.root.winfo_screenheight()

        # Calcula as coordenadas para centralizar a janela
        self.x = (self.largura_tela - self.largura) // 2
        self.y = (self.altura_tela - self.altura) // 2

        # Define a geometria da janela
        self.root.geometry(f"{self.largura}x{self.altura}+{self.x}+{self.y}")
        self.root.config(background="#D9D9D9")
        self.root.columnconfigure([0, 1, 2], weight=1)
        self.root.rowconfigure([0, 1, 2], weight=1)

    def janelaPrincipal(self):
        """ Função que gera a janela principal do game onde se encontra, um botão para INICIAR, outro para SAIR e um outro para ver o HISTORICO de partidas. 
        """
        root.title("JOKENPÔ")

        # Labels
        self.titulo = ttk.Label(self.root, text="JOKENPÔ")

        # Buttons
        self.btnIniciar = ttk.Button(
            self.root, text="\nINICIAR\n", command=self.iniciarJogo,)
        self.btnHistorico = ttk.Button(
            self.root, text="\nHISTORICO\n", command=self.historico)
        self.btnSairMenu = ttk.Button(
            self.root, text="\nSAIR\n", command=lambda: self.desligar(3))

        self.styleJanelaInicial()

    def iniciarJogo(self):
        """ Função que gera a janela onde se joga o game, aqui você irá encontrar 4 botões, 1 para voltar pro INICIO, um para escolher PEDRA, outro para escolher PAPEL e o ultimo será para escolher TESOURA. 
        """
        self.jogadas = []
        self.rodadas = 1
        self.x = 0
        self.y = 0

        # Esconde a pagina anterior.
        self.root.withdraw()

        # Janela
        self.janelaGame = Toplevel(self.root)

        # Labels
        self.pc = ttk.Label(self.janelaGame, text="COMPUTADOR")
        self.vs = ttk.Label(self.janelaGame, text="VS")
        self.player = ttk.Label(self.janelaGame, text="PLAYER")
        self.resultadoRodada = ttk.Label(self.janelaGame, text="")
        self.rodadaAtual = ttk.Label(self.janelaGame, text="RODADA 1")

        # Buttons
        self.btnSairDoJogo = ttk.Button(
            self.janelaGame, text="SAIR", command=lambda: self.desligar(0))
        self.pedra = ttk.Button(
            self.janelaGame, text="  \nPEDRA\n  ", command=lambda: self.winner(0))
        self.papel = ttk.Button(
            self.janelaGame, text="  \nPAPEL\n  ", command=lambda: self.winner(1))
        self.tesoura = ttk.Button(
            self.janelaGame, text="  \nTESOURA\n  ", command=lambda: self.winner(2))

        self.styleJanelaJogo()

    def janelaDeVitoria(self, idDoVencedor: int):
        """ Função que gera uma janela que mostra o vencedor, aqui aparece alguns dados referénte a partida que você iniciou, o vencedor e um botão para voltar para o INICIO e iniciar uma nova partida.
        :idDoVencedor: Recebe um valor tipo inteiro que baseado nele irá gerar uma tela com dados diferente. 
        """

        # Janela
        self.janelaVencedor = Toplevel(self.root)

        # Labels
        if idDoVencedor == 1:
            self.text = ttk.Label(self.janelaVencedor, text="VENCEDOR")
            self.vencedor = ttk.Label(self.janelaVencedor, text="PLAYER")
            self.comando = f'INSERT INTO partidas (vencedor, rodadas) VALUES ("PLAYER", {self.rodadas - 1})'
            cursor.execute(self.comando)
            conexao.commit()
            self.armazenaJogadas(self.jogadas)

        elif idDoVencedor == 2:
            self.text = ttk.Label(self.janelaVencedor, text="VENCEDOR")
            self.vencedor = ttk.Label(self.janelaVencedor, text="COMPUTADOR")
            self.comando = f'INSERT INTO partidas (vencedor, rodadas) VALUES ("COMPUTADOR", {self.rodadas - 1})'
            cursor.execute(self.comando)
            conexao.commit()
            self.armazenaJogadas(self.jogadas)

        self.qntRodadas = ttk.Label(
            self.janelaVencedor, text=f"QUANTIDADE DE RODADAS: {self.rodadas - 1}")

        # Buttons
        self.btnVoltaMenu = ttk.Button(
            self.janelaVencedor, text="VOLTAR PRO INICIO", command=lambda: self.desligar(1))

        self.styleJanelaDaVitoria()

    def historico(self):

        ids = self.pegarIds()

        self.root.withdraw()

        # Janela
        self.janelaHistorico = Toplevel(self.root)

        # Labels
        self.titulo = ttk.Label(
            self.janelaHistorico, text="HISTORICO DE PARTIDAS")
        self.obs = ttk.Label(
            self.janelaHistorico, text="Escolha um ID para ver o historico de jogadas:")

        # Select
        self.escolhaId = ttk.Combobox(self.janelaHistorico, values=ids)

        # Buttons
        self.btnSairHistorico = ttk.Button(
            self.janelaHistorico, text="SAIR", command=lambda: self.desligar(2))
        self.btnVerPartida = ttk.Button(
            self.janelaHistorico, text="VER JOGADAS", command=lambda: self.historicoDeJogadas())

        # Box
        self.boxHistorico = ttk.Treeview(
            self.janelaHistorico, columns=("id_partidas", "vencedor", "rodadas"), show="headings")
        self.boxHistorico.column("id_partidas", minwidth=0, width=215)
        self.boxHistorico.column("vencedor", minwidth=0, width=215)
        self.boxHistorico.column("rodadas", minwidth=0, width=217)
        self.boxHistorico.heading("id_partidas", text="ID PARTIDA")
        self.boxHistorico.heading("vencedor", text="VENCEDOR")
        self.boxHistorico.heading("rodadas", text="RODADAS")

        self.styleJanelaHistorico()
        self.mostrarPartidas()

    def historicoDeJogadas(self):

        self.id = self.escolhaId.get()

        # Janela
        self.janelaHistoricoDeRodadas = Toplevel(self.root)

        # Labels
        self.titulo = ttk.Label(
            self.janelaHistoricoDeRodadas, text=f"HISTORICO DE JOGADAS\nPARTIDA ID: {self.id}")

        # Buttons
        self.btnSairHistoricoJogadas = ttk.Button(
            self.janelaHistoricoDeRodadas, text="FECHAR", command=lambda: self.desligar(4))

        # Box
        self.boxHistoricoRodadas = ttk.Treeview(
            self.janelaHistoricoDeRodadas, columns=("cod_jogada", "id_partida", "rodada", "move_player_1", "move_player_2", "resultado"), show="headings")
        self.boxHistoricoRodadas.column("cod_jogada", minwidth=0, width=80)
        self.boxHistoricoRodadas.column("id_partida", minwidth=0, width=80)
        self.boxHistoricoRodadas.column("rodada", minwidth=0, width=80)
        self.boxHistoricoRodadas.column("move_player_1", minwidth=0, width=100)
        self.boxHistoricoRodadas.column("move_player_2", minwidth=0, width=100)
        self.boxHistoricoRodadas.column("resultado", minwidth=0, width=150)
        self.boxHistoricoRodadas.heading("cod_jogada", text="COD JOGADA")
        self.boxHistoricoRodadas.heading("id_partida", text="ID PARTIDA")
        self.boxHistoricoRodadas.heading("rodada", text="RODADA Nº")
        self.boxHistoricoRodadas.heading(
            "move_player_1", text="MOVE COMPUTADOR")
        self.boxHistoricoRodadas.heading("move_player_2", text="MOVE PLAYER")
        self.boxHistoricoRodadas.heading("resultado", text="RESULTADO")

        self.styleJanelaHistoricoDeJogadas()
        self.mostrarJogadas()


    # Logica

    def desligar(self, nmrDaJanela: int):
        """ Função que faz junção com os Button do Tkinter.
        Cada janela possui um id e baseado nele a função valida e fecha a janela e volta pro INICIO.
        :nmrDaJanela: Recebe um valor tipo int que indentifica a janela.
        """

        if nmrDaJanela == 0:
            comando = f'INSERT INTO partidas (vencedor, rodadas) VALUES ("IMCOMPLETA", {self.rodadas})'
            cursor.execute(comando)
            conexao.commit()
            self.armazenaJogadas(self.jogadas)
            self.janelaGame.destroy()
            # Traz de volta a pagina Inicial
            self.root.deiconify()

        elif nmrDaJanela == 1:
            self.janelaVencedor.destroy()
            self.root.deiconify()

        elif nmrDaJanela == 2:
            self.janelaHistorico.destroy()
            self.root.deiconify()

        elif nmrDaJanela == 3:
            conexao.close()
            root.destroy()

        elif nmrDaJanela == 4:
            self.janelaHistoricoDeRodadas.destroy()

    def escolhaComputador(self):
        """ Função que gera um número de 0 a 2 que faz referência a escolha do COMPUTADOR.
        :return: Retorna o número gerado.
        """

        computador = randint(0, 2)

        return computador

    def winner(self, escolhaDoPlayer: int):
        """ Função que recebe a escolha do player e aciona outras funções para efetuar a validação e trazer o resultado da validação para mostra na tela.
        :escolhaDoPlayer: Recebe um valor do tipo int.
        :return: Retorna o número de rodadas para ser utilizado em outras funções e armazenado no banco de dados.
        """

        pc = self.escolhaComputador()

        embate = self.verificarEmbate(pc, escolhaDoPlayer)

        self.DBresultado, self.DBjogadaPC, self.DBjogadaPlayer = self.converteJogada(
            embate, pc, escolhaDoPlayer)

        if embate == 0:
            self.resultadoRodada.config(text="EMPATE")
            self.jogadas.append(
                [self.rodadas, self.DBjogadaPC, self.DBjogadaPlayer, self.DBresultado])
            self.atulizarRodada()
            self.rodadas += 1

        elif embate == 1:
            self.y += 1
            self.resultadoRodada.config(text="PLAYER\nVENCEU")
            self.jogadas.append(
                [self.rodadas, self.DBjogadaPC, self.DBjogadaPlayer, self.DBresultado])
            self.atulizarRodada()
            self.rodadas += 1

        elif embate == 2:
            self.x += 1
            self.resultadoRodada.config(text="COMPUTADOR\nVENCEU")
            self.jogadas.append(
                [self.rodadas, self.DBjogadaPC, self.DBjogadaPlayer, self.DBresultado])
            self.atulizarRodada()
            self.rodadas += 1

        if self.x == 3:
            self.janelaGame.destroy()
            self.janelaDeVitoria(2)

        elif self.y == 3:
            self.janelaGame.destroy()
            self.janelaDeVitoria(1)

        return self.rodadas

    def verificarEmbate(self, computador: int, player: int):
        """ Função que efetua a validação da escolha do PLAYER e do COMPUTADOR e retorna o resultado.
        :computador: Recebe um valor tipo int que referência a escolha do COMPUTADOR.
        :player: Recebe um valor tipo int que referência a escolha do PLAYER.
        :return: Retorna o resultado onde 0 significa EMPATE, 1 será a vitória do PLAYER e 2 é a vitória do COMPUTADOR.
        """

        resultado = 0

        if computador == player:
            self.resultadoRodada.config(text="EMPATE")
            return resultado  # EMPATE

        elif computador == 0 and player == 1 or computador == 1 and player == 2 or computador == 2 and player == 0:
            resultado = 1  # Player vence
            return resultado

        elif computador == 0 and player == 2 or computador == 1 and player == 0 or computador == 2 and player == 1:
            resultado = 2  # Computador vence
            return resultado

    def converteJogada(self, resultado: int, jogadaPC: Optional[int] = None, jogadaPlayer: Optional[int] = None):

        if jogadaPC == 0:
            jogadaPC = "PEDRA"
        elif jogadaPC == 1:
            jogadaPC = "PAPEL"
        elif jogadaPC == 2:
            jogadaPC = "TESOURA"

        if jogadaPlayer == 0:
            jogadaPlayer = "PEDRA"
        elif jogadaPlayer == 1:
            jogadaPlayer = "PAPEL"
        elif jogadaPlayer == 2:
            jogadaPlayer = "TESOURA"

        if resultado == 0:
            resultado = "EMPATE"
        elif resultado == 1:
            resultado = "PLAYER VENCEU"
        elif resultado == 2:
            resultado = "COMPUTADOR VENCEU"

        return resultado, jogadaPC, jogadaPlayer

    def armazenaJogadas(self, jogadas: list):

        self.comando = "SELECT MAX(id_partidas) AS ultimo_id FROM partidas;"
        cursor.execute(self.comando)

        resultado = cursor.fetchone()
        self.ultimoId = resultado[0]

        for rodada, jogadaPC, jogadaPlayer, resultado in jogadas:

            self.comando = f'INSERT INTO jogadas (id_partida, rodada, move_player_1, move_player_2, resultado) VALUES ({self.ultimoId}, {rodada}, "{jogadaPC}", "{jogadaPlayer}", "{resultado}")'
            cursor.execute(self.comando)
            conexao.commit()

    def mostrarPartidas(self):
        self.comando = "SELECT * FROM partidas order by id_partidas"
        cursor.execute(self.comando)
        res = cursor.fetchall()

        for i in res:
            self.boxHistorico.insert("", "end", values=i)

    def pegarIds(self):
        self.comando = "SELECT id_partidas FROM partidas order by id_partidas"
        cursor.execute(self.comando)
        res = cursor.fetchall()

        return res

    def mostrarJogadas(self):
        self.comando = f'SELECT * FROM jogadas where id_partida ="{self.id}" order by rodada'
        cursor.execute(self.comando)
        res = cursor.fetchall()

        for i in res:
            self.boxHistoricoRodadas.insert("", "end", values=i)

    def atulizarRodada(self):
        self.pedra.config(state="disable")
        self.papel.config(state="disable")
        self.tesoura.config(state="disable")
        self.resultadoRodada.after(2200, self.limparResultado)

    def limparResultado(self):
        self.resultadoRodada.config(text="")
        self.rodadaAtual.config(text=f"RODADA {self.rodadas}")
        self.pedra.config(state="normal")
        self.papel.config(state="normal")
        self.tesoura.config(state="normal")


    # Funções de estilização das telas

    def styleJanelaInicial(self):

        estilo = ttk.Style()

        # Labels
        self.titulo.config(font=("Inter", 86, "bold"),
                           foreground="#3F3333", background="#D9D9D9")
        self.titulo.grid(column=0, row=0, columnspan=3)

        # Buttons
        estilo.configure("TButton", background="#3F3333",
                         foreground="#3F3333", font=("Inter", 15))
        self.btnIniciar.grid(column=1, row=1)
        self.btnHistorico.grid(column=0, row=2)
        self.btnSairMenu.grid(column=2, row=2)

    def styleJanelaJogo(self):

        # Janela
        self.janelaGame.config(background="#D9D9D9")
        self.janelaGame.geometry("650x440+443+212")
        self.janelaGame.columnconfigure([0, 1, 2], weight=1)
        self.janelaGame.rowconfigure([1, 2, 3, 4], weight=1)

        # Labels
        self.pc.grid(column=0, row=0, sticky="nw")
        self.pc.config(font=("Inter", 16, "bold"),
                       background="#D9D9D9", foreground="#3F3333")
        self.vs.grid(column=1, row=0, sticky="n")
        self.vs.config(font=("Inter", 30, "bold"),
                       background="#D9D9D9", foreground="#3F3333")
        self.player.grid(column=2, row=0, sticky="ne")
        self.player.config(font=("Inter", 16, "bold"),
                           background="#D9D9D9", foreground="#3F3333")
        self.resultadoRodada.grid(column=1, row=2)
        self.resultadoRodada.config(font=("Inter", 30, "bold"), anchor="center", justify="center",
                                    background="#D9D9D9", foreground="#3F3333")
        self.rodadaAtual.grid(column=1, row=1)
        self.rodadaAtual.config(font=("Inter", 25, "bold"), anchor="center", justify="center",
                                background="#D9D9D9", foreground="#3F3333")

        # Buttons
        self.btnSairDoJogo.grid(column=1, row=3)
        self.pedra.grid(column=0, row=4)
        self.papel.grid(column=1, row=4)
        self.tesoura.grid(column=2, row=4)

    def styleJanelaDaVitoria(self):

        # Janela
        self.janelaVencedor.config(background="#D9D9D9")
        self.janelaVencedor.geometry("650x440+443+212")
        self.janelaVencedor.columnconfigure([0, 1, 2], weight=1)
        self.janelaVencedor.rowconfigure([1, 2, 3], weight=1)

        # Labels
        self.text.grid(column=0, row=1, columnspan=3)
        self.text.config(font=("Inter", 25),
                         background="#D9D9D9", foreground="#3F3333")
        self.vencedor.grid(column=0, row=2, columnspan=3)
        self.vencedor.config(font=("Inter", 45, "bold"),
                             background="#D9D9D9", foreground="#3F3333")
        self.qntRodadas.grid(column=0, row=3, columnspan=3)
        self.qntRodadas.config(
            font=("Inter", 20), background="#D9D9D9", foreground="#3F3333")

        # Buttons
        self.btnVoltaMenu.grid(column=0, row=0, sticky="nw")

    def styleJanelaHistorico(self):

        estilo = ttk.Style()

        # Janela
        self.janelaHistorico.config(background="#D9D9D9")
        self.janelaHistorico.geometry("650x440+443+212")
        self.janelaHistorico.rowconfigure([0, 1, 2, 3, 4], weight=1)

        # Labels
        self.titulo.grid(column=1, row=0, columnspan=3, sticky="nswe")
        self.titulo.config(font=("Inter", 20, "bold"),
                           background="#D9D9D9", foreground="#3F3333")
        self.obs.grid(column=0, row=1, columnspan=3)
        self.obs.config(font=("Inter", 12, "bold"),
                        background="#D9D9D9", foreground="#3F3333")

        # Select
        self.escolhaId.grid(column=3, row=1)
        self.escolhaId.config(font=("Inter", 11, "bold"), width=4)

        # Buttons
        self.btnSairHistorico.grid(column=0, row=0)
        self.btnVerPartida.grid(column=3, row=3)

        # Box
        self.boxHistorico.grid(column=0, row=4, columnspan=4)
        estilo.configure("Treeview", foreground="#3F3333", font=("Inter", 10))

    def styleJanelaHistoricoDeJogadas(self):

        # Janela
        self.janelaHistoricoDeRodadas.config(background="#D9D9D9")
        self.janelaHistoricoDeRodadas.geometry("650x440+400+100")
        self.janelaHistoricoDeRodadas.columnconfigure([0, 1], weight=1)
        self.janelaHistoricoDeRodadas.rowconfigure([0, 1], weight=1)

        # Labels
        self.titulo.grid(column=1, row=0)
        self.titulo.config(font=("Inter", 23, "bold"),
                           background="#D9D9D9", foreground="#3F3333")

        # Buttons
        self.btnSairHistoricoJogadas.grid(column=0, row=0)

        # Box
        self.boxHistoricoRodadas.grid(column=0, row=1, columnspan=2)


if __name__ == "__main__":
    root = Tk()
    game = Game(root)
    root.mainloop()
