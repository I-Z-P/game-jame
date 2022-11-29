# this is config file

# absolute path of the project root
import os
ROOT_PATH = os.path.abspath('../')

# app window
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 720

# game core settings
TICKRATE = 200
TILE_SIZE = 128

# debugging and console logging
DEV = False
FPS_COUNTER = True
if not DEV:
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# player animations
animations_knight = {"run":["../player/Knight/noBKG_KnightRun_strip.png",8],
                     "stand": ["../player/Knight/noBKG_KnightIdle_strip.png", 15],
                     "attack": ["../player/Knight/noBKG_KnightAttack_strip.png", 22],
                     "jump": ["../player/Knight/noBKG_KnightJumpAndFall_strip.png", 15],
                     "shield": ["../player/Knight/noBKG_KnightShield_strip.png", 7],
                     "roll": ["../player/Knight/noBKG_KnightRoll_strip.png", 15]}

animations_wizard = {"run":["../player/Wizard/Run.png",8],
                     "stand": ["../player/Wizard/Idle.png", 8],
                     "attack": ["../player/Wizard/Attack1.png", 8],
                     "jump": ["../player/Wizard/Jump.png", 2],
                     "shield": ["../player/Wizard/Attack2.png", 8],
                     "roll": ["../player/Wizard/Death.png", 7]}