import pygame
import os
from random import choice


def load_image(name, color_key=(0, 255, 0, 255)):
    """
    :param name: image name if "data" directory
    :param color_key: clear color in image
    :return: image
    """
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if not color_key is None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
    image.set_colorkey(color_key)
    return image


class GameObject(pygame.sprite.Sprite):
    def __init__(self, g, HP, image_name, pos, speed=0, screen_size=(600, 600)):
        super().__init__(g)
        self.image = load_image(f'{image_name}.png')
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.HP, self.group = HP, g
        self.screen_size = screen_size
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = [0, 0]

    def die(self):
        # Some custom actions
        self.kill()

    def update(self, *args):
        if self.HP <= 0:
            self.die()
        self.move_on_vector()

    def move_on_vector(self):
        """Move object on vector"""
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]


class BG(pygame.sprite.Sprite):
    """Moving Background"""
    def __init__(self, g, image_name='bg1', top=True, screen_size=(600, 600)):
        super().__init__(g)
        self.image = load_image(f'{image_name}.png')
        self.rect = self.image.get_rect()
        self.rect.x = 0
        if top:
            self.rect.y = -self.rect.height
        else:
            self.rect.y = 0
        self.screen_size = screen_size
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        self.rect.y += 1
        if self.rect.y > self.screen_size[1]:
            self.rect.y = -self.rect.height


class Particle(pygame.sprite.Sprite):
    """Fulling Particles effect"""
    def __init__(self, group, pos, dx, dy, grav, screen_rect, image_name='star1.png'):
        self.fire = [load_image(image_name, -1)]
        for scale in (5, 10, 20):
            self.fire.append(pygame.transform.scale(self.fire[0], (scale, scale)))
        super().__init__(group)
        self.image = choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity, self.screen_rect = grav, screen_rect

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(self.screen_rect):
            self.kill()
