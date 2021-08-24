import pygame.image
from spritesheet import Spritesheet
from settings import *


class Crop:
    crop_list = []

    def __init__(self, days, game):
        self.days = days
        self.growth_stage = 0
        self.growth_time = 0

    def update(self, days, screen):
        if self.growth_time == 4:
            self.growth_stage += 1


class Tomato(Crop):
    def __init__(self, x, y, days, game):
        super(Tomato, self).__init__(days, game)
        self.item_id = 1
        # Load tomato's spritesheet
        self.tomato_spritesheet = Spritesheet(path.join(map_folder, 'crops.png'))
        self.crop_tomato = [self.tomato_spritesheet.parse_sprite('crop_tomato0.png'),
                            self.tomato_spritesheet.parse_sprite('crop_tomato1.png'),
                            self.tomato_spritesheet.parse_sprite('crop_tomato2.png'),
                            self.tomato_spritesheet.parse_sprite('crop_tomato3.png'),
                            self.tomato_spritesheet.parse_sprite('crop_tomato4.png')]

        self.days = days
        self.planted_date = days
        self.growth_stage = 0
        self.grow_days = 20
        self.harvestable = False
        self.picked = False
        self.coordx = x + 3
        self.coordy = y + 3

    def get_coordinate(self):
        return self.coordx, self.coordy

    def growing(self, days):
        if (days - self.planted_date) <= self.grow_days:
            # For every 4 days passed since planted date, the crop stage will grow by 1
            if days - (self.planted_date + 4) >= 0 and self.growth_stage < 3:
                self.growth_stage += 1
            if self.growth_stage == 4:
                self.harvestable = True

    def update(self, days, screen):
        self.growing(days)
        screen.blit(self.crop_tomato[self.growth_stage], [self.coordx, self.coordy])


class Potato(Crop):
    def __init__(self, x, y, days, game):
        super(Potato, self).__init__(days, game)
        self.item_id = 2
        # Load tomato's spritesheet
        self.potato_spritesheet = Spritesheet(path.join(map_folder, 'crops.png'))
        self.crop_potato = [self.potato_spritesheet.parse_sprite('crop_potato0.png'),
                            self.potato_spritesheet.parse_sprite('crop_potato1.png'),
                            self.potato_spritesheet.parse_sprite('crop_potato2.png'),
                            self.potato_spritesheet.parse_sprite('crop_potato3.png'),
                            self.potato_spritesheet.parse_sprite('crop_potato4.png')]

        self.game = game
        self.days = days
        self.planted_date = days
        self.growth_stage = 0
        self.grow_days = 20
        self.harvestable = False
        self.picked = False
        self.coordx = x + 4
        self.coordy = y + 4

    def get_coordinate(self):
        return self.coordx, self.coordy

    def growing(self, days):
        if (days - self.planted_date) <= self.grow_days:
            # For every 4 days passed since planted date, the crop stage will grow by 1
            if days - (self.planted_date + 4) == 0 and self.growth_stage < 3:
                self.growth_stage += 1
            if self.growth_stage == 4:
                self.harvestable = True

    def update(self, days, screen):
        self.growing(days)
        screen.blit(self.crop_potato[self.growth_stage], [self.coordx, self.coordy])


class Soil:
    data = []

    def __init__(self, x, y, game):
        self.game = game
        self.coordx = x
        self.coordy = y
        self.plowned = False
        self.seeded = False
        self.img = pygame.image.load(path.join(map_folder, 'tilled_soil.png'))

    def render(self, screen):
        screen.blit(self.img, [self.coordx, self.coordy])
