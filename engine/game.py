import pygame
from .screen_manager import *



class Engine:
    def __init__(self):
        self.config = self.load_config()
        
        # setup the display
        self.screen = pygame.display.set_mode((self.config.get("SCREEN_WIDTH"), self.config.get("SCREEN_WIDTH")))
        self.screen_manager = ScreenManager()
        
    def load_config(self):
        config = {}
        with open("config.cfg") as fconfig:
            for line in fconfig.readlines():
                if line[0] != "#":
                    config[line.split(" ")[0]] = line.split(" ")[1]
        return config