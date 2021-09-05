from os import path

# Settings
''' WINDOW '''
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TITLE = "Bootleg Harvest Moon"
FPS = 60

''' colors '''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BROW = (204, 136, 0)


''' fonts '''
TITLE_FONT = None
DEFAULT_FONT = None

'''PLAYER SETTING'''
P_SPEED = 20
P_IMG = 'character.png'

'''LAYERS'''
SOIL_LAYER = 1
CROP_LAYER = 2

'''FOLDER DIRECTORY'''
game_folder = path.dirname(__file__)
asset_folder = path.join(game_folder, 'Assets')
map_folder = path.join(asset_folder, 'Background')
sprites_folder = path.join(asset_folder, 'Character sprites')

