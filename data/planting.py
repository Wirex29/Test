import pygame as pg
from data.spritesheet import Spritesheet
from data.settings import *


class Soil:
    data = []

    def __init__(self, game, x, y, w, h):
        self.game = game
        # self.groups = game.soils
        # pg.sprite.Sprite.__init__(self, self.groups)
        self.spritesheet = Spritesheet(path.join(map_folder, 'soils.png'))
        self.potato_images = [self.spritesheet.parse_sprite('soil_potato' + str(i) + '.png') for i in range(0, 5)]
        self.tomato_images = [self.spritesheet.parse_sprite('soil_tomato' + str(i) + '.png') for i in range(0, 5)]

        self.x = x
        self.y = y
        self.rect = pg.Rect(x, y, w, h)
        self.rect.x = x
        self.rect.y = y
        self.is_plowed = False
        self.is_seeded = False
        self.crop_type = None
        self.harvestable = False
        self.image = self.spritesheet.parse_sprite('tilled_soil.png')
        self.growth_stage = 0
        self.index = 0
        self.planted_date = 0

    def render(self, screen):
        if self.is_plowed:
            screen.blit(self.image, self.rect)

    def growing(self, days):
        if days != self.planted_date:
            # For every 4 days passed since planted date, the crop stage will grow by 1
            if (days - self.planted_date) // (4 + self.index) and self.growth_stage < 4:
                self.growth_stage += 1
                self.index += 4
            if self.growth_stage == 4:
                self.harvestable = True

    def update(self, days, screen):
        self.growing(days)
        if self.is_seeded:
            if self.crop_type == 2:
                self.image = self.potato_images[self.growth_stage]
            elif self.crop_type == 1:
                self.image = self.tomato_images[self.growth_stage]
        else:
            self.image = self.spritesheet.parse_sprite('tilled_soil.png')
        self.render(screen)

    def get_crop_id(self):
        return self.crop_type
