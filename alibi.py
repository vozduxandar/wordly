import pygame

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


class InputDisplay:
    """Game класында қолданылатын басқару және сурет салу әдістері."""

    def on_key(self, event):
        if self.over:
            return
        if event.key == pygame.K_RETURN:
            self.submit()
        elif event.key == pygame.K_BACKSPACE:
            new = ""
            for i in range(len(self.current) - 1):
                new = new + self.current[i]
            self.current = new
        elif pygame.K_a <= event.key <= pygame.K_z:
            if len(self.current) < 5:
                self.current = self.current + ALPHABET[event.key - pygame.K_a]

    def draw(self, screen, font):
        screen.fill((15, 15, 35))

        if not self.over:
            for col in range(5):
                tile = self.board.tile(self.row, col)
                if col < len(self.current):
                    tile.letter = self.current[col]
                    tile.color = (68, 70, 84)
                else:
                    tile.letter = ""
                    tile.color = (58, 60, 72)

        self.board.draw(screen, font)

        title = font.render("Wordly: 5 әріптік сөзді тап", True, (255, 255, 255))
        screen.blit(title, (177, 320))
        hint = font.render(f"Әрекет {min(self.row + 1, 6)}/6. Enter — тексеру", True, (255, 255, 255))
        screen.blit(hint, (177, 352))

        if self.over:
            pygame.draw.rect(screen, (42, 45, 60), (90, 120, 420, 70))
            if self.won:
                message = "ЖЕҢІС! Жаңа ойын: R"
                color = (106, 170, 100)
            else:
                message = f"Ойын бітті. Сөз: {self.secret.upper()}. R — жаңа ойын"
                color = (201, 180, 88)
            msg = font.render(message, True, color)
            screen.blit(msg, (115, 145))
