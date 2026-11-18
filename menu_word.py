"""A five-tile sprite that demonstrates typing on the start screen."""

import pygame

from word_row import WordRow


class MenuWord(pygame.sprite.Sprite):
    def __init__(self, word, center, font):
        super().__init__()
        self.word = word
        self.frame = 0
        self.last_switch = pygame.time.get_ticks()
        self.set_font(font)
        self.rect = self.image.get_rect(center=center)

    def set_font(self, font):
        tiles = WordRow.tile_images()
        self.frames = []
        for count in range(6):
            image = pygame.Surface((245, 45), pygame.SRCALPHA)
            for i, letter in enumerate(self.word):
                rect = pygame.Rect(i * 50, 0, 45, 45)
                image.blit(tiles["typed" if i < count else "idle"], rect)
                if i < count:
                    glyph = font.render(letter, True, (255, 255, 255))
                    image.blit(glyph, glyph.get_rect(center=rect.center))
            self.frames.append(image)
        self.image = self.frames[self.frame]

    def restart(self):
        self.frame = 0
        self.image = self.frames[0]
        self.last_switch = pygame.time.get_ticks()

    def update(self, now):
        if self.frame < 5 and now - self.last_switch >= 170:
            steps = (now - self.last_switch) // 170
            self.frame = min(5, self.frame + steps)
            self.image = self.frames[self.frame]
            self.last_switch += steps * 170
