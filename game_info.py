import time
# Classe para armazenar informações do jogo, como nível atual, tempo de início do nível, etc.
class GameInfo:
    LEVELS = 10 # Número total de níveis no jogo

    def __init__(self, level=1): # nível inicial do jogo, por padrão é 1
        self.level = level
        self.started = False
        self.level_start_time = 0

    def next_level(self): # Avançar para o próximo nível
        self.level += 1
        self.started = False
# Reiniciar o jogo, voltando para o nível 1 e resetando as variáveis de controle
    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0
# Verificar se o jogo foi concluído, ou seja, se o nível atual é maior que o número total de níveis
    def game_finished(self):
        return self.level > self.LEVELS
# Iniciar o nível atual, registrando o tempo de início
    def start_level(self):
        self.started = True
        self.level_start_time = time.time()
# Retorna o tempo decorrido desde o início do nível atual, ou 0 se o nível ainda não começou
    def get_level_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)