import os

from constant import *
from planting import *
from os import path
from spritesheet import Spritesheet
from map import collide_hit_rect

vector = pg.math.Vector2


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.sprite_sheet = Spritesheet(path.join(sprites_folder, "character_sprite.png"))
        self.equipment_sheet = Spritesheet(path.join(map_folder, "equippable_items.png"))
        self.images = [self.sprite_sheet.parse_sprite('character' + str(i) + '.png') for i in range(0, 7)]
        self.equipment_imgs = [self.equipment_sheet.parse_sprite('hoe.png'),
                               self.equipment_sheet.parse_sprite('seed_tomato.png'),
                               self.equipment_sheet.parse_sprite('seed_potato.png')]

        self.equipment_img = self.equipment_imgs[0]
        self.game = game
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect()
        self.interact_rect = pg.Rect(0, 0, 48, 48)
        self.interact_rect.center = self.rect.center
        self.hit_rect = pg.Rect(0, 0, 16, 16)
        self.hit_rect.center = self.rect.center
        self.equipped_item = 0

        self.vel = vector(0, 0)
        self.pos = vector(x, y)
        print("Drawn a player")

    def keys_signal(self):
        keys = pg.key.get_pressed()
        # Character movements
        # Move left
        if keys[pg.K_a]:
            self.current_image = (self.current_image + 0.2) % (len(self.images) - 4)
            self.vel.x = -P_SPEED
        # Move up
        elif keys[pg.K_w]:
            self.current_image = (self.current_image + 0.2) % (len(self.images) - 4)
            self.vel.y = -P_SPEED
        # Move down
        elif keys[pg.K_s]:
            self.current_image = (self.current_image + 0.2) % (len(self.images) - 4)
            self.vel.y = P_SPEED
        # Move right
        elif keys[pg.K_d]:
            self.current_image = (4 + ((self.current_image + 0.2) % (len(self.images) - 4)) % len(self.images))
            self.vel.x = P_SPEED
        if self.vel.x != 0 or self.vel.y != 0:
            self.vel *= 0.2

    def plant_crop(self, soil, days, game):
        soil.is_seeded = True
        soil.growth_stage = 0
        soil.index = 0
        if self.equipped_item == 1 and game.inventory.check_inventory(self.equipped_item) >= 1:
            soil.crop_type = 1
            print(soil.growth_stage)
        elif self.equipped_item == 2 and game.inventory.check_inventory(self.equipped_item) >= 1:
            soil.crop_type = 2
            print(soil.growth_stage)
        soil.planted_date = days

    def harvest(self, soil, game):
        soil.is_seeded = False
        game.inventory.add_item(soil.crop_type, 1)
        print(game.inventory.item_list)
        print(soil.growth_stage)
        print(soil.index)
        print(soil.is_seeded)

    def till_soil(self, soil):
        soil.is_plowed = True

    def switch_item(self, signal):
        self.equipped_item = signal
        if self.equipped_item == 0:
            self.equipment_img = self.equipment_imgs[0]
        elif self.equipped_item == 1:
            self.equipment_img = self.equipment_imgs[1]
        elif self.equipped_item == 2:
            self.equipment_img = self.equipment_imgs[2]

    def update(self):
        self.keys_signal()
        self.image = self.images[int(self.current_image)]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        self.interact_rect.centerx = self.pos.x
        self.interact_rect.centery = self.pos.y


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Inventory:
    def __init__(self):
        self.item_list = items
        self.money = 50

    def use(self, item):
        self.remove_item(item, 1)

    def add_item(self, item_id, quantity):
        self.item_list[item_id]["Quantity"] = str(int(self.item_list[item_id]["Quantity"]) + quantity)
        # print(self.item_list)

    def remove_item(self, item_id, quantity):
        self.item_list[item_id]["Quantity"] = str(int(self.item_list[item_id]["Quantity"]) - quantity)
        print(self.item_list)

    def check_inventory(self, item_id):
        return int(self.item_list[item_id]["Quantity"])


class Shop:
    def __init__(self):
        self.img = pygame.image.load(os.path.join(map_folder, 'shop_menu.png')).convert()
        self.img_rect = self.img.get_rect()
        self.img_rect.centerx = SCREEN_WIDTH / 2
        self.img_rect.centery = SCREEN_HEIGHT / 2
        self.shop_list = items
        self.sell_button1 = pg.Rect(120, 320, 32, 10)
        self.sell_button2 = pg.Rect(120, 320, 32, 10)
        self.buy_button1 = pg.Rect(170, 320, 32, 10)
        self.buy_button2 = pg.Rect(170, 320, 32, 10)
        self.shopping = False

    def buy_item(self, mousepos, inventory):
        if self.shopping:
            if self.buy_button1.collidepoint(mousepos):
                if inventory.money >= int(self.shop_list[4]["Price"]):
                    inventory.add_item(4, 1)
                    inventory.money -= int(self.shop_list[4]["Price"])
                else:
                    print("Insufficient Funds")
            elif self.buy_button2.collidepoint(mousepos):
                if inventory.money >= int(self.shop_list[3]["Price"]):
                    inventory.add_item(3, 1)
                    inventory.money -= int(self.shop_list[3]["Price"])
                else:
                    print("Insufficient Funds")

    def sell_item(self, mousepos, inventory):
        if self.shopping:
            if self.sell_button1.collidepoint(mousepos):
                if inventory.money >= int(self.shop_list[2]["Price"]):
                    inventory.remove_item(2, 1)
                    inventory.money += int(self.shop_list[2]["Price"])
                else:
                    print("Insufficient Funds")
            elif self.buy_button2.collidepoint(mousepos):
                if inventory.money >= int(self.shop_list[1]["Price"]):
                    inventory.remove_item(1, 1)
                    inventory.money += int(self.shop_list[1]["Price"])
                else:
                    print("Insufficient Funds")

    def render(self, screen):
        if self.shopping:
            screen.blit(self.img, self.img_rect)

    def update(self, mouse_pos, inventory):
        self.buy_item(mouse_pos, inventory)
        self.sell_item(mouse_pos, inventory)
"""

"""
