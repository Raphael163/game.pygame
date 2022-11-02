import pygame
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, speed, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = speed

    def update(self, *args):
        if self.rect.y < args[0] - 20:
            self.rect.y += self.speed
        else:
            self.rect.y = 0





# class Mob(pygame.sprite.Sprite):
#     def __init__(self):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.Surface((30, 40))
#         self.image.fill(RED)
#         self.rect = self.image.get_rect()
#         self.rect.x = random.randrange(WIDTH - self.rect.width)
#         self.rect.y = random.randrange(-100, -40)
#         self.speedy = random.randrange(1, 8)
#
#     def update(self):
#         self.rect.y += self.speedy
#
#         if self.rect.top > HEIGHT + 10:
#             self.rect.x = random.randrange(WIDTH - self.rect.width)
#             self.rect.y = random.randrange(-100, -40)
#             self.speedy = random.randrange(1, 8)