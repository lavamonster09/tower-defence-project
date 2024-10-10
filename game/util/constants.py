import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
RESOLUTION_UPDATE = pygame.USEREVENT + 1 

PATH_SIZE = 24
MIN_OBSTICLE_SIZE, MAX_OBSTICLE_SIZE = 35, 150
SCREEN_SCALE = 1

# dont know why this has to be here but it does so dont touch 
def in_range(item, range):
    return range[0] <= item <= range[1]