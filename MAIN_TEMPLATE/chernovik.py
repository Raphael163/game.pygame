# ЧЕРНОВИК
import pygame

# SCREEM SET --> WIDTH --> HEIGHT --> FPS
WIDTH = 1150
HEIGHT = 1100
FPS = 60

# SET GAME SETTINGS
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('GAME')
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
speed = 50

# START
RUN_GAME_FLAG = True

while RUN_GAME_FLAG:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN_GAME_FLAG = False
            exit()
        # control game
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= speed
            elif event.key == pygame.K_RIGHT:
                x += speed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                y -= speed
            elif event.key == pygame.K_DOWN:
                y += speed

    screen.fill(BLACK)
    pygame.draw.rect(screen, GREEN, (x, y, 80, 80))
    pygame.display.flip()


# мышь

if event.type == pygame.MOUSEBUTTONDOWN:
    print('Mouse 1 ', event.button)
elif event.type == pygame.MOUSEMOTION:
    print('poz mouse', event.rel)



# ЧЕРНОВИК
import pygame

# SCREEM SET --> WIDTH --> HEIGHT --> FPS
WIDTH = 1150
HEIGHT = 1100
FPS = 60

# SET GAME SETTINGS
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('GAME')
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
speed = 50

# START
RUN_GAME_FLAG = True

while RUN_GAME_FLAG:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN_GAME_FLAG = False
            exit()
            # join image
            bg_image = pygame.image.load('content_game/Backgrounds/back_img.jpg')
            space_ship = pygame.image.load('content_game/PNG/playerShip3_blue.png')
            space_ship_rect = space_ship.get_rect(center=(x, y))

            screen.blit(bg_image, (0, 0))
            screen.blit(space_ship, space_ship_rect)

        # control game
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= speed
            elif event.key == pygame.K_RIGHT:
                x += speed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                y -= speed
            elif event.key == pygame.K_DOWN:
                y += speed

    screen.fill(BLACK)
    pygame.draw.rect(screen, GREEN, (x, y, 80, 80))
    pygame.display.flip()




