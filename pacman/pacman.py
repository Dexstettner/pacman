import pygame
from constants import *
from elementojogo import ElementoJogo
from movivel import Movivel

class Pacman(ElementoJogo, Movivel):
    def __init__(self, tamanho):
        self.coluna = PACMAN_X_START_POSITION
        self.linha = PACMAN_Y_START_POSITION
        self.centro_x = 400
        self.centro_y = 300
        self.tamanho = tamanho
        self.vel_x = VELOCIDADE
        self.vel_y = 0
        self.raio = self.tamanho // 2
        self.coluna_intencao = self.coluna
        self.linha_intencao = self.linha
        self.direcao = DIREITA
        self.abertura = 0
        self.velocidade_abertura = VELOCIDADE * 2

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna

    def mudar_direcao(self, direcoes):
        pass

    def calcular_regras(self):
        self.coluna_intencao = self.coluna + self.vel_x
        self.linha_intencao = self.linha + self.vel_y
        self.centro_x = int(self.coluna * self.tamanho + self.raio)
        self.centro_y = int(self.linha * self.tamanho + self.raio)

    def pintar(self, tela):
        # Desenhar o corpo do Pacman
        pygame.draw.circle(tela, AMARELO, (self.centro_x, self.centro_y), self.raio, 0)

        self.abertura += self.velocidade_abertura
        if self.abertura > self.raio:
            self.velocidade_abertura = -VELOCIDADE * 2
        if self.abertura <= 0:
            self.velocidade_abertura = VELOCIDADE * 2

        # Desenho da boca do Pacman
        canto_boca = (self.centro_x, self.centro_y)
        # Start direction
        labio_superior = (self.centro_x + self.raio - 1, self.centro_y - self.abertura)
        labio_inferior = (self.centro_x + self.raio - 1, self.centro_y + self.abertura)

        if self.direcao == DIREITA:
            labio_superior = (self.centro_x + self.raio - 1, self.centro_y - self.abertura)
            labio_inferior = (self.centro_x + self.raio - 1, self.centro_y + self.abertura)

        elif self.direcao == ESQUERDA:
            labio_superior = (self.centro_x + self.raio * -1, self.centro_y - self.abertura)
            labio_inferior = (self.centro_x + self.raio * -1, self.centro_y + self.abertura)

        elif self.direcao == ABAIXO:
            labio_superior = (self.centro_x + self.abertura, self.centro_y + self.raio - 1)
            labio_inferior = (self.centro_x - self.abertura, self.centro_y + self.raio - 1)

        elif self.direcao == ACIMA:
            labio_superior = (self.centro_x + self.abertura, self.centro_y + self.raio * -1)
            labio_inferior = (self.centro_x - self.abertura, self.centro_y + self.raio * -1)

        pontos = [canto_boca, labio_superior, labio_inferior]
        pygame.draw.polygon(tela, PRETO, pontos, 0)

        # Olho do Pacman
        if self.direcao == ESQUERDA or self.direcao == DIREITA:
            olho_x = int(self.centro_x + self.raio / 3)
            olho_y = int(self.centro_y - self.raio * 0.70)
        else:
            olho_x = int(self.centro_x - self.raio * 0.70)
            olho_y = int(self.centro_y + self.raio / 3)

        olho_raio = int(self.raio / 10)
        pygame.draw.circle(tela, PRETO, (olho_x, olho_y), olho_raio, 0)

    def processar_eventos(self, eventos):
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT or e.key == pygame.K_d:
                    self.vel_x = VELOCIDADE
                    self.vel_y = 0
                    self.direcao = DIREITA

                elif e.key == pygame.K_LEFT or e.key == pygame.K_a:
                    self.vel_x = -VELOCIDADE
                    self.vel_y = 0
                    self.direcao = ESQUERDA

                elif e.key == pygame.K_UP or e.key == pygame.K_w:
                    self.vel_y = -VELOCIDADE
                    self.vel_x = 0
                    self.direcao = ACIMA

                elif e.key == pygame.K_DOWN or e.key == pygame.K_s:
                    self.vel_y = VELOCIDADE
                    self.vel_x = 0
                    self.direcao = ABAIXO

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao



