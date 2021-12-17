import pygame as pg
import pymunk

from Boat.PlayerBoat import PlayerBoat


class Game:
    def __init__(self, w, h, FPS, debug=False):
        self.w, self.h, self.FPS = w, h, FPS
        self.size = self.w, self.h
        self.debug_mode = debug
        self.screen, self.clock = self.init_window()

        self.time_delta = 0

        self.space = pymunk.Space()
        self.space.gravity = 0, 0

        self.space = draw_wall(0, 0, 2000, 2000, self.space)
        self.space = draw_wall(2000 / 3, 2000 / 3, 2000 - 2000 / 3, 2000 - 2000 / 3, self.space)

        self.c = PlayerBoat(pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN, self)
        self.c2 = PlayerBoat('a', 'd', 'w', 's', self)

    def init_window(self):
        screen = pg.display.set_mode(self.size)
        clock = pg.time.Clock()
        return screen, clock

    def run(self):
        loop = True
        while loop:
            self.time_delta = self.clock.tick(60) / 1000.0

            self.update()
            events = pg.event.get()

            if not self.events(events):
                return 0

    def update(self):
        pg.display.flip()
        self.screen.fill('black')
        self.render_fps(str(int(self.clock.get_fps())), (0, 0))

    def events(self, events):

        self.c.update(events)
        self.c2.update(events)
        self.c.camera()

        for event in events:
            if event.type == pg.QUIT:
                return False

        return True

    def render_fps(self, text, pos):
        font = pg.font.Font(None, 30)
        render_text = font.render(text + ' FPS', True, pg.Color('green'))
        self.screen.blit(render_text, pos)


def draw_wall(x, y, x2, y2, space):
    c = [[x, y, x2, y], [x2, y, x2, y2], [x2, y2, x, y2], [x, y2, x, y]]
    for i in c:
        segment_shape = pymunk.Segment(
            space.static_body, (i[0], i[1]), (i[2], i[3]), 26)
        space.add(segment_shape)
        segment_shape.elasticity = 0.8
        segment_shape.friction = 1.0
    return space
