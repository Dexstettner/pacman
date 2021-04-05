import pygame
from pacman import Pacman
from cenario import Cenario
from fantasma import Fantasma
from constants import *

pygame.init()

screen = pygame.display.set_mode((800, 600), 0)

if __name__ == "__main__":
    size = 600 // 30
    clock = pygame.time.Clock()
    pacman = Pacman(size)
    blinky = Fantasma(VERMELHO, size)
    inky = Fantasma(CIANO, size)
    clyde = Fantasma(LARANJA, size)
    pinky = Fantasma(ROSA, size)
    cenario = Cenario(size, pacman)
    cenario.adicionar_movivel(pacman)
    cenario.adicionar_movivel(blinky)
    cenario.adicionar_movivel(inky)
    cenario.adicionar_movivel(clyde)
    cenario.adicionar_movivel(pinky)

    while True:
        # Calcular as regras
        if cenario.estado == JOGANDO:
            pacman.calcular_regras()
            blinky.calcular_regras()
            inky.calcular_regras()
            clyde.calcular_regras()
            pinky.calcular_regras()
        cenario.calcular_regras()

        # Pintar a tela
        screen.fill(PRETO)
        cenario.pintar(screen)
        pacman.pintar(screen)
        blinky.pintar(screen)
        inky.pintar(screen)
        clyde.pintar(screen)
        pinky.pintar(screen)
        pygame.display.update()
        clock.tick(30)

        # Captura os eventos
        eventos = pygame.event.get()
        cenario.processar_eventos(eventos)
        pacman.processar_eventos(eventos)
