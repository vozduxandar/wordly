"""Play the original Wordly soundtrack and short synthesized effects."""

from pathlib import Path

import pygame

ASSETS = Path(__file__).resolve().parent / "assets"


class Sound:
    def __init__(self):
        self.effects = {}
        self.music_available = False
        self.available = bool(pygame.mixer.get_init())
        self.enabled = True
        if not self.available:
            return
        for name, filename in (
            ("catch", "effect_submit.wav"),
            ("hit", "effect_invalid.wav"),
            ("over", "effect_end.wav"),
        ):
            self.effects[name] = pygame.mixer.Sound(str(ASSETS / filename))

        path = ASSETS / "music_original.wav"
        try:
            pygame.mixer.music.load(str(path))
        except (pygame.error, OSError) as error:
            print(f"Could not load {path}: {error}")
        else:
            self.music_available = True

    def play(self, name):
        if self.enabled and name in self.effects:
            return self.effects[name].play()

    def start_music(self):
        if self.enabled and self.music_available and not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

    def stop_music(self):
        if self.music_available:
            pygame.mixer.music.stop()

    def toggle(self):
        if not self.available:
            return
        self.enabled = not self.enabled
        if self.enabled:
            self.start_music()
        else:
            self.stop_music()
            pygame.mixer.stop()
