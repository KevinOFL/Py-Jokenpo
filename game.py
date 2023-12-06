from tkinter import * 
from tkinter import ttk
from db import cursor
from random import randint

class Game:

    def __init__(self, root):

        """ Função que inicia a tela principal. 
        """

        self.root = root
        self.janelaPrincipal()


    def janelaPrincipal(self):

        """ Função que gera a janela principal do game onde se encontra, um botão para INICIAR, outro para SAIR e um outro para ver o HISTORICO de partidas. 
        """

        root.title("JOKENPÔ")

        #Labels
        self.titulo = ttk.Label(self.root ,text="JOKENPÔ").grid(column=1, row=0)

        #Buttons
        self.btnIniciar = ttk.Button(self.root, text="INICIAR", command=self.iniciarJogo).grid(column=1, row=1)
        self.btnHistorico = ttk.Button(self.root, text="HISTORICO").grid(column=0, row=2)
        self.btnSair = ttk.Button(self.root, text="SAIR", command=root.destroy).grid(column=2, row=2)


    def iniciarJogo(self):

        """ Função que gera a janela onde se joga o game, aqui você irá encontrar 4 botões, 1 para voltar pro INICIO, um para escolher PEDRA, outro para escolher PAPEL e o ultimo será para escolher TESOURA. 
        """

        self.rodadas = 1
        self.x = 0
        self.y = 0

        #Esconde a pagina anterior.
        self.root.withdraw()

        self.janelaGame = Toplevel(self.root)

        #Labels
        self.pc = ttk.Label(self.janelaGame, text="COMPUTADOR").grid(column=0, row=0)
        self.vs = ttk.Label(self.janelaGame, text="VS").grid(column=1, row=0)
        self.player = ttk.Label(self.janelaGame, text="PLAYER").grid(column=2, row=0)

        #Buttons
        self.btnSairDoJogo = ttk.Button(self.janelaGame, text="SAIR", command= lambda : self.voltarProInicio(0)).grid(column=1, row=2)
        self.pedra = ttk.Button(self.janelaGame, text="PEDRA", command= lambda: self.winner(0)).grid(column=0, row=3)
        self.papel = ttk.Button(self.janelaGame, text="PAPEL", command= lambda: self.winner(1)).grid(column=1, row=3)
        self.tesoura = ttk.Button(self.janelaGame, text="TESOURA", command= lambda: self.winner(2)).grid(column=2, row=3)


    def janelaDeVitoria(self, idDoVencedor:int):

        """ Função que gera uma janela que mostra o vencedor, aqui aparece alguns dados referénte a partida que você iniciou, o vencedor e um botão para voltar para o INICIO e iniciar uma nova partida.
        :idDoVencedor: Recebe um valor tipo inteiro que baseado nele irá gerar uma tela com dados diferente. 
        """

        self.janelaVencedor = Toplevel(self.root)

        #Labels
        if idDoVencedor == 1:
            self.vencedor = ttk.Label(self.janelaVencedor, text="VENCEDOR\n  PLAYER!").grid(column=2, row=1)

        elif idDoVencedor ==2:
            self.vencedor = ttk.Label(self.janelaVencedor, text="VENCEDOR\n COMPUTADOR!").grid(column=2, row=1)
        self.qntRodadas = ttk.Label(self.janelaVencedor, text=f"QUANTIDADE DE RODADAS: {self.rodadas}").grid(column=2, row=2)

        #Buttons
        self.btnSair = ttk.Button(self.janelaVencedor, text="VOLTAR PRO INICIO", command= lambda : self.voltarProInicio(1)).grid(column=0, row=0)


    def voltarProInicio(self, nmrDaJanela:int):

        """ Função que faz junção com os Button do Tkinter.
        Cada janela possui um id e baseado nele a função valida e fecha a janela e volta pro INICIO.
        :nmrDaJanela: Recebe um valor tipo int que indentifica a janela.
        """
        
        if nmrDaJanela == 0:
            self.janelaGame.destroy()
            # Traz de volta a pagina anterior.
            self.root.deiconify()
        elif nmrDaJanela == 1:
            self.janelaVencedor.destroy()
            # Traz de volta a pagina anterior.
            self.root.deiconify()
    
    #Logicas

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
    
    
    def winner(self, escolhaDoPlayer:int):

        """ Função que recebe a escolha do player e aciona outras funções para efetuar a validação e trazer o resultado da validação para mostra na tela.
        :escolhaDoPlayer: Recebe um valor do tipo int.
        :return: Retorna o número de rodadas para ser utilizado em outras funções e armazenado no banco de dados.
        """

        pc = self.escolhaComputador()

        embate = self.verificarEmbate(pc, escolhaDoPlayer)
    
        if embate == 0:
            print(f"Rodada Nº{self.rodadas} concluída - Resultado: EMPATE \nComputador:", self.x, "Jogador:", self.y)
            self.rodadas += 1

        elif embate == 1:
            self.y += 1
            print(f"Rodada Nº{self.rodadas} concluída - Resultado: PLAYER VENCEU! \nComputador:", self.x, "Jogador:", self.y)
            self.rodadas += 1

        elif embate == 2:
            self.x += 1
            print(f"Rodada Nº{self.rodadas} concluída - Resultado: COMPUTADOR VENCEU! \nComputador:", self.x, "Jogador:", self.y)
            self.rodadas += 1

        if self.x == 3:
            self.janelaGame.destroy()
            self.janelaDeVitoria(2)
        
        elif self.y == 3:
            self.janelaGame.destroy()
            self.janelaDeVitoria(1)

        return self.rodadas

    
    def verificarEmbate(self, computador:int, player:int):

        """ Função que efetua a validação da escolha do PLAYER e do COMPUTADOR e retorna o resultado.
        :computador: Recebe um valor tipo int que referência a escolha do COMPUTADOR.
        :player: Recebe um valor tipo int que referência a escolha do PLAYER.
        :return: Retorna o resultado onde 0 significa EMPATE, 1 será a vitória do PLAYER e 2 é a vitória do COMPUTADOR.
        """

        resultado = 0

        if computador == player:
            return resultado # EMPATE

        elif computador == 0 and player == 1 or computador == 1 and player == 2 or computador == 2 and player == 0:
            resultado = 1  # Player vence
            return resultado

        elif computador == 0 and player == 2 or computador == 1 and player == 0 or computador == 2 and player == 1:
            resultado = 2  # Computador vence
            return resultado


if __name__ == "__main__":
    root = Tk()
    game = Game(root)
    root.mainloop()