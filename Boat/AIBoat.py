import pygame as pg
from Boat.BaseBoat import BaseBoat

class AIBoat(BaseBoat):
    def __init__(self, space, radarManager, settings):
        super().__init__(space, settings)

    def update(self, level):
        x, y = self.car_shape.body.position.x, self.car_shape.body.position.y
        level.get_next_checkpoint(x,y)

        return super().update(self.move, self.turn)