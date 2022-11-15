# this is config file


# app window
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 720

# game core settings
TICKRATE = 60

# debugging and console logging
DEV = False
if not DEV:
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"