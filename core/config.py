# this is config file

# absolute path of the project root
import os
ROOT_PATH = os.path.abspath('../')

# app window
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 720

# game core settings
TICKRATE = 60
TILE_SIZE = 128

# debugging and console logging
DEV = True
if not DEV:
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"