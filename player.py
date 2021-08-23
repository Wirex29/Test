import pygame as pg
from settings import *
from constant import *
from crops import *
from os import path

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
        # self.image = pg.transform.scale(self.image, [32, 32])
        self.rect = self.image.get_rect()
        self.vel = vector(0, 0)
        self.pos = vector(x, y)
        print("Drawn a player")

    def keys_signal(self):
        keys = pg.key.get_pressed()
        # Character movements
        # Move left
        if keys[pg.K_a]:
            self.vel.x = -P_SPEED
        # Move up
        elif keys[pg.K_w]:
            self.vel.y = -P_SPEED
        # Move down
        elif keys[pg.K_s]:
            self.vel.y = P_SPEED
        # Move right
        elif keys[pg.K_d]:
            self.current_image += 1
            self.vel.x = P_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def plant_crop(self, coordx, coordy, days):
        if not Crop.crop_list:
            Crop.crop_list = [Tomato(coordx, coordy, days, self.game)]
        else:
            Crop.crop_list.append(Potato(coordx, coordy, days, self.game))

    def wall_collision(self, dir):
        pass
        """if dir == 'x':
            
        # for wall in self.game."""

    def update(self):
        self.keys_signal()
        # self.image = self.images[self.current_image]
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y


class Inventory:
    def __init__(self):
        self.item_list = items
        self.money = 50
        print(self.item_list[1])

    def use(self, item):
        self.remove_item(item, 1)

    def add_item(self, item_id, quantity):
        self.item_list[item_id]["Quantity"] = str(int(self.item_list[item_id]["Quantity"]) + quantity)
        # print(self.item_list)

    def remove_item(self, item_id, quantity):
        self.item_list[item_id]["Quantity"] = str(int(self.item_list[item_id]["Quantity"]) - quantity)
        print(self.item_list)


class Shop:
    def __init__(self):
        self.img = None
        self.shop_list = items
        self.sell_button = pg.Rect(120, 320, 50, 50)
        self.buy_button = pg.Rect(170, 320, 50, 50)

    def buy_item(self, inventory, item):
        """and self.buy_button.collidepoint(mouse_pos)"""
        if inventory.money >= int(self.shop_list[item]["Price"]):
            inventory.add_item(item, 1)
            inventory.money -= int(self.shop_list[item]["Price"]) * 4
        else:
            print("Insufficient Funds")

    def sell_item(self, inventory, item):
        # if self.sell_button.collidepoint(mouse_pos):
        inventory.remove_item(item, 1)
        inventory.money += int(self.shop_list[item]["Price"])


"""class Toolbar:
    def __init__(self, width, height):
        self.image = pg.Surface(width, height)
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0 )
        screen.blit(self.image, (0, 0), (x, y, w, h))"""
