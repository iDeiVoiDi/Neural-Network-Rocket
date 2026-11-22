import pygame
from pygame.math import Vector2
from pathlib import Path

from config.config import load_config

class Rocket:
    '''
    OBJETO → Cohete | Objeto principal con sus fisicas
    '''
    def __init__(self, x, y, angle=0, image_path: str = Path(__file__).resolve().parent.parent / "assets" / "rocket.png"):
        config = load_config()

        # == Parametros Bases ==
        self.position = Vector2(x, y)       
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.vel_grav = 0.0
        self.angle = angle

        # == Parametros Editables ==
        self.max_speed = config["ROCKET_MAX_SPEED"]
        self.acceleration = config["ROCKET_ACELERATION"]
        self.gravity = config["ROCKET_GRAVITY"]
        self.turn_rate = config["ROCKET_TURN_RATE"]

        # == Carga Imagen ==
        self.original_image = pygame.image.load(image_path).convert_alpha()

        # == Reescalado Imagen ==
        self.width = config["WIDTH_ROCKET"]
        self.height = config["HEIGHT_ROCKET"]
        self.image = pygame.transform.scale(self.original_image, (int(self.width), int(self.height)))

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: # Si se presiona la flecha izquierda el ángulo disminuye.
            self.angle += self.turn_rate * dt 
        if keys[pygame.K_RIGHT]: # Si se presiona la flecha derecha el ángulo aumenta.
            self.angle += -self.turn_rate * dt

        if keys[pygame.K_UP]:
            pass




        
 
        
        direction = Vector2(0, -1).rotate(-self.angle)  # El vector (y) va en negativo porque si xd.
        #self.position.y += None
        print(self.velocity_y)
        

    def draw(self, surface, ppu=32):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        pixel_pos = self.position * ppu
        rect = rotated_image.get_rect(center=pixel_pos)
        
        surface.blit(rotated_image, rect.topleft)
