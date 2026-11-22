#==================================================
# GUI.SENSORS | Creacion de los objetos de los sensores
#==================================================
import math
import pygame

from config.config import load_config

class Sensor:
    '''
    Objeto → Sensor | Linea q mide distancia coche → pared
    '''
    def __init__(self, offset=0, max_distance=None):
        config = load_config()

        # == Parametros Bases ==
        self.offset = offset
        self.max_distance = max_distance or config["DISTANT_SENSOR"]
        self.distance = self.max_distance
        self.hit = False
        self.start = (0, 0)
        self.end = (0, 0)

    def measure(self, floor, x, y, angle):
        '''
        Lanza el rayo y guarda la distancia (en pixeles)
        '''
        # == Datos Suyos ==
        angle = math.radians(angle + self.offset - 90)
        dx = math.cos(angle)
        dy = -math.sin(angle)
        height, width = floor.shape
        self.distance = self.max_distance
        self.hit = False

        # == Marca por cada Rayo su Distancia ==
        self.distance = self.max_distance
        for d in range(self.max_distance):
            px = int(x + dx * d)
            py = int(y + dy * d)
            if px < 0 or px >= width or py < 0 or py >= height or floor[py, px]:
                self.distance = d
                self.hit = True
                break

        self.start = (x, y)
        self.end = (x + dx * self.distance, y + dy * self.distance)
        return self.distance

    def draw(self, surface):
        # == Las partes q chocan ==
        if self.hit:
            color = (255, 0, 0)
        # == Las partes q no chocan ==
        else:
            color = (0, 255, 0)

        pygame.draw.line(surface, color, self.start, self.end, 2)

        if self.hit:
            pygame.draw.circle(surface, color, (int(self.end[0]), int(self.end[1])), 4)