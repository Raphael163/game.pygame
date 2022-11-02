# import pygame sys
import pygame
from ufo import Enemy
import random

# SCREEM SET --> WIDTH --> HEIGHT --> FPS
WIDTH = 600
HEIGHT = 1024
FPS = 60

# SET GAME SETTINGS
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Звездный корабль")
clock = pygame.time.Clock()

# RGB COLOR
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# set controlling

x = WIDTH // 2
y = HEIGHT // 2
speed = 12




# back image Backgrounds
bg_image = pygame.image.load('content_game/Backgrounds/nebula600x1024.jpg').convert()
# image units
space_ship = pygame.image.load('content_game/PNG/playerShip3_blue.png')


# ENEMY
b1 = Enemy(WIDTH // 2, random.randrange(6, 20), 'content_game/PNG/Enemies/enemyGreen2.png')
b2 = Enemy(WIDTH // 2 - 250, random.randrange(3, 20), 'content_game/PNG/Enemies/enemyBlue1.png')
b3 = Enemy(WIDTH // 2 + 123, random.randrange(3, 25), 'content_game/PNG/Enemies/enemyRed2.png')
b4 = Enemy(WIDTH // 2 + 100, random.randrange(3, 40), 'content_game/PNG/Enemies/enemyBlack5.png')



# START
RUN_GAME_FLAG = True
while RUN_GAME_FLAG:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN_GAME_FLAG = False
            exit()

        # Отображение
    screen.blit(bg_image, (0, 0))
    space_ship_rect = space_ship.get_rect(center=(x, y))
    screen.blit(space_ship, space_ship_rect)

    # control game
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= speed

    elif keys[pygame.K_RIGHT]:
        x += speed

    if keys[pygame.K_UP]:
        y -= speed

    elif keys[pygame.K_DOWN]:
        y += speed

    clock.tick(FPS)



    screen.blit(b1.image, b1.rect)
    screen.blit(b2.image, b2.rect)
    screen.blit(b3.image, b3.rect)
    screen.blit(b4.image, b4.rect)



    pygame.display.update()
    clock.tick(FPS)
    b1.update(HEIGHT)
    b2.update(HEIGHT)
    b3.update(HEIGHT)
    b4.update(HEIGHT)
