"""Short-lived feedback particles for the end of a round."""

import random

import pygame


class Particle(pygame.sprite.Sprite):
    def __init__(self, center, color):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=center)
        self.dx = random.randint(-3, 3)
        self.dy = random.randint(-5, -2)
        self.life = 24

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.dy += 1
        self.life -= 1
        if self.life <= 0:
            self.kill()
