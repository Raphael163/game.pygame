# Ready base template
"""
import pygame
import random

# SCREEM SET --> WIDTH --> HEIGHT --> FPS
WIDTH = 800
HEIGHT = 600
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

# START
RUN_GAME_FLAG = True
while RUN_GAME_FLAG:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN_GAME_FLAG = False

    screen.fill(GREEN)
    pygame.display.flip()
"""
