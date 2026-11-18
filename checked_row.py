"""Checked row: Wordly's green/yellow/gray scoring rules."""

import pygame

from word_row import WordRow

GREEN = (106, 170, 100)
YELLOW = (201, 180, 88)
GRAY = (120, 124, 126)
INK = (8, 9, 14)


class CheckedRow(WordRow):
    def __init__(self, index, word, secret):
        super().__init__(index, word)
        self.colors = self.grade(secret)
        self.revealed = 0
        self.last_switch = pygame.time.get_ticks()

    def grade(self, secret):
        """Consume exact matches first so repeated letters cannot score twice."""
        colors = [GRAY] * 5
        remaining = list(secret)
        for i, letter in enumerate(self.word):
            if letter == secret[i]:
                colors[i] = GREEN
                remaining[i] = None

        for i, letter in enumerate(self.word):
            if colors[i] != GREEN and letter in remaining:
                colors[i] = YELLOW
                remaining[remaining.index(letter)] = None
        return colors

    def color_at(self, column):
        return self.colors[column] if column < self.revealed else (68, 70, 84)

    def text_color_at(self, column):
        return INK if column < self.revealed else super().text_color_at(column)

    def update(self, now):
        if self.revealed < 5 and now - self.last_switch >= 120:
            steps = (now - self.last_switch) // 120
            self.revealed = min(5, self.revealed + steps)
            self.last_switch += steps * 120

    def is_correct(self):
        return all(color == GREEN for color in self.colors)
