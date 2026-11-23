#==================================================
# GUI.ROCKET | Creacion del objeto de cohete
#==================================================
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
        self.velocity = Vector2(0, 0)
        self.angle = angle
        self.state = "start"

        # == Parametros Editables ==
        self.max_speed = config["ROCKET_MAX_SPEED"]
        self.acceleration = config["ROCKET_ACELERATION"]
        self.gravity = config["ROCKET_GRAVITY"]
        self.turn_rate = config["ROCKET_TURN_RATE"]
        self.velocity_crash = config["ROCKET_VELOCITY_CRASH"]

        # == Carga Imagen ==
        self.original_image = pygame.image.load(image_path).convert_alpha()

        # == Reescalado Imagen ==
        self.width = config["WIDTH_ROCKET"]
        self.height = config["HEIGHT_ROCKET"]
        self.image = pygame.transform.scale(self.original_image, (int(self.width), int(self.height)))


    def update(self, floor, dt):
        '''
        Actualizacion de las fisicas
        '''
        keys = pygame.key.get_pressed()

        if self.state == "start" and keys[pygame.K_UP]:
            self.state = "flying"

        if self.state != "flying":
            return

        # == Giro ==
        if keys[pygame.K_LEFT]:
            self.angle += self.turn_rate * dt
        if keys[pygame.K_RIGHT]:
            self.angle += -self.turn_rate * dt

        # == Gravedad ==
        self.velocity.y += self.gravity * dt

        # == Motor ==
        if keys[pygame.K_UP]:
            direction = Vector2(0, -1).rotate(-self.angle)
            self.velocity += direction * self.acceleration * dt

        # == Tope ==
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        # == Mover ==
        old_position = Vector2(self.position)
        self.position += self.velocity * dt

        # == Contacto con el suelo ==
        if self.touches_floor(floor):
            self.position = old_position
            # Velocidad de choque
            speed = self.velocity.length()
            # Angulo vertical
            tilt = abs((self.angle + 180) % 360 - 180)

            if speed < self.velocity_crash and tilt < 15:
                self.state = "landed"
            else:
                self.state = "crashed"

            self.velocity = Vector2(0, 0)

        
    def get_corners(self, ppu=32):
        '''
        Saca las esquinas para su Hitbox
        '''
        hw, hh = self.width / 2, self.height / 2
        local = [Vector2(-hw, -hh), Vector2(hw, -hh), Vector2(hw, hh), Vector2(-hw, hh)]
        center = self.position * ppu

        return [center + c.rotate(-self.angle) for c in local]


    def touches_floor(self, floor, ppu=32):
        '''
        Comprueba si toco suelo mirando el array de numpy
        '''
        h, w = floor.shape
        for p in self.get_corners(ppu):
            x, y = int(p.x), int(p.y)
            if 0 <= x < w and 0 <= y < h and floor[y, x]:
                return True
        return False


    def draw(self, surface, ppu=32):
        '''
        Dibujado en pantalla
        '''
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        pixel_pos = self.position * ppu
        rect = rotated_image.get_rect(center=pixel_pos)
        
        surface.blit(rotated_image, rect.topleft)
