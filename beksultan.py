"""Common five-letter row: geometry and drawing of the game board."""

import pygame


class WordRow:
    """Base class shared by the editable and checked rows."""

    def __init__(self, index, word=""):
        self.index = index
        self.word = word

    def tile_rect(self, column):
        return pygame.Rect(177 + 50 * column, 15 + 50 * self.index, 45, 45)

    def color_at(self, column):
        """Child classes decide how to color each letter."""
        return (58, 60, 72)

    def draw(self, screen, font):
        for column in range(5):
            rect = self.tile_rect(column)
            pygame.draw.rect(screen, self.color_at(column), rect, border_radius=4)
            if column < len(self.word):
                letter = font.render(self.word[column].upper(), True, (255, 255, 255))
                screen.blit(letter, letter.get_rect(center=rect.center))
