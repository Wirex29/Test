class Crop:
    def __init__(self, game):
        self.game = game
        self.growth_stage = 0
        self.growth_time = 0

    def update(self):
        if self.growth_time == 4:
            self.growth_stage += 1


class Tomato(Crop):
    def __init__(self, game):
        super(Tomato, self).__init__(game)
        self.crop_type = "tomato"
        self.grow_day = 0
        self.growth_time = 16
        self.growth_stage = 0

    def plant_crop(self, days):
        self.grow_day = days

    def growing(self, days):
        while self.grow_day <= self.growth_time:
            if (days - self.grow_day) % 4 >= 1:
                self.growth_stage += 1

    def update(self):
        pass
