import pygame
from ufo import Enemy

pygame.init()

BLACK = (0, 0, 0)
W, H = 600, 1024
fps = 70
clock = pygame.time.Clock()
screen = pygame.display.set_mode((W, H))

bg = pygame.image.load('content_game/Backgrounds/nebula600x1024.jpg').convert()

speed = 3


b1 = Enemy(W // 2, speed, 'content_game/PNG/Enemies/enemyGreen2.png')
b2 = Enemy(W // 2 - 250, 2, 'content_game/PNG/Enemies/enemyBlue1.png')
b3 = Enemy(W // 2 + 123, 4, 'content_game/PNG/Enemies/enemyRed2.png')
b4 = Enemy(W // 2 + 100, 7, 'content_game/PNG/Enemies/enemyBlack5.png')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    screen.blit(bg, (0, 0))
    screen.blit(b1.image, b1.rect)
    screen.blit(b2.image, b2.rect)
    screen.blit(b3.image, b3.rect)
    screen.blit(b4.image, b4.rect)




    pygame.display.update()
    clock.tick(fps)
    b1.update(H)
    b2.update(H)
    b3.update(H)
    b4.update(H)

