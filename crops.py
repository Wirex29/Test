class Crop:
    def __init__(self, game):
        self.game = game
        self.growth_stage = 0
        self.growth_time = 0

    def update(self):
        if self.growth_time == 4:
            self.growth_stage += 1


class Tomato():
    def __init__(self, days):
        self.days = days
        # super(Tomato, self).__init__(game)
        self.crop_type = "tomato"
        self.planted_date = days
        self.growth_stage = 0
        self.grow_days = 16
        self.harvestable = False

    def growing(self, days):
        if (days - self.planted_date) <= self.grow_days:
            if (days - self.planted_date) % 4 == 0 and self.growth_stage < 4:
                self.growth_stage += 1
            if self.growth_stage == 4:
                self.harvestable = True

    def update(self, day):
        self.growing(day)


day = 1
list_a = [Tomato(day)]
list_a.append(Tomato(day))
print(day)
for i in range(16):
    day += 1
    for obj in list_a:
        obj.growing(day)
        print("Current stage of plant:", obj.growth_stage)
        print("Grew for:", day - obj.planted_date, "days")
        print("Is havestable: ", str(obj.harvestable))
