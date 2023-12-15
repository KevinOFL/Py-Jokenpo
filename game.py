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

    def janelaPrincipal(self):
        """ Função que gera a janela principal do game onde se encontra, um botão para INICIAR, outro para SAIR e um outro para ver o HISTORICO de partidas. 
        """

        root.title("JOKENPÔ")

        # Labels
        titulo = ttk.Label(self.root, text="JOKENPÔ").grid(column=1, row=0)

        # Buttons
        btnIniciar = ttk.Button(
            self.root, text="INICIAR",command=self.iniciarJogo).grid(column=1, row=1, sticky="nsew")
        btnHistorico = ttk.Button(
            self.root, text="HISTORICO", command=self.historico).grid(column=0, row=2, sticky="nsew")
        btnSairMenu = ttk.Button(
            self.root, text="SAIR", command=lambda: self.desligar(3)).grid(column=2, row=2, sticky="nsew")
        

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
        self.janelaGame.geometry("650x440")
        self.janelaGame.columnconfigure([0,1,2], weight=1)
        self.janelaGame.rowconfigure([0,1,2,3], weight=1)


        # Labels
        pc = ttk.Label(self.janelaGame, text="COMPUTADOR").grid(
            column=0, row=0, sticky="nsew")
        vs = ttk.Label(self.janelaGame, text="VS").grid(
            column=1, row=0, sticky="nsew")
        player = ttk.Label(self.janelaGame, text="PLAYER").grid(
            column=2, row=0, sticky="nsew")

        # Buttons
        btnSairDoJogo = ttk.Button(self.janelaGame, text="SAIR",
            command=lambda: self.desligar(0)).grid(column=1, row=2, sticky="nsew")
        pedra = ttk.Button(self.janelaGame, text="PEDRA",
            command=lambda: self.winner(0)).grid(column=0, row=3, sticky="nsew")
        papel = ttk.Button(self.janelaGame, text="PAPEL",
            command=lambda: self.winner(1)).grid(column=1, row=3, sticky="nsew")
        tesoura = ttk.Button(self.janelaGame, text="TESOURA",
            command=lambda: self.winner(2)).grid(column=2, row=3, sticky="nsew")

    def janelaDeVitoria(self, idDoVencedor: int):
        """ Função que gera uma janela que mostra o vencedor, aqui aparece alguns dados referénte a partida que você iniciou, o vencedor e um botão para voltar para o INICIO e iniciar uma nova partida.
        :idDoVencedor: Recebe um valor tipo inteiro que baseado nele irá gerar uma tela com dados diferente. 
        """

        # Janela
        self.janelaVencedor = Toplevel(self.root)
        self.janelaVencedor.geometry("650x440")
        self.janelaVencedor.columnconfigure([0,1,2], weight=1)
        self.janelaVencedor.rowconfigure([0,1,2], weight=1)
        

        # Labels
        if idDoVencedor == 1:
            vencedor = ttk.Label(
                self.janelaVencedor, text="VENCEDOR\n  PLAYER!").grid(column=1, row=1, sticky="nsew", columnspan=2)
            self.comando = f'INSERT INTO partidas (vencedor, rodadas) VALUES ("PLAYER", {self.rodadas - 1})'
            cursor.execute(self.comando)
            conexao.commit()
            self.armazenaJogadas(self.jogadas)

        elif idDoVencedor == 2:
            vencedor = ttk.Label(
                self.janelaVencedor, text="VENCEDOR\n COMPUTADOR!").grid(column=1, row=1, sticky="nsew", columnspan=2)
            self.comando = f'INSERT INTO partidas (vencedor, rodadas) VALUES ("COMPUTADOR", {self.rodadas - 1})'
            cursor.execute(self.comando)
            conexao.commit()
            self.armazenaJogadas(self.jogadas)

        qntRodadas = ttk.Label(
            self.janelaVencedor, text=f"QUANTIDADE DE RODADAS: {self.rodadas - 1}").grid(column=1, row=2, sticky="nsew", columnspan=2)

        # Buttons
        btnVoltaMenu = ttk.Button(
            self.janelaVencedor, text="VOLTAR PRO INICIO",command=lambda: self.desligar(1)).grid(column=0, row=0, sticky="nsew")

    def historico(self):

        ids = self.pegarIds()

        self.root.withdraw()

        # Janela
        self.janelaHistorico = Toplevel(self.root)
        self.janelaHistorico.geometry("650x440")
        self.janelaHistorico.columnconfigure(0, weight=1)
        self.janelaHistorico.rowconfigure([0,1,2,3,4], weight=1)
        

        # Labels
        titulo = ttk.Label(
            self.janelaHistorico,text="HISTORICO DE PARTIDAS").grid(column=1, row=0, sticky="nsew")
        obs = ttk.Label(
            self.janelaHistorico, text="Escolha o ID que deseja ver o historico de jogadas: ").grid(column=0, row=1, sticky="nsew", columnspan=2)

        # Select
        self.escolhaId = ttk.Combobox(self.janelaHistorico, values= ids)
        self.escolhaId.grid(column=2, row=1, sticky="nsew")
        
        # Buttons
        btnSairHistorico = ttk.Button(
            self.janelaHistorico, text="SAIR", command=lambda: self.desligar(2)).grid(column=0, row=0, sticky="nsew")
        btnVerPartida = ttk.Button(
            self.janelaHistorico, text="VER JOGADAS", command=lambda: self.historicoDeJogadas()).grid(column=1, row=3, sticky="nsew")

        # Box
        self.boxHistorico = ttk.Treeview(
            self.janelaHistorico, columns=("id_partidas", "vencedor", "rodadas"), show="headings")
        self.boxHistorico.column("id_partidas", minwidth=0, width=80)
        self.boxHistorico.column("vencedor", minwidth=0, width=125)
        self.boxHistorico.column("rodadas", minwidth=0, width=80)
        self.boxHistorico.heading("id_partidas", text="ID PARTIDA")
        self.boxHistorico.heading("vencedor", text="VENCEDOR")
        self.boxHistorico.heading("rodadas", text="RODADAS")
        self.boxHistorico.grid(padx=10, pady=10, sticky="nsew", columnspan=3)
        self.mostrarPartidas()

    def historicoDeJogadas(self):

        self.id = self.escolhaId.get()

        # Janela
        self.janelaHistoricoDeRodadas = Toplevel(self.root)
        self.janelaHistoricoDeRodadas.geometry("650x440")
        self.janelaHistoricoDeRodadas.columnconfigure([0,1], weight=1)
        self.janelaHistoricoDeRodadas.rowconfigure(0, weight=1)

        # Labels
        titulo = ttk.Label(
            self.janelaHistoricoDeRodadas,text=f"HISTORICO DE JOGADAS\nPARTIDA ID: {self.id}").grid(column=1, row=0, sticky="nsew")
        
        # Buttons
        btnSairHistoricoJogadas = ttk.Button(
            self.janelaHistoricoDeRodadas, text="FECHAR", command= lambda: self.desligar(4)).grid(column=0, row=0, sticky="nsew")

        # Box
        self.boxHistoricoRodadas = ttk.Treeview(
            self.janelaHistoricoDeRodadas, columns= ("cod_jogada", "id_partida", "rodada", "move_player_1", "move_player_2", "resultado"), show="headings")
        self.boxHistoricoRodadas.column("cod_jogada", minwidth=0, width=80)
        self.boxHistoricoRodadas.column("id_partida", minwidth=0, width=80)
        self.boxHistoricoRodadas.column("rodada", minwidth=0, width=80)
        self.boxHistoricoRodadas.column("move_player_1", minwidth=0, width=100)
        self.boxHistoricoRodadas.column("move_player_2", minwidth=0, width=100)
        self.boxHistoricoRodadas.column("resultado", minwidth=0, width=150)
        self.boxHistoricoRodadas.heading("cod_jogada", text="COD JOGADA")
        self.boxHistoricoRodadas.heading("id_partida", text="ID PARTIDA")
        self.boxHistoricoRodadas.heading("rodada", text="RODADA Nº")
        self.boxHistoricoRodadas.heading("move_player_1", text="MOVE COMPUTADOR")
        self.boxHistoricoRodadas.heading("move_player_2", text="MOVE PLAYER")
        self.boxHistoricoRodadas.heading("resultado", text="RESULTADO")
        self.boxHistoricoRodadas.grid(padx=10, pady=10, sticky="nsew", columnspan=2)
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

        if computador == 0:
            print("Pedra")

        elif computador == 1:
            print("Papel")

        elif computador == 2:
            print("Tesoura")

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
            print(f"Rodada Nº{self.rodadas} concluída - Resultado: EMPATE \nComputador:",
                self.x, "Jogador:", self.y)
            self.jogadas.append(
                [self.rodadas, self.DBjogadaPC, self.DBjogadaPlayer, self.DBresultado])
            print(self.jogadas)
            self.rodadas += 1

        elif embate == 1:
            self.y += 1
            print(f"Rodada Nº{self.rodadas} concluída - Resultado: PLAYER VENCEU! \nComputador:",
                self.x, "Jogador:", self.y)
            self.jogadas.append(
                [self.rodadas, self.DBjogadaPC, self.DBjogadaPlayer, self.DBresultado])
            print(self.jogadas)
            self.rodadas += 1

        elif embate == 2:
            self.x += 1
            print(f"Rodada Nº{self.rodadas} concluída - Resultado: COMPUTADOR VENCEU! \nComputador:",
                self.x, "Jogador:", self.y)
            self.jogadas.append(
                [self.rodadas, self.DBjogadaPC, self.DBjogadaPlayer, self.DBresultado])
            print(self.jogadas)
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
        

if __name__ == "__main__":
    root = Tk()
    root.geometry("650x440")
    root.columnconfigure([0,1,2], weight=1)
    root.rowconfigure([0,1,2], weight=1)
    game = Game(root)
    root.mainloop()
