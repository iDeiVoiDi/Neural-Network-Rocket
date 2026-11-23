#==================================================
# GUI.UI | Orquestador principal de la ventana
#==================================================
import pygame
from pathlib import Path

from config.config import load_config

from GUI.rocket import Rocket
from GUI.sensors import Sensor
from GUI.position import Objetive
from GUI.map_loader import load_floor


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
        ppu = 32

        map_path = Path(__file__).resolve().parent.parent / "assets" / "map.png"
        size = (config["SCREEN_WIDTH"], config["SCREEN_HEIGHT"])

        # == Cohete ==
        rocket = Rocket(10, 10)

        # == Sensores ==
        sensors = [Sensor(offset) for offset in (-60, -30, 0, 30, 60, 180)]

        # == Puntero ==
        objetive = Objetive()

        # == Carga del suelo ==
        floor = load_floor(map_path, size)

        # == Carga del mapa ==
        map_surface = pygame.transform.scale(pygame.image.load(map_path).convert(), size=size)

        while not self.exit:
            dt = self.clock.get_time() / 1000.0 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        line_x = event.pos[0]
                        objetive.init(map_surface, line_x)
                
            
            self.screen.blit(map_surface, (0, 0))

            rocket.update(floor, dt)

            rocket_px = rocket.position * ppu
            for s in sensors:
                s.measure(floor, rocket_px.x, rocket_px.y, rocket.angle)

            self.screen.blit(map_surface, (0, 0))

            for s in sensors:
                s.draw(self.screen)
            rocket.draw(self.screen)
            
            
            pygame.display.flip()
            self.clock.tick(self.ticks)

            if rocket.state != "flying":
                print(rocket.state)


        pygame.quit()


