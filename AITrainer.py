import sys
import pygame as pg
import pymunk
from Boat.AIBoat import AIBoat
from Boat.PlayerBoat import PlayerBoat
from Boat.levelBuilder import SandBox
from Boat.RadarManager import RadarManager
import Game

class Main:
    def __init__(self, w, h, GAME_FPS):
        self.w, self.h, self.FPS = w, h, GAME_FPS
        self.size = self.w, self.h

    def run_game(self, is_debug=False):
        pg.init()
        pymunk.pygame_util.positive_y_is_up = False
        space = pymunk.Space()
        radarManager = RadarManager(space)
        surface = pg.display.set_mode((self.w, self.h))

        boats =   [PlayerBoat(space, radarManager, (0.5, "yacht.png", 0.5, 0.61), pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN),
                   AIBoat(space, radarManager, (0.5, "yacht.png", 0.5, 0.61))]

        game = Game.Game(space, surface, radarManager, boats, self.FPS, SandBox(), is_debug)
        exit_code = game.run()
        pg.quit()
        return exit_code


if __name__ == '__main__':
    FPS = 60
    DEBUG = False

    SIZE = WIGHT, HEIGHT = 900, 720
    app = Main(WIGHT, HEIGHT, FPS)

    code = app.run_game(DEBUG)
    # some actions here
    sys.exit(code)
