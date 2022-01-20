import math
import os
import sys
import pygame as pg


class DelayedUpdate:
    def __init__(self, initial=math.nan, k=0.1):
        self.k = k
        self.oldValue = initial
        self.speed = 0

    def update(self, current):
        if math.isnan(self.oldValue):
            self.oldValue = current
            return (current, current)
        err = (current - self.oldValue) * self.k
        self.speed = self.speed * 0.8 + err * 0.2

        self.oldValue += self.speed
        return (self.oldValue, self.speed)


def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    if not os.path.isfile(fullname):
        print("Файл не найден " + fullname)
        sys.exit()
    image = pg.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
