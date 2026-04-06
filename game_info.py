# Classe para armazenar informações do jogo, como nível atual, tempo de início do nível, etc.
from time import time


class GameInfo:
    LEVELS = 10 # Número total de níveis no jogo

    def __init__(self, level=1): # nível inicial do jogo, por padrão é 1
        self.level = level
        self.started = False
        self.level_start_time = 0

    def next_level(self): # Avançar para o próximo nível, incrementando o número do nível e resetando o estado de início do nível
        self.level += 1
        self.started = False

    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    def game_finished(self):
        return self.level > self.LEVELS

    def start_level(self): # Iniciar o nível, definindo o estado de início como True e registrando o tempo de início do nível
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self): # Obter o tempo decorrido desde o início do nível, retornando 0 se o nível ainda não tiver sido iniciado
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)