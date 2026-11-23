#==================================================
# GUI.POSITION | Marca para seleccionar el inicio del cohete
#==================================================
import pygame

class Objetive:
    def __init__(self):
        self.c_init = (0, 255, 0)
        self.c_objetive = (255, 0, 0)

    def init(self, screen, line):
        pygame.draw.line(
                screen,
                self.c_init,
                (line, 0),
                (line, 600),
                2
            )