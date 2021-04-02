import pygame
import random
from abc import ABCMeta, abstractmethod
pygame.init()

screen = pygame.display.set_mode((800, 600), 0)
font = pygame.font.SysFont("arial", 24, True, False)
AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
ROSA = (255, 15, 192)
LARANJA = (255, 140, 0)
CIANO = (0, 255, 255)
VELOCIDADE = 1
ACIMA = "ACIMA"
ABAIXO = "ABAIXO"
DIREITA = "DIREITA"
ESQUERDA = "ESQUERDA"
PAUSADO = "PAUSADO"
JOGANDO = "JOGANDO"
GAMEOVER = "GAMEOVER"
VITORIA = "VITORIA"


class ElementoJogo(metaclass=ABCMeta):
    @abstractmethod
    def pintar(self, tela):
        pass

    @abstractmethod
    def calcular_regras(self):
        pass

    @abstractmethod
    def processar_eventos(self, eventos):
        pass


class ValidadorMovivel(metaclass=ABCMeta):
    @abstractmethod
    def adicionar_movivel(self, movivel):
        pass


class Movivel(metaclass=ABCMeta):
    @abstractmethod
    def aceitar_movimento(self):
        pass

    @abstractmethod
    def recusar_movimento(self, direcoes):
        pass

    @abstractmethod
    def mudar_direcao(self, direcoes):
        pass


class Cenario(ElementoJogo, ValidadorMovivel):
    def __init__(self, tamanho, pacman):
        self.pacman = pacman
        self.moviveis = []
        self.tamanho = tamanho
        # JOGANDO, PAUSADO, GAMEOVER, VITORIA
        self.estado = JOGANDO
        self.pontos = 0
        self.matriz = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]

    def adicionar_movivel(self, movivel):
        self.moviveis.append(movivel)

    def pintar_linha(self, tela, numero_linha, linha):
        for numero_coluna, coluna in enumerate(linha):
            x = numero_coluna * self.tamanho
            y = numero_linha * self.tamanho
            half = self.tamanho // 2
            cor = PRETO
            if coluna == 2:
                cor = AZUL
            pygame.draw.rect(tela, cor, (x, y, self.tamanho, self.tamanho), 0)
            if coluna == 1:
                pygame.draw.circle(tela, AMARELO, (x + half, y + half),
                                   self.tamanho // 10, 0)

    def pintar(self, tela):
        if self.estado == JOGANDO:
            self.pintar_jogando(tela)

        elif self.estado == PAUSADO:
            self.pintar_jogando(tela)
            self.pintar_pausado(tela)

        elif self.estado == GAMEOVER:
            self.pintar_jogando(tela)
            self.pintar_gameover(tela)

        elif self.estado == VITORIA:
            self.pintar_jogando(tela)
            self.pintar_vitoria(tela)

    @staticmethod
    def pintar_texto_centro(tela, texto):
        texto_img = font.render(texto, True, AMARELO)
        texto_x = (tela.get_width() - texto_img.get_width()) // 2
        texto_y = (tela.get_height() - texto_img.get_height()) // 2
        tela.blit(texto_img, (texto_x, texto_y))

    def pintar_gameover(self, tela):
        self.pintar_texto_centro(tela, "G A M E  O V E R")

    def pintar_pausado(self, tela):
        self.pintar_texto_centro(tela, "P A U S A D O")

    def pintar_vitoria(self, tela):
        self.pintar_texto_centro(tela, "P A R A B E N S  V O C E  V E N C E U ! ! !")

    def pintar_jogando(self, tela):
        for numero_linha, linha in enumerate(self.matriz):
            self.pintar_linha(tela, numero_linha, linha)
            self.pintar_pontos(tela)

    def pintar_pontos(self, tela):
        pontos_x = 30 * self.tamanho
        img_pontos = font.render("Score: {}".format(self.pontos), True, AMARELO)
        tela.blit(img_pontos, (pontos_x, 50))

    def calcular_regras(self):
        if self.estado == JOGANDO:
            self.calcular_regras_jogando()

        elif self.estado == PAUSADO:
            self.calcular_regras_pausado()

    def calcular_regras_vitoria(self):
        pass

    def calcular_regras_gameover(self):
        pass

    def calcular_regras_pausado(self):
        pass

    def calcular_regras_jogando(self):
        for movivel in self.moviveis:
            lin = int(movivel.linha)
            col = int(movivel.coluna)
            lin_intencao = int(movivel.linha_intencao)
            col_intencao = int(movivel.coluna_intencao)
            direcoes = self.get_direcoes(lin, col)
            exists_points = False

            if len(direcoes) >= 3:
                movivel.mudar_direcao(direcoes)

            if isinstance(movivel, Fantasma) and movivel.linha == self.pacman.linha \
                    and movivel.coluna == self.pacman.coluna:
                self.estado = GAMEOVER

            else:
                if 0 <= col_intencao <= 28 and 0 <= lin_intencao <= 29 and self.matriz[lin_intencao][col_intencao] != 2:
                    movivel.aceitar_movimento()
                    if isinstance(movivel, Pacman) and self.matriz[lin][col] == 1:
                        self.pontos += 1
                        self.matriz[lin][col] = 0

                        for lista in self.matriz:
                            if any(element == 1 for element in lista):
                                exists_points = True
                                break

                        if not exists_points:
                            self.estado = VITORIA
                else:
                    movivel.recusar_movimento(direcoes)

    def processar_eventos(self, eventos):
        for e in eventos:
            if e.type == pygame.QUIT:
                exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    self.estado = (PAUSADO if self.estado == JOGANDO else JOGANDO)

                if e.key == pygame.K_o:
                    self.estado = (GAMEOVER if self.estado == JOGANDO else JOGANDO)

    def get_direcoes(self, linha, coluna):
        direcoes = []
        if self.matriz[int(linha - 1)][int(coluna)] != 2:
            direcoes.append(ACIMA)

        if self.matriz[int(linha + 1)][int(coluna)] != 2:
            direcoes.append(ABAIXO)

        if self.matriz[int(linha)][int(coluna - 1)] != 2:
            direcoes.append(ESQUERDA)

        if self.matriz[int(linha)][int(coluna + 1)] != 2:
            direcoes.append(DIREITA)

        return direcoes


class Pacman(ElementoJogo, Movivel):
    def __init__(self, tamanho):
        self.coluna = 1
        self.linha = 1
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


class Fantasma(ElementoJogo, Movivel):
    def __init__(self, cor, tamanho):
        self.coluna = 14.0
        self.linha = 14.0
        self.coluna_intencao = self.coluna
        self.linha_intencao = self.linha
        self.velocidade = VELOCIDADE
        self.direcao = ACIMA
        self.cor = cor
        self.tamanho = tamanho

    def pintar(self, tela):
        fatia = self.tamanho // 8
        px = int(self.coluna * self.tamanho)
        py = int(self.linha * self.tamanho)
        contorno = [(px, py + self.tamanho),
                    (px + fatia, py + fatia * 2),
                    (px + fatia * 2, py + fatia // 2),
                    (px + fatia * 3, py),
                    (px + fatia * 5, py),
                    (px + fatia * 6, py + fatia // 2),
                    (px + fatia * 7, py + 2),
                    (px + self.tamanho, py + self.tamanho)]
        pygame.draw.polygon(tela, self.cor, contorno, 0)

        olho_raio_ext = fatia
        olho_raio_int = fatia // 2

        olho_e_x = int(px + fatia * 2.5)
        olho_e_y = int(py + fatia * 2.5)

        olho_d_x = int(px + fatia * 5.5)
        olho_d_y = int(py + fatia * 2.5)

        pygame.draw.circle(tela, BRANCO, (olho_e_x, olho_e_y), olho_raio_ext, 0)
        pygame.draw.circle(tela, PRETO, (olho_e_x, olho_e_y), olho_raio_int, 0)

        pygame.draw.circle(tela, BRANCO, (olho_d_x, olho_d_y), olho_raio_ext, 0)
        pygame.draw.circle(tela, PRETO, (olho_d_x, olho_d_y), olho_raio_int, 0)

    def calcular_regras(self):
        if self.direcao == ACIMA:
            self.linha_intencao -= self.velocidade
        elif self.direcao == ABAIXO:
            self.linha_intencao += self.velocidade
        elif self.direcao == ESQUERDA:
            self.coluna_intencao -= self.velocidade
        elif self.direcao == DIREITA:
            self.coluna_intencao += self.velocidade

    def mudar_direcao(self, direcoes):
        self.direcao = random.choice(direcoes)

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.mudar_direcao(direcoes)

    def processar_eventos(self, eventos):
        pass


if __name__ == "__main__":
    size = 600 // 30
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
        pygame.time.delay(100)

        # Captura os eventos
        eventos = pygame.event.get()
        cenario.processar_eventos(eventos)
        pacman.processar_eventos(eventos)
