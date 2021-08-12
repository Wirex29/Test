import os

import pygame.sprite


class Player(pygame.sprite.Sprite):
    """Create player"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(os.path.join('image', 'hero' + str(i) + '.png')).convert_alpha()
                       for i in range(6)]

        self.image = self.images[0]
        self.rect = self.image.get_rect()

