import sys
from Boat.AIController import AIController
from Boat.BaseBoat import BaseBoat
from Boat.KeyboardController import KeyboardController
from Boat.SimpleController import SimpleController
from Game import Game
import pygame as pg
import pymunk
from Boat.levelBuilder import SandBox
from Boat.levelBuilder2 import SandBox2
from Boat.RadarManager import RadarManager

from Utills.FieldGenerator import FiledGenerator
from config import Collisiontypes

class Main:
    def __init__(self, w, h, GAME_FPS):
        self.w, self.h, self.FPS = w, h, GAME_FPS
        self.size = self.w, self.h

    def run_game(self, is_debug=False):
        pg.init()
        pymunk.pygame_util.positive_y_is_up = False
        space = pymunk.Space()
        radarManager = RadarManager(space, Collisiontypes.SENSOR)
        surface = pg.display.set_mode((self.w, self.h))
        level = SandBox2()
        level.build(space, (100, 73))

        boats = [
            BaseBoat(space, radarManager, (0.5, "yacht.png", 30, 1, 0.1), level),
            BaseBoat(space, radarManager, (0.5, "yacht.png", 30, 10, 0.1), level),
            BaseBoat(space, radarManager, (0.5, "yacht.png", 30, 10, 0.1), level)
        ]
        controllers = [
            # SimpleController(boats[0], level),
            SimpleController(boats[1], level),
            SimpleController(boats[2], level),
            KeyboardController(boats[0], pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN),
        ]

        radarManager.registerCollisionType(Collisiontypes.BOAT)
        radarManager.registerCollisionType(Collisiontypes.SHORE)
        radarManager.registerCollisionType(Collisiontypes.CHECKPOINT)

        game = Game(space, surface, radarManager, boats, controllers, self.FPS, level, is_debug)
        exit_code = game.run()
        pg.quit()
        return exit_code


if __name__ == '__main__':
    FPS = 60
    DEBUG = True

    SIZE = WIGHT, HEIGHT = 900, 720
    app = Main(WIGHT, HEIGHT, FPS)

    code = app.run_game(DEBUG)
    # some actions here
    sys.exit(code)
    # # field = FiledGenerator(64, 64, 2, 8)
    # # field.generate_new()
    # l = FiledGenerator(70, 70, 8, 16)
    # l.generate_new()
    # print(l.get_field(), l.get_back_field())
