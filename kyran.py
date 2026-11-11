"""Checked row: Wordly's green/yellow/gray scoring rules."""

from beksultan import WordRow

GREEN = (106, 170, 100)
YELLOW = (201, 180, 88)
GRAY = (120, 124, 126)


class CheckedRow(WordRow):
    def __init__(self, index, word, secret):
        super().__init__(index, word)
        self.colors = self.grade(secret)

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
        return self.colors[column]

    def is_correct(self):
        return all(color == GREEN for color in self.colors)
