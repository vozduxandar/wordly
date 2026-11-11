"""Editable row: keyboard input and appearance before submitting a guess."""

import pygame

from beksultan import WordRow

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


class EditableRow(WordRow):
    def __init__(self, index):
        super().__init__(index)
        self.active = False

    def on_key(self, event):
        """Return True when Enter submits a complete five-letter word."""
        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            return self.is_complete()
        if event.key == pygame.K_BACKSPACE:
            self.word = self.word[:-1]
        elif pygame.K_a <= event.key <= pygame.K_z and len(self.word) < 5:
            self.word += ALPHABET[event.key - pygame.K_a]
        return False

    def is_complete(self):
        return len(self.word) == 5

    def color_at(self, column):
        """Override the base color to highlight typed letters and the active row."""
        if column < len(self.word):
            return (68, 70, 84)
        if self.active:
            return (65, 69, 88)
        return super().color_at(column)
