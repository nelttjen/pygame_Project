import sys
import pymunk
import pymunk.pygame_util
import pygame as pg

from typing import List

import Config
from Boat.Camera import Camera
from Boat.BaseBoat import BaseBoat
from Utills.utils import load_image


class MenuError(Exception):
    pass


class Menu(pg.sprite.Sprite):
    def __init__(self, image, x, y, group):
        super().__init__(group)
        self.image = pg.transform.scale(load_image(image), (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        if args and args[0].type == pg.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and args[0].button == 1:
            raise MenuError


def init_window():
    screen = pg.display.set_mode((Config.Screen.WIDTH, Config.Screen.HEIGHT))
    clock = pg.time.Clock()
    return screen, clock


class Game:
    camera: Camera
    boats: List[BaseBoat]

    def __init__(
            self,
            space,
            surface,
            radarManager,
            boats,
            controllers,
            FPS,
            level,
            debug=False):
        self.space = space
        self.surface = surface
        self.boats = boats
        self.controllers = controllers
        self.radarManager = radarManager

        self.FPS = FPS
        self.debug_mode = debug
        self.screen, self.clock = init_window()

        self.time_delta = 0

        self.draw_options = pymunk.pygame_util.DrawOptions(self.surface)
        self.camera = Camera(
            level.size, (Config.Screen.WIDTH, Config.Screen.HEIGHT))

        self.space.gravity = 0, 0

        self.level = level
        level.arrangeBoats(self.boats)

        self.a = level.get_image()

        self.max_speed = 0
        self.place = 0
        self.points = 0
        self.name = ''

        self.all_sprites = pg.sprite.Group()
        Menu(
            "menu.png",
            self.screen.get_width() // 2 - 80,
            self.screen.get_height() // 2 + 70,
            self.all_sprites)

    def run(self):
        for boat in self.boats:
            boat.update(0, 0)
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
        infoboat[0] = infoboat[0] + ('Яхта игрока',)
        for i in range(1, len(infoboat)):
            infoboat[i] = infoboat[i] + ('Бот',)
        self.radarManager.update_sensors()

        playerX, playerY = self.boats[0].get_position()
        cxy, wxy, scaling = self.camera.update(
            playerX, playerY, self.boats[0].get_velocity())

        self.space.step(1 / self.FPS)
        if Config.Screen.DEBUG:
            self.draw_options.transform = (
                pymunk.Transform.scaling(scaling)
                @ pymunk.Transform(tx=-cxy[0], ty=-cxy[1])
            )

        cropped_image = self.a.subsurface(cxy[0], cxy[1], wxy[0], wxy[1])
        cropped_image = pg.transform.scale(
            cropped_image, self.camera.screen_size)
        self.screen.blit(cropped_image, (0, 0))
        if Config.Screen.DEBUG:
            self.space.debug_draw(self.draw_options)

        for boat in self.boats:
            boat.update_image(self.surface, cxy[0], cxy[1], scaling)
        self.render_fps(str(int(self.clock.get_fps())), (0, 0))
        self.render_lap(str(lap), (100, 0))
        self.render_speed(str(int(self.boats[0].get_velocity())), (300, 0))
        self.render_place(infoboat, (600, 0))
        if lap == 5:
            self.finish(self.place)
        if self.boats[0].get_velocity() > self.max_speed:
            self.max_speed = self.boats[0].get_velocity()
        pg.display.flip()

        return True

    def events(self, events):
        for event in events:
            if event.type == pg.QUIT:
                return False
            for controller in self.controllers:
                controller.process_event(event)
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
                self.place = i + 1
                render_text = font.render(
                    'Место' + str(i + 1), True, pg.Color('red'))
                self.screen.blit(render_text, pos)

    def finish(self, place):
        points = {1: 16000, 2: 12000, 3: 8000, 4: 4000}
        a = pg.transform.scale(load_image("finish.png"), (800, 400))
        running = True
        self.name = ''
        self.points = int(self.max_speed) * 6 + points[place]
        font = pg.font.Font(None, 40)
        while running:
            events = pg.event.get()
            self.screen.blit(
                a,
                (self.screen.get_width() //
                 2 -
                 400,
                 self.screen.get_height() //
                 2 -
                 200))
            self.all_sprites.draw(self.screen)
            render_text = font.render('За место: ' +
                                      str(points[place]), True, (60, 80, 200))
            self.screen.blit(render_text,
                             (self.screen.get_width() // 2 - 150,
                              self.screen.get_height() // 2 - 90))
            render_text = font.render(
                'За скорость: ' + str(int(self.max_speed) * 6), True, (60, 80, 200))
            self.screen.blit(render_text,
                             (self.screen.get_width() // 2 - 150,
                              self.screen.get_height() // 2 - 45))
            render_text = font.render('Итого: ' +
                                      str(self.points), True, (60, 80, 200))
            self.screen.blit(
                render_text,
                (self.screen.get_width() // 2 - 150,
                 self.screen.get_height() // 2))
            render_text = font.render(
                'Ваше имя: ' + self.name, True, (60, 80, 200))
            self.screen.blit(render_text,
                             (self.screen.get_width() // 2 - 150,
                              self.screen.get_height() // 2 + 45))
            for event in events:
                self.all_sprites.update(event)
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.unicode == '\x08':
                        self.name = self.name[:-1]
                    elif len(self.name) < 8:
                        self.name += event.unicode
            pg.display.flip()
