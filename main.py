from db import cursor
from random import randint


def escolhaComputador():
    computador = randint(0, 2)

    if computador == 0:
        print("Pedra")

    elif computador == 1:
        print("Papel")

    elif computador == 2:
        print("Tesoura")

    return computador


def embate(computador, player):
    resultado = -1
    if computador == player:
        print("Empate")

    elif computador == 0 and player == 1 or computador == 1 and player == 2 or computador == 2 and player == 0:
        resultado = 1  # Player vence
        print("Player Venceu!")

    elif computador == 0 and player == 2 or computador == 1 and player == 0 or computador == 2 and player == 1:
        resultado = 2  # Computador vence
        print("Computador Venceu!")

def humano(): 
    escolha = int(input("Escolha entre: PEDRA(0), PAPEL(1) e TESOURA(2) ="))
    return escolha

embate(escolhaComputador(), humano())
