class Crop:
    def __init__(self, game, crop):
        self.game = game
        self.crop = crop
        self.growth_stage = 0
        self.growth_time = 0

    def update(self):
        if self.growth_time == 4:
            self.growth_stage += 1

