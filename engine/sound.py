import pygame
import os

class SoundManager:
    def __init__(self, game) -> None:
        self.game = game
        self.sounds = {}
        # Load all sound files from the assets/sounds directory
        for sound in os.listdir(r"assets\sounds"):
            sound_name = sound.split(".")[0]
            self.add_sound(sound_name, f"assets\sounds\{sound_name}.wav", 0.1)

    def add_sound(self, name, path, volume):
        self.sounds[name] = pygame.mixer.Sound(path)
        self.sounds[name].set_volume(volume)

    def play_sound(self, name):
        # Play a sound effect with volume from the game config
        self.sounds[name].set_volume(float(self.game.config.get("SOUND_VOLUME")))
        self.sounds[name].play()

    def play_music(self, name):
        # Play background music with volume from the game config
        pygame.mixer.music.set_volume(float(self.game.config.get("MUSIC_VOLUME")))
        pygame.mixer.music.load(f"assets\sounds\{name}.wav")
        pygame.mixer.music.play(-1)