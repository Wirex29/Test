from spritesheet import Spritesheet
from os import path


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
        # Get and store Game's directory
        game_folder = path.dirname(__file__)
        asset_folder = path.join(game_folder, 'Assets')
        map_folder = path.join(asset_folder, 'Background')

        # Load tomato's spritesheet
        self.tomato_spritesheet = Spritesheet(path.join(map_folder, 'crops.png'))
        self.crop_tomato = [self.tomato_spritesheet.parse_sprite('crop_tomato0.png'),
                            self.tomato_spritesheet.parse_sprite('crop_tomato1.png'),
                            self.tomato_spritesheet.parse_sprite('crop_tomato2.png'),
                            self.tomato_spritesheet.parse_sprite('crop_tomato3.png'),
                            self.tomato_spritesheet.parse_sprite('crop_tomato4.png')]
        self.game = game
        self.days = days
        self.planted_date = days
        self.growth_stage = 0
        self.grow_days = 20
        self.harvestable = False
        self.coordx = x
        self.coordy = y

    def growing(self, days):
        if (days - self.planted_date) <= self.grow_days:
            # For every 4 days passed since planted date, the crop stage will grow by 1
            if (days % (self.planted_date + 4)) == 0 and self.growth_stage < 5:
                self.growth_stage += 1
            if self.growth_stage == 5:
                self.harvestable = True

    def update(self, days, screen):
        self.growing(days)
        screen.blit(self.crop_tomato[self.growth_stage], [self.coordx, self.coordy])


class Potato(Crop):
    def __init__(self, x, y, days, game):
        super(Potato, self).__init__(days, game)
        # Get and store Game's directory
        game_folder = path.dirname(__file__)
        asset_folder = path.join(game_folder, 'Assets')
        map_folder = path.join(asset_folder, 'Background')

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
        self.coordx = x
        self.coordy = y

    def growing(self, days):
        if (days - self.planted_date) <= self.grow_days:
            # For every 4 days passed since planted date, the crop stage will grow by 1
            if (days % (self.planted_date + 4)) == 0 and self.growth_stage < 5:
                self.growth_stage += 1
            if self.growth_stage == 5:
                self.harvestable = True

    def update(self, days, screen):
        self.growing(days)
        screen.blit(self.crop_potato[self.growth_stage], [self.coordx, self.coordy])


"""list_a = [Tomato(day)]
list_a.append(Tomato(day))
print(day)
for i in range(16):
    day += 1
    for obj in list_a:
        obj.growing(day)
        print("Current stage of plant:", obj.growth_stage)
        print("Grew for:", day - obj.planted_date, "days")
        print("Is havestable: ", str(obj.harvestable))"""
