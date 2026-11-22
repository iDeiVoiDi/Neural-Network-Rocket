#==================================================
# GUI.MAP LOADER | Carga el mapa con numpy
#==================================================
from pathlib import Path
import numpy as np
import pygame

def load_floor(image_path, size, threshold=40):
    '''
    Carga los muros en un array de np
    '''
    image_path = Path(image_path)
    cache_path = image_path.with_suffix(".npy")

    # == Carga la cache cargada ==
    if cache_path.exists() and cache_path.stat().st_mtime >= image_path.stat().st_mtime:
        floor = np.load(cache_path)
        if floor.shape == (size[1], size[0]):
            return floor

    # == Crea el array de booleanos de si es muro ==
    surface = pygame.image.load(image_path).convert()
    surface = pygame.transform.scale(surface, size)
    rgb = pygame.surfarray.array3d(surface)
    floor = (rgb.sum(axis=2) < threshold).T      # Detecta lo negro, lo usaremos como suelo
    np.save(cache_path, floor)
    return floor