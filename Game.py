import sys
from Boat.BaseBoat import BaseBoat
from Boat.KeyboardController import KeyboardController
import pygame as pg
import pymunk
from Boat.Camera import Camera
import pymunk.pygame_util


class Game:
    def __init__(self,  space, surface, radarManager, boats, controllers, FPS, level, debug=False):
        self.space = space
        self.surface = surface
        self.boats = boats
        self.controllers = controllers
        self.radarManager = radarManager

        self.FPS =FPS        
        self.debug_mode = debug
        self.screen, self.clock = self.init_window()

        self.time_delta = 0

        self.draw_options = pymunk.pygame_util.DrawOptions(self.surface)
        self.camera = Camera()

        self.space.gravity = 0, 0

        self.level = level
        level.arrangeBoats(self.boats)

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
        infoboat = []
        for controller in self.controllers:
            controller.update()
        for boat in self.boats:
            infoboat.append(boat.get_info())
        lap = infoboat[0][0]
        infoboat[0] = infoboat[0] + ('Яхта игрока', )
        for i in range(1, len(infoboat)):
            infoboat[i] = infoboat[i] + ('Бот', )
        if lap == 78:
            sys.exit()
        self.radarManager.updateSensors()

        playerX, playerY = self.boats[0].get_position()
        cx, cy, scaling = self.camera.update(playerX-300, playerY-300, self.boats[0].get_velocity())
        if scaling < 0.5:
            scaling = 0.5
        self.space.step(1 /self.FPS)
        self.draw_options.transform = (
            pymunk.Transform.scaling(scaling)
            @ pymunk.Transform(tx=cx, ty=cy)
        )
        self.space.debug_draw(self.draw_options)
        for boat in self.boats:
            boat.updateImage(self.surface, cx, cy, scaling)
        self.render_fps(str(int(self.clock.get_fps())), (0, 0))
        self.render_lap(str(lap), (100, 0))
        self.render_speed(str(int(self.boats[0].get_velocity())), (300, 0))
        self.render_place(infoboat, (600, 0))
        pg.display.flip()
        self.screen.fill('black')
#        if self.level.get_next_checkpoint(playerX, playerY) == (0,0):
#            return False
        return True

    def events(self, events):
        for event in events:
            if event.type == pg.QUIT:
                return False
            for controller in self.controllers:
                controller.processEvent(event)   
        return True

    def render_fps(self, text, pos):
        font = pg.font.Font(None, 30)
        render_text = font.render(text + ' FPS', True, pg.Color('green'))
        self.screen.blit(render_text, pos)
    
    def render_lap(self, lap, pos):
        font = pg.font.Font(None, 30)
        render_text = font.render('Lap' + lap + '/4', True, pg.Color('red'))
        self.screen.blit(render_text, pos)
    
    def render_speed(self, speed, pos):
        font = pg.font.Font(None, 30)
        render_text = font.render('Speed' + speed, True, pg.Color('red'))
        self.screen.blit(render_text, pos)
    
    def render_place(self, infoboat, pos):
        font = pg.font.Font(None, 30)
        infoboat.sort(key=lambda x: (-x[0], -x[1], x[2]))
        for i in range(len(infoboat)):
            if infoboat[i][3] == 'Яхта игрока':
                render_text = font.render('Место' + str(i + 1), True, pg.Color('red'))
                self.screen.blit(render_text, pos)
