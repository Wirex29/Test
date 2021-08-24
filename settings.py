from os import path

# Settings
''' WINDOW '''
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "Bootleg Harvest Moon"
FPS = 60

''' colors '''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

''' fonts '''
TITLE_FONT = None
DEFAULT_FONT = None

'''PLAYER SETTING'''
P_SPEED = 100
P_IMG = 'character.png'

'''FOLDER DIRECTORY'''
game_folder = path.dirname(__file__)
asset_folder = path.join(game_folder, 'Assets')
map_folder = path.join(asset_folder, 'Background')
sprites_folder = path.join(asset_folder, 'Character sprites')
