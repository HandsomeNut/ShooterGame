
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


class Ball(pg.sprite.Sprite):
    """A ball that will move across the screen
    Returns: ball object
    Functions: update, calcnewpos
    Attributes: area, vector"""

    def __init__(self, vector):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("ball.png")
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.vector = vector

    def update(self):
        newpos = self.calcnewpos(self.rect, self.vector)
        self.rect = newpos

    def calcnewpos(self, rect, vector):
        (angle, z) = vector
        (dx, dy) = (z*math.cos(angle), z*math.sin(angle))
        return rect.move(dx, dy)


def main():

    ball = Ball()

    while 1:
        ball.update()
