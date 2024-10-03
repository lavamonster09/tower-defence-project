import pygame
from .screen_manager import *

class Engine:
     def __init__(self):
         self.display_surface = None
         self.screen_manager = ScreenManager()