import sys
# from Boat.AIController import AIController
from Boat.BaseBoat import BaseBoat
from Boat.KeyboardController import KeyboardController
from Boat.SimpleController import SimpleController
from Game import Game
import pygame as pg
import pymunk

from Boat.RadarManager import RadarManager
from Config import Collisiontypes
from Config import Specifications
from Boat.mapGenerator import MapGenerator
from Config import Tracks
from startscreen import Startscreen
from table_records import Table_records


class Main:
    def __init__(self, w, h, GAME_FPS):
        self.w, self.h, self.FPS = w, h, GAME_FPS
        self.size = self.w, self.h

    def run_game(self, is_debug=False):
        pg.font.init()
        start = Startscreen()
        start.start()
        while start.res[0] == 'records':
            try:
                table = Table_records()
                table.start()
            except Exception:
                pass
            start.start()
        pg.init()
        pymunk.pygame_util.positive_y_is_up = False
        space = pymunk.Space()
        radarManager = RadarManager(space, Collisiontypes.SENSOR)
        surface = pg.display.set_mode((self.w, self.h))

        level = Tracks.get_track(start.res[0] - 1)

        level.build(space)#MapGenerator(30, 30, 35, 35, 22))
        #level.build(space, (100, 73), MapGenerator(24, 24, 29, 29, 18))
        #level.build(space, (100, 73), MapGenerator(25, 25, 30, 30, 36))
        #level.build(space, (100, 73), MapGenerator(15, 15, 19, 19, 3))
        boats = [
            BaseBoat(space, radarManager, (Specifications.BOATS[start.res[1] - 1]), level),
            BaseBoat(space, radarManager, (Specifications.BOATS[3]), level),
            # BaseBoat(space, radarManager, (0.5, "yacht.png", 150, 0.01, 0.005), level)
        ]
        controllers = [
            # SimpleController(boats[0], level),
            SimpleController(boats[1], level),
            KeyboardController(boats[0], level, pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN),
            # KeyboardController(boats[1], level, "a", "d", "w", "s")
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
    DEBUG = False

    SIZE = WIGHT, HEIGHT = 920, 700
    app = Main(WIGHT, HEIGHT, FPS)

    code = app.run_game(DEBUG)
    # some actions here
    sys.exit(code)
