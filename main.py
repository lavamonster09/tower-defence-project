# To do 
# waves 

from misc.constants import * 
from screens.screen_manager import ScreenManager
import pygame 
import sys

pygame.init()


class App:
    def __init__(self) -> None:
        self.display_width , self.display_height = SCREEN_WIDTH, SCREEN_HEIGHT
        self.display = pygame.display.set_mode((self.display_width, self.display_height))
        self.screen_manager = ScreenManager(self)
        self.clock = pygame.time.Clock()
        self.main()
        
    def main(self):
        while True:
            self.check_events()
            self.display.fill((0,0,0))
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
            if event.type == RESOLUTION_UPDATE:
                self.display_width, self.display_height = event.resolution
                self.display = pygame.display.set_mode((self.display_width, self.display_height))
    
    def update(self):
        self.screen_manager.update()

    def draw(self):
        self.screen_manager.draw()

if __name__ == "__main__":
    app = App()
