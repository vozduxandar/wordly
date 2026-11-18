"""Wordly: guess a five-letter word in six attempts. Run with python main.py."""

import os
import random
from pathlib import Path

import pygame

from checked_row import CheckedRow, GRAY, GREEN
from editable_row import EditableRow
from menu_word import MenuWord
from particle import Particle
from sound import Sound

WORDS = (
    "apple", "house", "table", "tiger", "robot", "plant", "cloud",
    "smile", "train", "brick", "snake", "ocean", "chair", "storm", "glass",
)
WIDTH, HEIGHT = 600, 400
BACKGROUND = (15, 15, 35)
PANEL = (42, 45, 60)
SECONDARY_BUTTON = (68, 70, 84)
WHITE = (255, 255, 255)
MUTED = (210, 215, 230)
INK = (8, 9, 14)
FONT_FILES = (
    ("Segoe UI", "segoeui.ttf", "segoeui"),
    ("Arial", "arial.ttf", "arial"),
    ("Calibri", "calibri.ttf", "calibri"),
)


def available_fonts():
    choices = []
    fonts_folder = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
    for label, filename, family in FONT_FILES:
        path = fonts_folder / filename
        if not path.is_file():
            match = pygame.font.match_font(family)
            if match is None:
                continue
            path = Path(match)
        font = pygame.font.Font(str(path), 24)
        if all(metric is not None for metric in font.metrics("ӘәҒғҚқҢңӨөҰұҮүІі")):
            choices.append((label, str(path)))
    return choices or [("Әдепкі", None)]


class Game:
    def __init__(self, secret=None, sound=None):
        self.sound = sound
        self.level = 1
        self.score = 0
        self.secret = secret if secret is not None else random.choice(WORDS)
        self.remaining_words = [word for word in WORDS if word != self.secret]
        self.font_choices = available_fonts()
        self.font_index = 0
        self.set_fonts()

        self.menu_word = MenuWord("ABCDE", (WIDTH // 2, 148), self.tile_font)
        self.menu_sprites = pygame.sprite.Group(self.menu_word)
        self.effects = pygame.sprite.Group()
        self.start_button = pygame.Rect(160, 215, 280, 46)
        self.font_button = pygame.Rect(110, 276, 180, 44)
        self.sound_button = pygame.Rect(310, 276, 180, 44)
        self.action_button = pygame.Rect(78, 235, 210, 46)
        self.menu_button = pygame.Rect(312, 235, 210, 46)
        self.focus = 0
        self.now = pygame.time.get_ticks()
        self.state = "start"
        self._reset_board()
        if self.sound:
            self.sound.start_music()

    def has_audio(self):
        return self.sound is not None and self.sound.available

    def can_change_font(self):
        return len(self.font_choices) > 1

    def set_fonts(self):
        path = self.font_choices[self.font_index][1]
        self.title_font = pygame.font.Font(path, 36)
        self.tile_font = pygame.font.Font(path, 28)
        self.text_font = pygame.font.Font(path, 23)
        self.small_font = pygame.font.Font(path, 18)

    def change_font(self, step=1):
        if not self.can_change_font():
            return
        self.font_index = (self.font_index + step) % len(self.font_choices)
        self.set_fonts()
        self.menu_word.set_font(self.tile_font)

    def _reset_board(self):
        self.rows = [EditableRow(index) for index in range(6)]
        self.row_sprites = pygame.sprite.Group(self.rows)
        self.rows[0].active = True
        self.row = 0
        self.round_score = 0
        self.over = False
        self.won = False
        self.revealing = False
        self.notice_until = 0
        self.effects.empty()

    def start(self):
        self._reset_board()
        self.state = "play"
        self.focus = 0
        if self.sound:
            self.sound.start_music()

    def next_round(self):
        if self.state != "over":
            return
        if self.won:
            self._advance_level()
        else:
            self._new_game()
        self.start()

    def _new_game(self):
        previous = self.secret
        self.secret = random.choice([word for word in WORDS if word != previous])
        self.remaining_words = [word for word in WORDS if word != self.secret]
        self.level = 1
        self.score = 0

    def _advance_level(self):
        previous = self.secret
        if not self.remaining_words:
            self.remaining_words = [word for word in WORDS if word != previous]
        self.secret = random.choice(self.remaining_words)
        self.remaining_words.remove(self.secret)
        self.level += 1

    def back_to_menu(self):
        if self.state == "over":
            if self.won:
                self._advance_level()
            else:
                self._new_game()
        self._reset_board()
        self.state = "start"
        self.focus = 0
        self.menu_word.restart()

    def _activate(self):
        if self.state == "start":
            if self.focus == 0:
                self.start()
            elif self.focus == 1 and self.can_change_font():
                self.change_font()
            elif self.focus == 2 and self.has_audio():
                self.sound.toggle()
        elif self.state == "over":
            if self.focus == 0:
                self.next_round()
            else:
                self.back_to_menu()

    def on_key(self, event):
        if event.key == pygame.K_F1:
            self.change_font()
            return False

        if self.state == "play":
            if event.key == pygame.K_ESCAPE:
                self.back_to_menu()
            elif not self.revealing:
                editable = self.rows[self.row]
                if editable.on_key(event):
                    checked = CheckedRow(self.row, editable.word, self.secret)
                    self.row_sprites.remove(editable)
                    self.rows[self.row] = checked
                    self.row_sprites.add(checked)
                    self.revealing = True
                    if self.sound:
                        self.sound.play("catch")
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self.notice_until = pygame.time.get_ticks() + 1000
                    if self.sound:
                        self.sound.play("hit")
            return False

        if event.key == pygame.K_TAB:
            step = -1 if event.mod & pygame.KMOD_SHIFT else 1
            if self.state == "start":
                choices = [0]
                if self.can_change_font():
                    choices.append(1)
                if self.has_audio():
                    choices.append(2)
            else:
                choices = [0, 1]
            self.focus = choices[(choices.index(self.focus) + step) % len(choices)]
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            self._activate()
        elif self.state == "start":
            if event.key == pygame.K_ESCAPE:
                return True
            if self.focus == 1 and self.can_change_font() and event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.change_font(-1 if event.key == pygame.K_LEFT else 1)
        elif self.state == "over":
            if event.key == pygame.K_r:
                self.next_round()
            elif event.key in (pygame.K_m, pygame.K_ESCAPE):
                self.back_to_menu()
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.focus = 1 - self.focus
        return False

    def hovered_tile(self, position):
        if self.state != "play" or self.revealing:
            return None
        editable = self.rows[self.row]
        pointer = pygame.Rect(position, (1, 1))
        for column in range(len(editable.word)):
            if pointer.colliderect(editable.tile_rect(column)):
                return column
        return None

    def on_click(self, position):
        if self.state == "start":
            if self.start_button.collidepoint(position):
                self.focus = 0
                self.start()
            elif self.font_button.collidepoint(position) and self.can_change_font():
                self.focus = 1
                self.change_font()
            elif self.sound_button.collidepoint(position) and self.has_audio():
                self.focus = 2
                self.sound.toggle()
        elif self.state == "play":
            column = self.hovered_tile(position)
            if column is not None:
                self.rows[self.row].erase_at(column)
        elif self.state == "over":
            if self.action_button.collidepoint(position):
                self.focus = 0
                self.next_round()
            elif self.menu_button.collidepoint(position):
                self.focus = 1
                self.back_to_menu()

    def update(self, now=None):
        self.now = pygame.time.get_ticks() if now is None else now
        if self.state == "start":
            self.menu_sprites.update(self.now)
        elif self.state == "play" and self.revealing:
            checked = self.rows[self.row]
            checked.update(self.now)
            if checked.revealed == 5:
                self.revealing = False
                if checked.is_correct() or self.row == 5:
                    self.won = checked.is_correct()
                    self.over = True
                    self.state = "over"
                    self.focus = 0
                    if self.won:
                        self.round_score = 6 - self.row
                        self.score += self.round_score
                    color = GREEN if self.won else GRAY
                    for column in range(5):
                        for _ in range(3):
                            self.effects.add(Particle(checked.tile_rect(column).center, color))
                    if not self.won and self.sound:
                        self.sound.play("over")
                else:
                    self.row += 1
                    self.rows[self.row].active = True
        self.effects.update()

    def _center(self, screen, text, y, font, color=WHITE):
        image = font.render(text, True, color)
        screen.blit(image, image.get_rect(center=(WIDTH // 2, y)))

    def _button(self, screen, rect, label, primary, focused, font=None, enabled=True):
        hovered = enabled and rect.collidepoint(pygame.mouse.get_pos())
        color = GREEN if primary else SECONDARY_BUTTON
        pygame.draw.rect(screen, color if enabled else PANEL, rect, border_radius=4)
        if enabled and not primary:
            pygame.draw.rect(screen, (144, 150, 170), rect, width=1, border_radius=4)
        if enabled and (focused or hovered):
            pygame.draw.rect(screen, WHITE, rect, width=2, border_radius=4)
        text_color = (INK if primary else WHITE) if enabled else MUTED
        image = (font or self.text_font).render(label, True, text_color)
        screen.blit(image, image.get_rect(center=rect.center))

    def draw(self, screen):
        screen.fill(BACKGROUND)
        if self.state == "start":
            self._center(screen, "Wordly", 52, self.title_font)
            self._center(screen, f"{self.level}-деңгей  ·  5 әріп, 6 әрекет", 92, self.small_font, MUTED)
            self.menu_sprites.draw(screen)
            self._center(screen, "Үлгі: 5 ұяшыққа 5 әріп", 190, self.small_font, MUTED)
            self._button(screen, self.start_button, "Ойынды бастау", True, self.focus == 0)
            self._button(
                screen, self.font_button,
                f"Қаріп: {self.font_choices[self.font_index][0]}", False, self.focus == 1,
                font=self.small_font, enabled=self.can_change_font(),
            )
            label = (
                "Дыбыс: қосулы" if self.sound.enabled else "Дыбыс: өшірулі"
            ) if self.has_audio() else "Дыбыс жоқ"
            self._button(
                screen, self.sound_button, label, False, self.focus == 2,
                font=self.small_font, enabled=self.has_audio(),
            )
            self._center(screen, "A-Z: жазу  ·  Backspace: өшіру  ·  Enter: тексеру", 349, self.small_font)
            self._center(screen, "Tab: таңдау  ·  F1: қаріп  ·  Esc: шығу", 377, self.small_font, MUTED)
            return

        self._center(screen, f"Wordly  ·  {self.level}-деңгей", 23, self.text_font)
        hovered = self.hovered_tile(pygame.mouse.get_pos())
        for row in self.rows:
            row.render(self.tile_font, hovered if row is self.rows[self.row] else None)
        self.row_sprites.draw(screen)
        self.effects.draw(screen)
        hint = (
            "5 әріп жазыңыз" if self.notice_until > self.now else
            "Ұяшықты бассаңыз, әріп өшеді" if hovered is not None else
            f"Әрекет {self.row + 1}/6  ·  Enter: тексеру  ·  F1: қаріп  ·  Esc: мәзір"
        )
        self._center(screen, hint, 373, self.small_font, MUTED)

        if self.state == "over":
            shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            shade.fill((0, 0, 0, 175))
            screen.blit(shade, (0, 0))
            pygame.draw.rect(screen, PANEL, (58, 94, 484, 221), border_radius=6)
            title = f"{self.level}-деңгей: Жеңіс!" if self.won else f"{self.level}-деңгей: Мүмкіндік бітті"
            self._center(screen, title, 128, self.text_font)
            word = "Табылған сөз" if self.won else "Жасырын сөз"
            self._center(screen, f"{word}: {self.secret.upper()}", 167, self.text_font)
            self._center(
                screen, f"Осы раунд: {self.round_score} ұпай  ·  Барлығы: {self.score}",
                205, self.small_font, MUTED,
            )
            self._button(
                screen, self.action_button,
                "Келесі деңгей" if self.won else "Жаңа ойын", True, self.focus == 0,
            )
            self._button(screen, self.menu_button, "Мәзір", False, self.focus == 1)
            self._center(screen, "R: жалғастыру  ·  M: мәзір  ·  F1: қаріп", 299, self.small_font, MUTED)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Wordly | 7-команда ВОЗДУХ")
    clock = pygame.time.Clock()
    game = Game(sound=Sound())
    running = True

    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and game.on_key(event):
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    game.on_click(event.pos)

            if not running:
                break
            game.update()
            game.draw(screen)
            pygame.display.flip()
            clock.tick(60)
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
