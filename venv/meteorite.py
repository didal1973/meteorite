import pygame
import random
from os import path

# Константы
WIDTH = 600
HEIGHT = 720
FPS = 60


# Класс для игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.centerx = WIDTH /    2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -4
        if keystate[pygame.K_DOWN]:
            self.speedy = 4
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        rocket = Rocket(self.rect.centerx, self.rect.top)
        all_sprites.add(rocket)
        rockets.add(rocket)


# Класс выстрела (ракета)
class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = rocket_img
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # Выход за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()


# Класс для метеорита
class Meteorite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = meteorite_img
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


img_dir = path.join(path.dirname(__file__), 'images')
# Создаем окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Метеоритная атака")
clock = pygame.time.Clock()
# Зугружаем картинки
background = pygame.image.load(path.join(img_dir, "space.png")).convert()
background_rect = background.get_rect()
# Космический истребитель
player_img = pygame.image.load(path.join(img_dir, "ship.png")).convert()
# Метеорит
meteorite_img = pygame.image.load(path.join(img_dir, "meteorite.png")).convert()
# Выстрел (ракета)
rocket_img = pygame.image.load(path.join(img_dir, "rocket.png")).convert()
#
all_sprites = pygame.sprite.Group()
meteorites = pygame.sprite.Group()
rockets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(9):
    meteorite = Meteorite()
    all_sprites.add(meteorite)
    meteorites.add(meteorite)
# Игровой цикл
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    # Обновление
    all_sprites.update()
    # Проверка попадания ракеты
    hits = pygame.sprite.groupcollide(meteorites, rockets, True, True)
    for hit in hits:
        meteorite = Meteorite()
        all_sprites.add(meteorite)
        meteorites.add(meteorite)
    # Проверка столкновения метеоритов и игрока
    hits = pygame.sprite.spritecollide(player, meteorites, False, pygame.sprite.collide_circle)
    if hits:
        running = False
    screen.fill((0, 0, 0))
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
