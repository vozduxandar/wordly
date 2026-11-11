"""Wordly - 7-команда «ВОЗДУХ». Ойынды іске қосу."""
import pygame
from kyran import Game

WIDTH, HEIGHT = 600, 400


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Wordly — 7-команда ВОЗДУХ")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 26)
    game = Game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and game.over:
                game = Game()
            elif event.type == pygame.KEYDOWN:
                game.on_key(event)

        game.draw(screen, font)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
