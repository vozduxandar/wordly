"""Sprite for a five-letter row, rendered from original tile PNGs."""

from pathlib import Path

import pygame

WHITE = (255, 255, 255)
TILE_FILES = {
    "idle": "tile_idle.png",
    "active": "tile_active.png",
    "typed": "tile_typed.png",
    "correct": "tile_correct.png",
    "present": "tile_present.png",
    "absent": "tile_absent.png",
    "hover": "tile_hover.png",
}
COLOR_STYLES = {
    (58, 60, 72): "idle",
    (65, 69, 88): "active",
    (68, 70, 84): "typed",
    (106, 170, 100): "correct",
    (201, 180, 88): "present",
    (120, 124, 126): "absent",
}


class WordRow(pygame.sprite.Sprite):
    """Base sprite shared by the editable and checked rows."""

    _tile_images = None

    def __init__(self, index, word=""):
        super().__init__()
        self.index = index
        self.word = word
        self.image = pygame.Surface((245, 45), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(177, 47 + 50 * index))

    @classmethod
    def tile_images(cls):
        if WordRow._tile_images is None:
            assets = Path(__file__).resolve().parent / "assets"
            WordRow._tile_images = {
                style: pygame.image.load(str(assets / filename))
                for style, filename in TILE_FILES.items()
            }
        return WordRow._tile_images

    def tile_rect(self, column):
        return pygame.Rect(self.rect.x + 50 * column, self.rect.y, 45, 45)

    def color_at(self, column):
        """Child classes decide how to color each letter."""
        return (58, 60, 72)

    def text_color_at(self, column):
        return WHITE

    def render(self, font, hovered_column=None):
        tiles = self.tile_images()
        self.image.fill((0, 0, 0, 0))
        for column in range(5):
            rect = pygame.Rect(50 * column, 0, 45, 45)
            self.image.blit(tiles[COLOR_STYLES[self.color_at(column)]], rect)
            if column == hovered_column:
                self.image.blit(tiles["hover"], rect)
            if column < len(self.word):
                letter = font.render(self.word[column].upper(), True, self.text_color_at(column))
                self.image.blit(letter, letter.get_rect(center=rect.center))

    def draw(self, screen, font):
        self.render(font)
        screen.blit(self.image, self.rect)
