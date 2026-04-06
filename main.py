import pygame
import time
import math
from game_info import GameInfo
from utils import scale_image, blit_rotate_center, blit_text_center

pygame.font.init()

# Carregar as imagens
GRASS = scale_image(pygame.image.load("assets/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("assets/track.png"), 0.9)

TRACK_BORDER = scale_image(pygame.image.load("assets/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load("assets/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (130, 250)

RED_CAR = scale_image(pygame.image.load("assets/red-car.png"), 0.55)
GREEN_CAR = scale_image(pygame.image.load("assets/green-car.png"), 0.55)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

MAIN_FONT = pygame.font.SysFont("Arial", 50)
# escolher a cor da fonte e o tamanho do texto a ser exibido na tela, utilizando a fonte Arial com tamanho 50

# Configurações do jogo
FPS = 60
# Caminho para o carro do computador seguir
PATH = [(175, 119), (110, 70), (56, 133), (70, 481), (318, 731), (404, 680), (418, 521), (507, 475), (600, 551), (613, 715), (736, 713),
        (734, 399), (611, 357), (409, 343), (433, 257), (697, 258), (738, 123), (581, 71), (303, 78), (275, 377), (176, 388), (178, 260)]


# Classe para representar um carro genérico, com funcionalidades comuns para o carro do jogador e o carro do computador
class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG # A imagem do carro é definida na classe filha (PlayerCar ou ComputerCar)
        self.max_vel = max_vel # A velocidade máxima do carro, definida no momento da criação do objeto
        self.vel = 0 # A velocidade atual do carro, inicialmente definida como 0
        self.rotation_vel = rotation_vel # A velocidade de rotação do carro, definida no momento da criação do objeto
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
# Função para rotacionar o carro para a esquerda ou para a direita, dependendo dos parâmetros passados
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
# Função para desenhar o carro na janela, utilizando a função blit_rotate_center para rotacionar a imagem do carro 
    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

# Classe para representar o carro do jogador, com funcionalidades específicas para o controle do jogador, 
# como reduzir a velocidade e rebater ao colidir com a borda da pista
class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (180, 200)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()

# Classe para representar o carro do computador, com funcionalidades específicas para seguir um caminho pré-definido,
class ComputerCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150, 200)

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)

    def draw(self, win):
        super().draw(win)
        # self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))
# Função para atualizar o ponto de destino do carro do computador, verificando se ele colidiu com o ponto atual e, 
# em caso afirmativo, avançando para o próximo ponto do caminho
    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(
            self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1
# Função para mover o carro do computador, calculando o ângulo necessário para seguir o caminho e atualizando o ponto de destino
    def move(self):
        if self.current_point >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()
        super().move()

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.2
        self.current_point = 0

# Função para desenhar os elementos do jogo na janela, incluindo o fundo, a pista, o ponto de chegada, 
# as informações do jogo e os carros do jogador e do computador
def draw(win, images, player_car, computer_car, game_info):
    for img, pos in images:
        win.blit(img, pos)

    level_text = MAIN_FONT.render(
        f"Level {game_info.level}", 1, (255, 255, 255))
    win.blit(level_text, (10, HEIGHT - level_text.get_height() - 70))

    time_text = MAIN_FONT.render(
        f"Time: {game_info.get_level_time()}s", 1, (255, 255, 255))
    win.blit(time_text, (10, HEIGHT - time_text.get_height() - 40))

    vel_text = MAIN_FONT.render(
        f"Vel: {round(player_car.vel, 1)}px/s", 1, (255, 255, 255))
    win.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 10))

    player_car.draw(win)
    computer_car.draw(win)
    pygame.display.update()

# Função para mover o carro do jogador, verificando as teclas pressionadas e chamando as funções de rotação e movimento correspondentes
def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]: # Se a tecla A estiver pressionada, o carro do jogador irá rotacionar para a esquerda
        player_car.rotate(left=True)
    if keys[pygame.K_d]: # Se a tecla D estiver pressionada, o carro do jogador irá rotacionar para a direita
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True # Se a tecla W estiver pressionada, o carro do jogador irá se mover para frente
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True # Se a tecla S estiver pressionada, o carro do jogador irá se mover para trás
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()

# Função para lidar com as colisões do carro do jogador e do carro do computador, 
# verificando se eles colidiram com a borda da pista ou com o ponto de chegada e reagindo de acordo
def handle_collision(player_car, computer_car, game_info):
    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()

    computer_finish_poi_collide = computer_car.collide(
        FINISH_MASK, *FINISH_POSITION)
    if computer_finish_poi_collide != None:
        blit_text_center(WIN, MAIN_FONT, "You lost!")
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()
        computer_car.reset()

    player_finish_poi_collide = player_car.collide(
        FINISH_MASK, *FINISH_POSITION)
    if player_finish_poi_collide != None:
        if player_finish_poi_collide[1] == 0:
            player_car.bounce()
        else:
            game_info.next_level()
            player_car.reset()
            computer_car.next_level(game_info.level)


run = True # Variável para controlar o loop principal do jogo, permitindo que ele continue rodando até que o jogador decida sair
clock = pygame.time.Clock() # Objeto para controlar o tempo do jogo, garantindo que ele rode a uma taxa de quadros constante (FPS)
images = [(GRASS, (0, 0)), (TRACK, (0, 0)),
          (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]
player_car = PlayerCar(4, 4) 
computer_car = ComputerCar(2, 4, PATH)
game_info = GameInfo()
# Loop principal do jogo, onde são processados os eventos, atualizados os estados dos objetos e desenhados os elementos na janela
while run:
    clock.tick(FPS)

    draw(WIN, images, player_car, computer_car, game_info)

    while not game_info.started:
        blit_text_center(
            WIN, MAIN_FONT, f"Press any key to start level {game_info.level}!")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

            if event.type == pygame.KEYDOWN:
                game_info.start_level()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    move_player(player_car)
    computer_car.move()

    handle_collision(player_car, computer_car, game_info)

    if game_info.game_finished():
        blit_text_center(WIN, MAIN_FONT, "You won the game!")
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()
        computer_car.reset()


pygame.quit()