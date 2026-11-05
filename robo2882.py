# bots/shadow_hunter.py - Robô Ofensivo
import math
import random
from core.pybot_base import Pybot

class EstrelaHunter(Pybot):
    def __init__(self, nome, cor="orange"):
        super().__init__(nome, cor)
        self.alvo_atual = None
        self.estrategia_atual = "cacador"
        self.contador_exploracao = 0

    def on_turno(self):
        if not self.vivo:
            return

        inimigos = self.escanear()

        if inimigos:
            self.estrategia_atual = "ataque"

            # Prioriza inimigos com menor energia
            self.alvo_atual = min(
                inimigos,
                key=lambda x: x.get('energia', 50000)
            )

            dx = self.alvo_atual['pos_x'] - self.pos_x
            dy = self.alvo_atual['pos_y'] - self.pos_y

            angulo = math.degrees(math.atan2(dy, dx))
            diferenca = (angulo - self.direcao + 180) % 360 - 180

            # Mira mais agressiva
            if abs(diferenca) > 5:
                self.virar(diferenca * 0.8)
            else:
                self.atirar(angulo)

            # Distâncias de combate
            distancia = self.alvo_atual['distancia']

            if distancia < 180:
                self.mover_para_frente(-14)
            elif distancia > 350:
                self.mover_para_frente(16)
            else:
                self.mover_para_frente(3)

        else:
            self.estrategia_atual = "exploracao"
            self.contador_exploracao += 1

            if self.contador_exploracao % 10 == 0:
                self.virar(random.randint(-90, 90))
            else:
                self.mover_para_frente(13)

        # Gerenciamento do campo de força
        if (self.energia < 2500
                and not self.campo_forca_ativo
                and self.cooldown_campo_forca == 0):
            self.ativar_campo_forca()

        elif self.energia > 6000 and self.campo_forca_ativo:
            self.desativar_campo_forca()
