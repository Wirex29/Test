from data.constant import *
from data.planting import *
from os import path
from data.spritesheet import Spritesheet
from data.map import collide_hit_rect, TiledMap

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

    def plant_crop(self, soil, days):
        soil.is_seeded = True
        soil.growth_stage = 0
        soil.index = 0
        if self.equipped_item == 1 and self.game.inventory.check_inventory(3) >= 1:
            soil.crop_type = 1
            self.game.inventory.remove_item(3, 1)
            print(soil.growth_stage)
        elif self.equipped_item == 2 and self.game.inventory.check_inventory(4) >= 1:
            soil.crop_type = 2
            self.game.inventory.remove_item(4, 1)
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

    def buy_plot(self):
        if self.game.inventory.money >= 500:
            self.game.map = TiledMap(path.join(map_folder, "Map2.tmx"))
            self.game.map_img = self.game.map.make_map()
            self.game.map_rect = self.game.map_img.get_rect()
            self.game.walls = pg.sprite.Group()
            self.game.soils = pg.sprite.Group()
            for tile_object in self.game.map.gameMap.objects:
                if tile_object.name == 'obstacle':
                    Obstacle(self.game, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                if tile_object.name == 'soil':
                    Soil.data.append(
                        Soil(self.game, tile_object.x, tile_object.y, tile_object.width, tile_object.height))
                if tile_object.name == 'shop':
                    self.game.shop = Shop(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            self.game.inventory.money -= 500
        else:
            print("Insufficient money")

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


class BuyPlot:
    def __init__(self, game, x, y, w, h):
        self.game = game
        self.img = pg.image.load(path.join(map_folder, 'buy_plot.png')).convert_alpha()
        self.img_rect = self.img.get_rect()
        self.img_rect.x = x + 100
        self.img_rect.y = SCREEN_HEIGHT / 2
        self.x = x
        self.y = y
        self.rect = pg.Rect(x, y, w, h)
        self.rect.x = x
        self.rect.y = y
        self.button1 = pg.Rect(self.img_rect.x + 8, self.img_rect.y + 64, 40, 16)
        self.button2 = pg.Rect(self.img_rect.x + 80, self.img_rect.y + 64, 40, 16)
        self.is_rendered = False

    def render(self, screen):
        if self.is_rendered:
            screen.blit(self.img, self.img_rect)

    def interaction(self, mousepos):
        # Interaction "No"
        if self.button1.collidepoint(mousepos):
            self.is_rendered = False
        # Interaction "Yes"
        elif self.button2.collidepoint(mousepos):
            print("Bought")
            self.game.player.buy_plot()
            self.is_rendered = False


class Shop:
    def __init__(self, x, y, w, h):
        self.img = pg.image.load(path.join(map_folder, 'shop_menu.png')).convert_alpha()
        self.img_rect = self.img.get_rect()
        self.img_rect.x = x + 100
        self.img_rect.y = y
        self.x = x
        self.y = y
        self.rect = pg.Rect(x, y, w, h)
        self.rect.x = x
        self.rect.y = y
        self.shop_list = items
        self.buy_button1 = pg.Rect(self.img_rect.x + 40, self.img_rect.y + 40, 32, 10)
        self.buy_button2 = pg.Rect(self.img_rect.x + 109, self.img_rect.y + 40, 32, 10)
        self.sell_button1 = pg.Rect(self.img_rect.x + 39, self.img_rect.y + 96, 32, 10)
        self.sell_button2 = pg.Rect(self.img_rect.x + 109, self.img_rect.y + 95, 32, 10)
        self.exit_button = pg.Rect(self.img_rect.x + 120, self.img_rect.y, 25, 17)
        self.shopping = False

    def buy_item(self, mousepos, inventory):
        if self.shopping:
            if self.buy_button1.collidepoint(mousepos):
                if inventory.money >= int(self.shop_list[4]["Price"]):
                    inventory.add_item(4, 1)
                    inventory.money -= int(self.shop_list[4]["Price"])
                    print("Bought potato seed x1")
                else:
                    print("Insufficient Funds")
            elif self.buy_button2.collidepoint(mousepos):
                if inventory.money >= int(self.shop_list[3]["Price"]):
                    inventory.add_item(3, 1)
                    inventory.money -= int(self.shop_list[3]["Price"])
                    print("Bought tomato seed x1")
                else:
                    print("Insufficient Funds")

    def sell_item(self, mousepos, inventory):
        if self.shopping:
            if self.sell_button1.collidepoint(mousepos):
                if inventory.money >= int(self.shop_list[2]["Price"]) and inventory.check_inventory(2) > 0:
                    inventory.remove_item(2, 1)
                    inventory.money += int(self.shop_list[2]["Price"])
                    print("Sold potato x1")
                elif inventory.money < int(self.shop_list[2]["Price"]):
                    print("Insufficient Funds")
                elif inventory.check_inventory(2) < 0:
                    print("No item to sell!")
            elif self.sell_button2.collidepoint(mousepos):
                if inventory.money >= int(self.shop_list[1]["Price"]) and inventory.check_inventory(1) > 0:
                    inventory.remove_item(1, 1)
                    inventory.money += int(self.shop_list[1]["Price"])
                    print("Sold tomato x1")
                elif inventory.money < int(self.shop_list[1]["Price"]):
                    print("Insufficient Funds")
                elif inventory.check_inventory(1) < 0:
                    print("No item to sell!")

    def render(self, screen):
        if self.shopping:
            screen.blit(self.img, self.img_rect)

    def exit_shop(self, mousepos):
        if self.shopping and self.exit_button.collidepoint(mousepos):
            self.shopping = False

    def update(self, mouse_pos, inventory):
        pass
