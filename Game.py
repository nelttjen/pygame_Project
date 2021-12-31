import pygame as pg
import pymunk
from Boat.Camera import Camera
import pymunk.pygame_util
from Boat.PlayerBoat import PlayerBoat

class Game:
    def __init__(self,  space, surface, radarManager, boats, FPS, level, debug=False):
        self.space = space
        self.surface = surface
        self.boats = boats
        self.radarManager = radarManager

        self.FPS =FPS        
        self.debug_mode = debug
        self.screen, self.clock = self.init_window()

        self.time_delta = 0

        self.draw_options = pymunk.pygame_util.DrawOptions(self.surface)
        self.camera = Camera()

        self.space.gravity = 0, 0
  
        self.level = level
        level.build(self.space, (100, 73))
        level.arrangeBoats(boats)
        self.player = self.boats.pop(0)

    def init_window(self):
        screen = pg.display.set_mode(self.surface.get_size())
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
        playerX, playerY, playerVelocity = self.player.update()
        for boat in self.boats:
            boat.update(self.level)
        self.radarManager.updateSensors()

        cx, cy, scaling = self.camera.update(playerX-300, playerY-300, playerVelocity)
        self.space.step(1 /self.FPS)
        self.draw_options.transform = (
            pymunk.Transform.scaling(scaling)
            @ pymunk.Transform(tx=cx, ty=cy)
        )
        self.space.debug_draw(self.draw_options)
        self.player.updateImage(self.surface, cx, cy, scaling)
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
            self.player.processEvent(event)
        return True

    def render_fps(self, text, pos):
        font = pg.font.Font(None, 30)
        render_text = font.render(text + ' FPS', True, pg.Color('green'))
        self.screen.blit(render_text, pos)
