import sys
import pymunk
import pygame as pg

from random import choice, randrange

from Boat.RadarManager import RadarManager
from Boat.BaseBoat import BaseBoat
from Boat.KeyboardController import KeyboardController
from Boat.SimpleController import SimpleController
from Game import Game, MenuError
from Config import Collisiontypes
from Config import Specifications
from Config import Tracks
from database import Records
from startscreen import Startscreen
from table_records import Table_records


class Main:
    def __init__(self, w, h, GAME_FPS):
        self.w, self.h, self.FPS = w, h, GAME_FPS
        self.size = self.w, self.h

    def run_game(self, is_debug=False):
        while True:
            pg.font.init()
            start = Startscreen()
            start.start()
            while start.res[0] == 'records':
                try:
                    table = Table_records()
                    table.start()
                except Exception as e:
                    e.__str__()
                start.start()
            pg.init()
            pymunk.pygame_util.positive_y_is_up = False
            space = pymunk.Space()
            radarManager = RadarManager(space, Collisiontypes.SENSOR)
            surface = pg.display.set_mode((self.w, self.h))

            level = Tracks.get_track(start.res[0] - 1)

            level.build(space)
            c = [0, 1, 2, 3, 4, 5]
            c.remove(start.res[1] - 1)
            boats = [BaseBoat(space,
                              radarManager,
                              (Specifications.BOATS[start.res[1] - 1]),
                              level),
                     ]
            for i in range(4):
                a = choice(c)
                boats.append(
                    BaseBoat(
                        space,
                        radarManager,
                        (Specifications.BOATS[a]),
                        level))
                c.remove(a)
            controllers = [
                SimpleController(
                    boats[1], level), SimpleController(
                    boats[2], level), SimpleController(
                    boats[3], level), SimpleController(
                    boats[4], level), KeyboardController(
                        boats[0], level, pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN), ]

            radarManager.register_collision_type(Collisiontypes.BOAT)
            radarManager.register_collision_type(Collisiontypes.SHORE)
            radarManager.register_collision_type(Collisiontypes.CHECKPOINT)
            try:
                game = Game(
                    space,
                    surface,
                    radarManager,
                    boats,
                    controllers,
                    self.FPS,
                    level,
                    is_debug)
                exit_code = game.run()
            except MenuError:
                pass
            except Exception as e:
                print(e.__str__())
                game = None
                return -1
            if game:
                if not game.name:
                    yacht = Records.create(name='Гость' + str(randrange(99)),
                                           yacht=Specifications.BOATS[start.res[1] - 1][1],
                                           points=game.points, track=start.res[0])
                    yacht.save()
                else:
                    yacht = Records.create(name=game.name,
                                           yacht=Specifications.BOATS[start.res[1] - 1][1],
                                           points=game.points,
                                           track=start.res[0])
                    yacht.save()


if __name__ == '__main__':
    FPS = 60
    DEBUG = False

    SIZE = WIGHT, HEIGHT = 920, 700
    app = Main(WIGHT, HEIGHT, FPS)

    code = app.run_game(DEBUG)
    # some actions here
    pg.quit()
    sys.exit(code)
