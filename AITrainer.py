import sys

from pymunk import pygame_util
from Boat.AIController import AIController
from Boat.BaseBoat import BaseBoat
from Boat.KeyboardController import KeyboardController
from Boat.SimpleController import SimpleController
from Game import Game
import pygame as pg
import pymunk

from Boat.RadarManager import RadarManager
import Config

class Main:
    def __init__(self, w, h, GAME_FPS):
        self.w, self.h, self.FPS = w, h, GAME_FPS
        self.size = self.w, self.h

    def run_game(self, is_debug=False):
        pg.font.init()
        Config.Screen.DEBUG = True
        pymunk.pygame_util.positive_y_is_up = False
        space = pymunk.Space()
        radarManager = RadarManager(space, Config.Collisiontypes.SENSOR)
        surface = pg.display.set_mode((self.w, self.h))

        level = Config.Tracks.get_track(-1)

        level.build(space)
        boats = [
            BaseBoat(space, radarManager, (Config.Specifications.BOATS[0]), level),
            BaseBoat(space, radarManager, (Config.Specifications.BOATS[2]), level),
            BaseBoat(space, radarManager, (Config.Specifications.BOATS[3]), level),
        ]
        controllers = [
            # SimpleController(boats[0], level),
            SimpleController(boats[0], level),
            AIController(boats[1], level),
            SimpleController(boats[2], level),
            KeyboardController(boats[0], level, pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN),
        ]

        radarManager.registerCollisionType(Config.Collisiontypes.BOAT)
        radarManager.registerCollisionType(Config.Collisiontypes.SHORE)
        radarManager.registerCollisionType(Config.Collisiontypes.CHECKPOINT)

        game = Game(space, surface, radarManager, boats, controllers, self.FPS, level, is_debug)
        exit_code = game.run()
        pg.quit()
        return exit_code


if __name__ == '__main__':
    FPS = 60
    DEBUG = False

    SIZE = WIGHT, HEIGHT = 920, 700
    app = Main(WIGHT, HEIGHT, FPS)

    code = app.run_game(DEBUG)
    # some actions here
    sys.exit(code)
