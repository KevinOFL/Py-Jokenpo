from tkinter import * 
from tkinter import ttk

class Game:

    def __init__(self, root):
        self.root = root
        self.criarJanelaInicial()

    def janelaPrincipal(self):

        root.title("JOKENPÔ")

        self.titulo = ttk.Label(self.root ,text="JOKENPÔ").grid(column=1, row=0)

        self.btnIniciar = ttk.Button(self.root, text="INICIAR", command=self.iniciarJogo).grid(column=1, row=1)

        self.btnHistorico = ttk.Button(self.root, text="HISTORICO").grid(column=0, row=2)

        self.btnSair = ttk.Button(self.root, text="SAIR", command=root.destroy).grid(column=2, row=2)

    def iniciarJogo(self):
        #Esconde a pagina anterior.
        self.root.withdraw()

        self.janelaGame = Toplevel(self.root)

        self.label = ttk.Label(self.root, text="Esta é a Nova Janela")

        self.btnSairDoJogo = ttk.Button(self.janelaGame, text="SAIR", command=self.sairDoJogo).grid(column=1, row=2)

    def sairDoJogo(self):
        
        self.janelaGame.destroy()
        # Traz de volta a pagina anterior.
        self.root.deiconify()

        


if __name__ == "__main__":
    root = Tk()
    game = Game(root)
    root.mainloop()


