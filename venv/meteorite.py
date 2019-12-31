import pygame
import random
import os

# Константы
WIDTH = 600
HEIGHT = 720
FPS = 30


# Класс для игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.health = 100
        self.lives = 5

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
        self.image = random.choice(meteorite_images)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 7)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


def print_text(canvas, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    canvas.blit(text_surface, text_rect)


def draw_lives(canvas, x, y, lives, img):
    rect = pygame.Rect((x, y - 5, 30 * lives, 35))
    pygame.draw.rect(canvas, (127, 255, 212), rect)
    for i in range(lives):
        img_rect = img.get_rect()
        img.set_colorkey((0, 0, 0))
        img_rect.x = x + 30 * i + 2
        img_rect.y = y
        canvas.blit(img, img_rect)


def draw_health_bar(canvas, x, y, health):
    if health < 0:
        health = 0
    fill = health / 100 * 100
    outline_rect = pygame.Rect(x, y, 100, 15)
    fill_rect = pygame.Rect(x, y, fill, 15)
    pygame.draw.rect(canvas, (255, 165, 0), fill_rect)
    pygame.draw.rect(canvas, (255, 255, 255), outline_rect, 2)


img_dir = os.path.join(os.path.dirname(__file__), 'images')
font_name = pygame.font.match_font('arial')
# Создаем окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Метеоритная атака")
#os.environ['Sp_VIDEO_WINDOW_POS'] = "10, 200"
clock = pygame.time.Clock()
# Зугружаем картинки
background = pygame.image.load(os.path.join(img_dir, "space.png")).convert()
background_rect = background.get_rect()
# Космический истребитель
player_img = pygame.image.load(os.path.join(img_dir, "ship.png")).convert()
# Метеориты
meteorite_images = []
for i in '12345':
    meteorite_images.append(pygame.image.load(os.path.join(img_dir,
                                                           "meteorite0" + i + ".png")).convert())
# Выстрел (ракета)
rocket_img = pygame.image.load(os.path.join(img_dir, "rocket.png")).convert()
# Жизнь
live_img = pygame.image.load(os.path.join(img_dir, "ship_mini.png")).convert()
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
rating = 0
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
        rating += 50 - hit.radius
        meteorite = Meteorite()
        all_sprites.add(meteorite)
        meteorites.add(meteorite)
    # Проверка столкновения метеоритов и игрока
    hits = pygame.sprite.spritecollide(player, meteorites, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.health -= hit.radius * 2
        print(player.health, player.lives)
        meteorite = Meteorite()
        all_sprites.add(meteorite)
        meteorites.add(meteorite)
        if player.health <= 0:
            player.lives -= 1
            player.health = 100
    # Если игрок умер
    if player.lives == 0:
        running = False
    screen.fill((0, 0, 0))
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    print_text(screen, str(rating), 18, WIDTH / 2, 10)
    draw_lives(screen, WIDTH - 150, 5, player.lives, live_img)
    draw_health_bar(screen, 5, 5, player.health)
    if rating <= 1000:
        pass
    elif 1000 < rating <= 8000:
        FPS = (rating + 2000) // 100
    else:
        FPS = 100
    pygame.display.flip()
pygame.quit()
