import pygame
import os

class SoundManager():
    def __init__(self) -> None:
        self.sounds = {}
        for sound in os.listdir(r"assets\sounds"):
            sound_name = sound.split(".")[0]
            self.add_sound(sound_name, f"assets\sounds\{sound_name}.wav", 0.1)

    def add_sound(self, name, path, volume):
        self.sounds[name] = pygame.mixer.Sound(path)
        self.sounds[name].set_volume(volume)

    def play_sound(self, name):
        self.sounds[name].play()