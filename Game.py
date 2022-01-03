from Boat.BaseBoat import BaseBoat
from Boat.KeyboardController import KeyboardController
import pygame as pg
import pymunk
from Boat.Camera import Camera
import pymunk.pygame_util

class Game:
    def __init__(self,  w, h, FPS, level, debug=False):
        self.w, self.h, self.FPS = w, h, FPS
        self.size = self.w, self.h
        self.debug_mode = debug
        self.screen, self.clock = self.init_window()

        self.time_delta = 0

        pg.init()
        pymunk.pygame_util.positive_y_is_up = False

        self.surface = pg.display.set_mode((w, h))
        self.draw_options = pymunk.pygame_util.DrawOptions(self.surface)
        self.camera = Camera()

        self.space = pymunk.Space()
        self.space.gravity = 0, 0
        self.boats = [
            BaseBoat(self.space, (0.5, "yacht.png", 0.5, 0.61)),
            BaseBoat(self.space, (0.5, "yacht.png", 0.5, 0.61))
        ]
        self.keyboardControllers = [
            KeyboardController(self.boats[0], pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN),
            KeyboardController(self.boats[1], "a", "d", "w", "s")
        ]

        self.level = level
        level.build(self.space, (100, 73))
        level.arrangeBoats(self.boats)

    def init_window(self):
        screen = pg.display.set_mode(self.size)
        clock = pg.time.Clock()
        return screen, clock

    def run(self):
        while True:
            self.time_delta = self.clock.tick(60) / 1000.0
            events = pg.event.get()
            if not self.events(events):
                return 0
            if not self.update():
                return 0

    def update(self):
        playerX, playerY, playerVelocity = self.boats[0].update()
        self.boats[1].update()
        cx, cy, scaling = self.camera.update(playerX-300, playerY-300, playerVelocity)
        self.space.step(1 /self.FPS)
        self.draw_options.transform = (
            pymunk.Transform.scaling(scaling)
            @ pymunk.Transform(tx=cx, ty=cy)
        )
        self.space.debug_draw(self.draw_options)
        for boat in self.boats:
            boat.updateImage(self.surface, cx, cy, scaling)
        
        pg.display.flip()
        self.screen.fill('black')
        self.render_fps(str(int(self.clock.get_fps())), (0, 0))
        if self.level.get_next_checkpoint(playerX, playerY) == (0,0):
            return False
        return True

    def events(self, events):
        for event in events:
            if event.type == pg.QUIT:
                return False
            for keyboardController in self.keyboardControllers:
                keyboardController.processEvent(event)
        return True

    def render_fps(self, text, pos):
        font = pg.font.Font(None, 30)
        render_text = font.render(text + ' FPS', True, pg.Color('green'))
        self.screen.blit(render_text, pos)
