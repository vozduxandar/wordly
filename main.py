"""Wordly: guess a five-letter word in six attempts. Run with python main.py."""

import random

import pygame

from alibi import EditableRow
from kyran import CheckedRow, GREEN, YELLOW

WORDS = (
    "apple", "house", "table", "tiger", "robot", "plant", "cloud",
    "smile", "train", "brick", "snake", "ocean", "chair", "storm", "glass",
)
WIDTH, HEIGHT = 600, 400


class Game:
    def __init__(self, secret=None):
        self.secret = secret if secret is not None else random.choice(WORDS)
        # CheckedRow and EditableRow share one collection and one draw loop.
        self.rows = [EditableRow(index) for index in range(6)]
        self.rows[0].active = True
        self.row = 0
        self.over = False
        self.won = False

    def on_key(self, event):
        if self.over:
            return
        editable = self.rows[self.row]
        if not editable.on_key(event):
            return

        checked = CheckedRow(self.row, editable.word, self.secret)
        self.rows[self.row] = checked
        if checked.is_correct():
            self.won = True
            self.over = True
        elif self.row == 5:
            self.over = True
        else:
            self.row += 1
            self.rows[self.row].active = True

    def draw(self, screen, font):
        screen.fill((15, 15, 35))
        for row in self.rows:
            row.draw(screen, font)

        title = font.render("Wordly: 5 әріптік сөзді тап", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 330)))
        hint = font.render(
            f"Әрекет {min(self.row + 1, 6)}/6  •  Enter — тексеру",
            True, (210, 215, 230),
        )
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 365)))

        if self.over:
            shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            shade.fill((0, 0, 0, 150))
            screen.blit(shade, (0, 0))
            pygame.draw.rect(screen, (42, 45, 60), (35, 125, 530, 120), border_radius=8)
            message = "ЖЕҢІС!" if self.won else f"Ойын бітті. Сөз: {self.secret.upper()}"
            color = GREEN if self.won else YELLOW
            text = font.render(message, True, color)
            screen.blit(text, text.get_rect(center=(WIDTH // 2, 165)))
            again = font.render("R — жаңа ойын", True, (255, 255, 255))
            screen.blit(again, again.get_rect(center=(WIDTH // 2, 205)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Wordly — 7-команда ВОЗДУХ")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("segoeui", 24)
    game = Game()
    running = True

    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and game.over:
                        game = Game()
                    else:
                        game.on_key(event)

            if not running:
                break
            game.draw(screen, font)
            pygame.display.flip()
            clock.tick(60)
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
