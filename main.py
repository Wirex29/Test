import time
import pygame
import sys
import os

from data.settings import *
from data.player import *
from data.map import *

# Make window
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption(TITLE)

# Pygame clock
clock = pygame.time.Clock()
last_time = time.time()

# Load assets
font_sm = pygame.font.Font(DEFAULT_FONT, 24)
font_md = pygame.font.Font(DEFAULT_FONT, 28)
font_xl = pygame.font.Font(TITLE_FONT, 96)


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Time:
    def __init__(self):
        self.hidden_timer = (pg.time.get_ticks() // 1000)
        self.minute = 0
        self.hour = 7
        self.day = 1
        self.last_minute = 0

    def running_time(self):
        self.last_minute = self.hidden_timer
        # print("Last minute:", self.last_minute)
        self.hidden_timer = (pg.time.get_ticks() // 1000)
        # print("Hidden timer:", self.hidden_timer)
        if self.minute < 59:
            if self.hidden_timer >= self.minute and self.hidden_timer != self.last_minute:
                self.minute += 1
                # print("Minute:", self.minute)
        else:
            if self.hour < 23:
                self.hour += 1
            else:
                self.hour = 0
                self.day += 1
            self.minute = 0

    def pass_day(self):
        self.minute = 0
        self.hour = 7
        self.day += 1

    def render(self, money):
        self.container = pygame.image.load(os.path.join(map_folder, "date_time.png")).convert_alpha()

        self.calendar = font_md.render("Days: " + str(self.day).zfill(2), False, BLACK)
        self.clock = font_md.render(str(self.hour).zfill(2) + ":" + str(self.minute).zfill(2), False, BLACK)
        self.gold_info = font_md.render("Gold: " + str(money), False, BLACK)

        self.container_rect = self.container.get_rect()
        self.container_rect.top, self.container_rect.left = [0, 0]

        self.calendar_rect = self.calendar.get_rect()
        self.calendar_rect.top, self.calendar_rect.left = [8, 13]

        self.gold_info_rect = self.gold_info.get_rect()
        self.gold_info_rect.top, self.gold_info_rect.left = [64, 13]

        self.clock_rect = self.clock.get_rect()
        self.clock_rect.top, self.clock_rect.left = [36, 13]

        screen.blit(self.container, self.container_rect)
        screen.blit(self.calendar, self.calendar_rect)
        screen.blit(self.clock, self.clock_rect)
        screen.blit(self.gold_info, self.gold_info_rect)

    def update(self):
        # self.pass_day()
        self.running_time()


# Scenes
class Scene:
    def __init__(self):
        self.next_scene = self

    def process_input(self, events, keys):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

    def terminate(self):
        self.next_scene = None


class TitleScene(Scene):
    def __init__(self):
        super().__init__()
        self.bg_menu = pygame.image.load(os.path.join(map_folder, 'menu.png')).convert()
        print(os.path.join(map_folder, 'start_button.png'))
        self.start_img = pygame.image.load(os.path.join(map_folder, 'start_button.png'))
        self.start_button = pygame.Rect(480, 288, 320, 72)
        self.exit_img = pygame.image.load(os.path.join(map_folder, 'exit_button.png'))
        self.exit_button = pygame.Rect(480, 432, 320, 72)
        self.rect = self.bg_menu.get_rect()
        self.rect.left, self.rect.top = (0, 0)

    def process_input(self, events, keys):
        for event in events:
            """if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_scene = GameScene()"""
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.start_button.collidepoint(mouse_pos):
                    print("Starting Game...")
                    self.next_scene = GameScene()
                elif self.exit_button.collidepoint(mouse_pos):
                    print("Exiting...")
                    self.terminate()

    def update(self):
        pass

    def render(self):
        screen.fill(BLACK)
        self.bg_menu = pygame.transform.scale(self.bg_menu, [SCREEN_WIDTH, SCREEN_HEIGHT])
        screen.blit(self.bg_menu, self.rect)
        screen.blit(self.start_img, self.start_button)
        screen.blit(self.exit_img, self.exit_button)


class GameScene(Scene):
    def __init__(self):
        super().__init__()
        # Load map data
        self.map = TiledMap(os.path.join(map_folder, 'Map.tmx'))
        self.map_img = self.map.make_map()

        # self.map_img = pygame.transform.scale(self.map_img, [SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2])

        self.map_rect = self.map_img.get_rect()

        self.camera = Camera(self.map.width, self.map.height)
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.soils = pg.sprite.Group()

        for tile_object in self.map.gameMap.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'obstacle':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'soil':
                Soil.data.append(Soil(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height))
            if tile_object.name == 'shop':
                Shop.list.append(Shop(tile_object.x, tile_object.y, tile_object.width, tile_object.height))

        self.inventory = Inventory()
        self.dt = clock.tick(FPS) / 1000
        self.time = Time()
        self.draw_debug = False

    def process_input(self, events, keys):
        for event in events:
            # Space bar to end the game and switch to EndScene
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_scene = TitleScene()
                elif event.key == pygame.K_j:
                    print("passed day")
                    self.time.pass_day()
                elif event.key == pygame.K_h:
                    self.draw_debug = not self.draw_debug
                elif event.key == pygame.K_1:
                    self.player.switch_item(0)
                    print(self.player.equipped_item)
                elif event.key == pygame.K_2:
                    self.player.switch_item(1)
                    print(self.player.equipped_item)
                elif event.key == pygame.K_3:
                    self.player.switch_item(2)
                    print(self.player.equipped_item)

            # Plant crop at the mouse click position
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()

                for soil in Soil.data:
                    if soil.rect.collidepoint(mouse_pos) and soil.rect.colliderect(self.player.interact_rect):
                        print("hit")
                        if soil.is_plowed is False and self.player.equipped_item == 0:
                            print(soil.x, soil.y)
                            self.player.till_soil(soil)
                        elif soil.is_plowed and soil.is_seeded is False:
                            soil.is_seeded = True
                            self.player.plant_crop(soil, self.time.day)
                            soil.planted_date = self.time.day
                        elif soil.is_plowed and soil.is_seeded and soil.harvestable:
                            self.player.harvest(soil, self)

                for shop in Shop.list:
                    if shop.rect.colliderect(self.player.interact_rect):
                        shop.shopping = True
                    if shop.shopping:
                        shop.buy_item(mouse_pos, self.inventory)
                        shop.sell_item(mouse_pos, self.inventory)
                        shop.exit_shop(mouse_pos)

    def update(self):
        # Update character
        self.all_sprites.update()

        # Maintain camera Rectangle on the player
        self.camera.update(self.player)

        # Iterate through every crop object stored in the list and update the status of it
        for soil in Soil.data:
            soil.update(self.time.day, self.map_img)

        # Update time
        self.time.update()

        # Update shop
        for shop in Shop.list:
            shop.update(pygame.mouse.get_pos(), self.inventory)

    def render(self):
        # Map render
        screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

        # Character renwder
        for sprite in self.all_sprites:
            screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pygame.draw.rect(screen, CYAN, self.camera.apply_rect(sprite.interact_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pygame.draw.rect(screen, CYAN, self.camera.apply_rect(wall.rect), 1)
            for soil in self.soils:
                pygame.draw.rect(screen, CYAN, self.camera.apply_rect(soil.rect), 1)

        for shop in Shop.list:
            shop.render(screen)

        # Clock render
        self.time.render(self.inventory.money)


class EndScene(Scene):
    def __init__(self):
        super().__init__()

    def process_input(self, events, keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_scene = TitleScene()

    def update(self):
        pass

    def render(self):
        screen.fill(BLACK)
        text = font_xl.render("Game Over", True, WHITE)
        rect = text.get_rect()
        rect.centerx = SCREEN_WIDTH // 2
        rect.centery = SCREEN_HEIGHT // 2
        screen.blit(text, rect)


class OptionScene(Scene):
    def __init__(self):
        super().__init__()

    def process_input(self, events, keys):
        """for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_scene = TitleScene()"""
        pass

    def update(self):
        pass

    def render(self):
        screen.fill(BLACK)
        text = font_xl.render("Option scene", True, WHITE)
        rect = text.get_rect()
        rect.centerx = SCREEN_WIDTH // 2
        rect.centery = SCREEN_HEIGHT // 2
        screen.blit(text, rect)


# Main game class
class Game:
    def __init__(self):
        self.active_scene = TitleScene()

    @staticmethod
    def is_quit_event(event, pressed_keys):
        x_out = event.type == pygame.QUIT
        ctrl = pressed_keys[pygame.K_LCTRL] or pressed_keys[pygame.K_RCTRL]
        q = pressed_keys[pygame.K_q]

        return x_out or (ctrl and q)

    def run(self):
        while self.active_scene is not None:
            # Get user input
            pressed_keys = pygame.key.get_pressed()
            filtered_events = []

            # Quit tracking
            for event in pygame.event.get():
                if self.is_quit_event(event, pressed_keys):
                    self.active_scene.terminate()
                else:
                    filtered_events.append(event)

            # Manage scene
            self.active_scene.process_input(filtered_events, pressed_keys)
            self.active_scene.update()
            self.active_scene.render()
            self.active_scene = self.active_scene.next_scene

            # Update and tick
            pygame.display.flip()
            clock.tick(FPS)


# Run the program
if __name__ == "__main__":
    main = Game()
    main.run()
    pygame.quit()
