from tkinter import *
from tkinter import ttk
from db import  criarConexao
from random import randint
from PIL import Image, ImageTk

conexao = criarConexao("dbjokenpo")
cursor = conexao.cursor()

class Game:

    def __init__(self, root):
        """ Função que inicia a tela principal."""
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
        """ Função que gera o widgets INICIAR, HISTORICO e SAIR da Janela Inicial. """
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
        """ Função que gera o widgets da janela do game. """
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
        self.vs = ttk.Label(self.janelaGame, text="VS\n0 - 0")
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

        # Labels com imagen
        self.imgEscolhaPc = ttk.Label(self.janelaGame)
        self.imgEscolhaPlayer = ttk.Label(self.janelaGame)

        self.styleJanelaJogo()

    def janelaDeVitoria(self, idDoVencedor: int):
        """ Função que gera os widgets da janela do vencedor e efetua o armazenamento de dados coletados durante a partida.
         O armazenamento e feito com auxilio de outra função. """
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
        """ Função que gera os widgets da janela do historico de partidas.
        Com o auxilio de uma função que recolhe os dados do banco de dados é mostrado no Treeview todas as partidas e seus dados. """
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
            self.janelaHistorico, text="VER JOGADAS", command=lambda: self.historicoDeRodadas())

        # Box
        self.boxHistorico = ttk.Treeview(
            self.janelaHistorico, columns=("id_partida", "vencedor", "rodadas"), show="headings")
        self.boxHistorico.column("id_partida", minwidth=0, width=215)
        self.boxHistorico.column("vencedor", minwidth=0, width=215)
        self.boxHistorico.column("rodadas", minwidth=0, width=217)
        self.boxHistorico.heading("id_partida", text="ID PARTIDA")
        self.boxHistorico.heading("vencedor", text="VENCEDOR")
        self.boxHistorico.heading("rodadas", text="RODADAS")

        self.styleJanelaHistorico()
        self.mostrarPartidas()

    def historicoDeRodadas(self):
        """ Função que gera os widgets da janela do historico de rodadas.
        Possui os mesmo formato da janela historico de partidas com uma função auxiliar para buscar os dados e ser visualmente mostrado no Treeview. """
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
        self.boxHistoricoRodadas.heading("move_player_1", text="MOVE COMPUTADOR")
        self.boxHistoricoRodadas.heading("move_player_2", text="MOVE PLAYER")
        self.boxHistoricoRodadas.heading("resultado", text="RESULTADO")

        self.styleJanelaHistoricoDeJogadas()
        self.mostrarJogadas()

    # Logica

    def desligar(self, nmrDaJanela: int):
        """ Função que faz junção com os Button do Tkinter.
        Cada janela possui um id e baseado nele a função valida e fecha a janela e volta pro INICIO.
        Na janela de Id = 0 é a janela do game que caso o usuário sai no meio da partida e armazenado no banco de dados as rodadas jogadas
        mas a partida e dada como resultado IMCOMPLETO.
        :nmrDaJanela: Recebe um valor tipo int que indentifica a janela. """
        if nmrDaJanela == 0:
            comando = f'INSERT INTO partidas (vencedor, rodadas) VALUES ("IMCOMPLETA", {self.rodadas})'
            cursor.execute(comando)
            conexao.commit()
            self.armazenaJogadas(self.jogadas)
            self.janelaGame.destroy()
            # Traz de volta a pagina Inicial
            self.root.deiconify()

        elif nmrDaJanela == 1: # Janela Vencedor
            self.janelaVencedor.destroy()
            self.root.deiconify()

        elif nmrDaJanela == 2: # Janela Historico
            self.janelaHistorico.destroy()
            self.root.deiconify()

        elif nmrDaJanela == 3: # Janela Principal
            conexao.close()
            root.destroy()

        elif nmrDaJanela == 4: # Janela Historico de rodadas
            self.janelaHistoricoDeRodadas.destroy()

    def escolhaComputador(self):
        """ Função que gera um número de 0 a 2 que faz referência a escolha do COMPUTADOR.
        :return: Retorna o número gerado.
        """
        computador = randint(0, 2)

        return computador

    def winner(self, escolhaDoPlayer: int):
        """ Função que recebe a escolha do player e aciona outras funções para efetuar a validação e trazer o resultados pra serem mostrado na tela.
        A cada retorno da função auxiliar embate e verificado e armazendo o resultado em uma lista para que no final da partida seja armazenado no banco de dados.
        :escolhaDoPlayer: Recebe um valor do tipo int.
        :return: Retorna o número de rodadas para ser utilizado em outras funções e armazenado no banco de dados.
        """
        # Transmite a escolha do PC e Player pra ser utilizada em outras funções.
        self.escolhaPlayer = escolhaDoPlayer
        self.pc = self.escolhaComputador()

        embate = self.verificarEmbate(self.pc, escolhaDoPlayer)

        self.DBresultado, self.DBjogadaPC, self.DBjogadaPlayer = self.converteJogada(
            embate, self.pc, escolhaDoPlayer)

        if embate == 0:
            self.resultadoRodada.config(text="EMPATE")
            self.jogadas.append(
                [self.rodadas, self.DBjogadaPC, self.DBjogadaPlayer, self.DBresultado])
            self.congelaRodada()
            self.rodadas += 1

        elif embate == 1:
            self.y += 1
            self.resultadoRodada.config(text="PLAYER\nVENCEU")
            self.jogadas.append(
                [self.rodadas, self.DBjogadaPC, self.DBjogadaPlayer, self.DBresultado])
            self.congelaRodada()
            self.rodadas += 1

        elif embate == 2:
            self.x += 1
            self.resultadoRodada.config(text="COMPUTADOR\nVENCEU")
            self.jogadas.append(
                [self.rodadas, self.DBjogadaPC, self.DBjogadaPlayer, self.DBresultado])
            self.congelaRodada()
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

    def converteJogada(self, resultado: int, jogadaPC: int, jogadaPlayer: int):
        """ FUnção auxiliar para pegar a jogada do Player, PC e o resultado do embate para transforma em uma string pra ser armazenado no banco de dados.
        :resultado: Recebe um paramétro tipo Int que se refere ao resultado do embate.
        :jogadaPC: Recebe um paramétro tipo Int que se refere a jogada do PC.
        :jogadaPlayer: Recebe um paramétro tipo Int que se refere a jogada do player.
        :return: Retorna os 3 paramétros que recebeu em uma String cada.
        """
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
        """ Função que percorre uma lista de dados de cada rodada de uma partida e armazena eles no banco de dados.
        Logo quando e finalizado a partida primeiro e gravado a partida e em seguida essa função pega a ultima partida armazenada pelo Id e armazena os dados de cada rodada.
        :jogadas: Recebe uma lista de dados das rodadas que teve em uma partida.
        """
        self.comando = "SELECT MAX(id_partida) AS ultimo_id FROM partidas;"
        cursor.execute(self.comando)

        resultado = cursor.fetchone()
        self.ultimoId = resultado[0]

        for rodada, jogadaPC, jogadaPlayer, resultado in jogadas:

            self.comando = f'INSERT INTO rodadas (id_partida, rodada, move_player_1, move_player_2, resultado) VALUES ({self.ultimoId}, {rodada}, "{jogadaPC}", "{jogadaPlayer}", "{resultado}")'
            cursor.execute(self.comando)
            conexao.commit()

    def mostrarPartidas(self):
        """ Função auxiliar que efetua um SELECT de todas as partidas no banco de dados e insere no Treeview da Janela historico. """
        self.comando = "SELECT * FROM partidas order by id_partida"
        cursor.execute(self.comando)
        res = cursor.fetchall()

        for i in res:
            self.boxHistorico.insert("", "end", values=i)

    def pegarIds(self):
        """ FUnção auxiliar que efetua um SELECT de todos os Ids de partidas e ordena eles do menor para o maior
        e é retornado para ser inserido no Combobox da janela historico.
        :return: Retorna o resultado do SELECT que foi executado. 
        """
        self.comando = "SELECT id_partida FROM partidas order by id_partida"
        cursor.execute(self.comando)
        res = cursor.fetchall()

        return res

    def mostrarJogadas(self):
        """ Função auxiliar que efetua um SELECT baseado no ID da partida que foi escolhido no Combobox da janela historico
        e mostra no Treeview da janela Historico de rodadas todos dados de cada rodada que teve naquela partida.
        """
        self.comando = f'SELECT * FROM rodadas where id_partida ="{self.id}" order by rodada'
        cursor.execute(self.comando)
        res = cursor.fetchall()

        for i in res:
            self.boxHistoricoRodadas.insert("", "end", values=i)

    def atualizarImagen(self, escolhaPc: int, escolhaPlayer: int):
        """ Função auxiliar que baseado na escolha do player e pc é selecionado uma imagen respectiva a escolha e é transformada em um formato 
        que o TkInter aceita para ser mostrado na tela.
        :escolhaPc: Recebe um paramétro tipo Int que se refere a escolha do PC.
        :escolhaPlayer: Recebe um paramétro tipo Int que se refere a escolha do Player. 
        """
        caminhoImagens = {
            0: "E:\\Repositorios\\Py-Jokenpo\\Imagens\\pedra.png",
            1: "E:\\Repositorios\\Py-Jokenpo\\Imagens\\papel.png",
            2: "E:\\Repositorios\\Py-Jokenpo\\Imagens\\tesoura.png"
        }

        imgPc = Image.open(caminhoImagens[escolhaPc])
        imgPlayer = Image.open(caminhoImagens[escolhaPlayer])

        tamanho = (100, 100)
        imgPc = imgPc.resize(tamanho)
        imgPlayer = imgPlayer.resize(tamanho)

        imgPc_Tt = ImageTk.PhotoImage(imgPc)
        imgPlayer_Tk = ImageTk.PhotoImage(imgPlayer)

        self.imgEscolhaPc.config(image=imgPc_Tt)
        self.imgEscolhaPlayer.config(image=imgPlayer_Tk)

        self.imgEscolhaPc.imagem = imgPc_Tt
        self.imgEscolhaPlayer.imagem = imgPlayer_Tk

    def congelaRodada(self):
        """ Função que altera o estado da tela do jogo, desabilitando os botões de escolha do usuário, somente deixando o botão sair habilitado.
        Além disso efetua a execução de outras funções que altera alguns widgets na tela do jogo.
        """
        self.pedra.config(state="disable")
        self.papel.config(state="disable")
        self.tesoura.config(state="disable")
        self.atualizarImagen(self.pc, self.escolhaPlayer)
        self.resultadoRodada.after(2500, self.atualizaResultados)

    def atualizaResultados(self):
        """ Função que altera o estado e alguns elementos dos widgets, habilitando os depois de 2.5 seg os botões de ação do usuário e alterando os dados 
        de rodada e resultado na tela do jogo. 
        """
        self.resultadoRodada.config(text="")
        self.rodadaAtual.config(text=f"RODADA {self.rodadas}")
        self.vs.config(text=f"VS\n{self.x} - {self.y}")
        self.imgEscolhaPc.config(image="")
        self.imgEscolhaPlayer.config(image="")
        self.pedra.config(state="normal")
        self.papel.config(state="normal")
        self.tesoura.config(state="normal")

    # Funções de estilização das Janelas

    def styleJanelaInicial(self):
        """ Função que efetua a estilização dos widgets da Janela Inical. """
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
        """ Função que efetua a estilização dos widgets da Janela do Jogo. """
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
        self.vs.config(font=("Inter", 30, "bold"), anchor="center", justify="center",
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

        # Labels com imagen
        self.imgEscolhaPc.grid(column=0, row=1, rowspan=2)
        self.imgEscolhaPc.config(anchor="center", justify="center", background="#D9D9D9", foreground="#3F3333")
        self.imgEscolhaPlayer.grid(column=2, row=1, rowspan=2)
        self.imgEscolhaPlayer.config(anchor="center", justify="center", background="#D9D9D9", foreground="#3F3333")

    def styleJanelaDaVitoria(self):
        """ Função que efetua a estilização dos widgets da Janela do Vencedor. """
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
        """ Função que efetua a estilização dos widgets da Janela Hitorico. """
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
        """ Função que efetua a estilização dos widgets da Janela Historico de Rodadas. """
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