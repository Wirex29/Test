from os import path
import pygame as pg
from settings import *
vector = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        game_folder = path.dirname(__file__)
        asset_folder = path.join(game_folder, 'Assets')
        sprites_folder = path.join(asset_folder, 'Character sprites')
        self.images = [pg.image.load(path.join(sprites_folder, 'character_' + str(i) + '.png')).convert_alpha()
                       for i in range(2)]
        self.game = game
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.image = pg.transform.scale(self.image, [32, 32])
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        # self.dx, self.dy = None, None
        print("Drawn a player")

    def keys_signal(self):
        self.dx, self.dy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.dx = -P_SPEED
        elif keys[pg.K_w]:
            self.dy = -P_SPEED
        elif keys[pg.K_s]:
            self.dy = P_SPEED
        elif keys[pg.K_d]:
            self.current_image += 1
            self.dx = P_SPEED

    def wall_collision(self, dx=0, dy=0):
        pass
        # for wall in self.game.

    def update(self):
        self.keys_signal()
        self.x += self.dx * self.game.dt
        self.y += self.dy * self.game.dt
        self.rect.topleft = (self.x, self.y)
