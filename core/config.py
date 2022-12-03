# this is config file

# absolute path of the project root
import os
ROOT_PATH = os.path.abspath('../')

# app window
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

# game core settings
TICKRATE = 1000 # should be set to 1000+ to avoid lags
TILE_SIZE = 32

# debugging and console logging
DEV = True
FPS_COUNTER = False
if not DEV:
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# player animations
animations_knight = {"run":["../assets/Knight/run.png",7],
                     "jump":["../assets/Knight/jump.png",8],
                     "stand":["../assets/Knight/idle.png",4],
                     "attack": ["../assets/Knight/attack.png", 7]}

animations_wizard = {"run":["../assets/Wizard/Run.png",8],
                     "stand": ["../assets/Wizard/Idle.png", 8],
                     "attack": ["../assets/Wizard/Attack1.png", 8],
                     "jump": ["../assets/Wizard/Jump.png", 2],
                     "shield": ["../assets/Wizard/Attack2.png", 8],
                     "roll": ["../assets/Wizard/Death.png", 7]}

# objects animations
stone = {'full':["../assets/Stone/full.png",1],
         '1':["../assets/Stone/1.png",1],
         '2':["../assets/Stone/2.png",1],
         'animation': ['../assets/Stone/animation.png',12]}