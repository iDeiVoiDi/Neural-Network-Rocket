#==================================================
# GUI.UI | Orquestador principal de la ventana
#==================================================
import pygame
from pathlib import Path

from config.config import load_config
from GUI.rocket import Rocket


class Game:
    def __init__(self):
        config = load_config()

        # == Parametros base ==
        pygame.init()
        pygame.display.set_caption(config["NAME"])
        width = config["SCREEN_WIDTH"]
        height = config["SCREEN_HEIGHT"]
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()  
        self.ticks = 60

        self.exit = False

    def run(self):
        ''''
        Corre la ventana principal del simulador
        '''
        config = load_config()
        map_path = Path(__file__).resolve().parent.parent / "assets" / "map.png"
        size = (config["SCREEN_WIDTH"], config["SCREEN_HEIGHT"])
        rocket = Rocket(10, 10)
        map_surface = pygame.transform.scale(pygame.image.load(map_path).convert(), size=size)
        mapa = pygame.mask.from_surface(map_surface) 
        while not self.exit:
            dt = self.clock.get_time() / 1000.0 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
            
            self.screen.blit(map_surface, (0, 0))

            
            
            rocket.update(dt)

            self.screen.blit(map_surface, (0, 0))
            rocket.draw(self.screen)
            
            
            pygame.display.flip()
            self.clock.tick(self.ticks)

        pygame.quit()


"""
threshold=40
surface = pygame.image.load(image_path).convert()
surface = pygame.transform.scale(surface, size)
rgb = pygame.surfarray.array3d(surface)
walls = (rgb.sum(axis=2) > threshold).T
np.save(cache_path, walls)"""

