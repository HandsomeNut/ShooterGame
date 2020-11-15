
VERSION = "0.4"
try:
    import sys
    import random
    import math
    import os
    import getopt
    import pygame as pg
    from socket import *
    from pygame.locals import *
except ImportError as err:
    print(f"couldn't load module {err}")
    sys.exit(2)

def load_png(name):
    """ Load image an return image object"""
    fullname = os.path.join('data', name)
    try:
        image = pg.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pg.error as message:
        print(f"Cannot load image: {fullname}")
        raise SystemExit and message
    return image, image.get_rect()