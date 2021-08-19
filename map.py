import pytmx
import pygame as pg
from settings import *


class TiledMap:
    def __init__(self, filename):
        self.gameMap = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.gameMap.tilewidth * self.gameMap.width
        self.height = self.gameMap.tileheight * self.gameMap.height

    def render(self, surface):
        for layer in self.gameMap.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.gameMap.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.gameMap.tilewidth, y * self.gameMap.tileheight))

    def make_map(self):
        mapSurface = pg.Surface((self.width, self.height))
        self.render(mapSurface)
        return mapSurface

    def get_tile_pos(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                x, y = mouse_pos
                print(int(x - (x % 16)), int(y - (y % 16)))


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width * 2
        self.height = height * 2

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - SCREEN_WIDTH), x)  # right
        y = max(-(self.height - SCREEN_HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
