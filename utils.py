import pygame
from os.path import join


text_storage: dict[str, pygame.Surface] = {}


def fetch_texture(name: str, scale: tuple[float, float] = (1, 1)) -> pygame.Surface:
    if name not in text_storage:
        text_storage[name] = pygame.image.load(join("images", name)).convert()
        if scale != (1, 1):
            img_w, img_h = text_storage[name].get_size()
            text_storage[name] = pygame.transform.scale(text_storage[name], (int(img_w*scale[0]), int(img_h*scale[1])))
    return text_storage[name]
