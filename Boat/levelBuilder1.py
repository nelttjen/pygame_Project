from collections import defaultdict
import sys
from typing import Tuple

from pymunk import space
import Config
from pygame.colordict import THECOLORS
import pymunk
import pygame
from Utills.utils import load_image
from Boat.test_map_generator import Test_MapGenerator
from random import randrange
from math import pi

class LevelBuilder1:
    size: Tuple[int, int]

    def __init__(self, size, map_generator):
        self.coords = []
        self.dict_checkpoint = defaultdict()
        self.x, self.y = size
        self.m = 150
        self.load_images()
        
        cps, lp = map_generator.add_decorations()      
        self.map = map_generator.map
        self.track = map_generator.track
        self.lp = lp[1]
        self.cps = cps
        self.cp = self.cps[0][1]
        
        self.generate_image(self.map, self.track[self.lp][0], self.track[self.lp][1])
    
    def build(self, space):   
        self.space = space
        self.generate_pymunk_objects(self.map, self.cps, self.track)


    def draw_wall(self, x, y, x2, y2):
        segment_shape = pymunk.Segment(
            self.space.static_body, (x, y), (x2, y2), 4
        )
        segment_shape.collision_type = Config.Collisiontypes.SHORE
        self.space.add(segment_shape)
        segment_shape.elasticity = 0.8
        segment_shape.friction = 1.0
        segment_shape.color = THECOLORS["white"]

    colors = [THECOLORS["red"], THECOLORS["yellow"], THECOLORS["green"], THECOLORS["white"], THECOLORS["red"], THECOLORS["yellow"], THECOLORS["green"], THECOLORS["white"]]
    def draw_coord(self, xy, color):
        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        shape = pymunk.Circle(body, 20, xy)
        shape.sensor=True
        shape.color = color
        self.space.add(body, shape)

    def draw_checkpoint(self, x, y, x2, y2, tag):
        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

        segment_shape = pymunk.Segment(
            body, (x, y), (x2, y2), 14.0
        )
        segment_shape.collision_type = Config.Collisiontypes.CHECKPOINT
        segment_shape.sensor = True
        self.space.add(body, segment_shape)
        self.dict_checkpoint[segment_shape] = tag
        segment_shape.color = THECOLORS["red"]

    def generate_pymunk_objects(self, level, cp, track):
        for i in range(len(level)):
            for j in range(len(level[i])):
                if level[i][j] == '>' or level[i][j] == '<':
                    self.draw_wall(j * self.m + self.m / 2, i * self.m,
                                   j * self.m + self.m / 2, i * self.m + self.m)
                if level[i][j] == '^' or level[i][j] == 'v':
                    self.draw_wall(
                        j * self.m, i * self.m + self.m / 2, j * self.m + self.m,
                        i * self.m + self.m / 2)

                if level[i][j] == 'd' or level[i][j] == 'e':
                    self.draw_wall(
                        j * self.m, i * self.m + 0.5 * self.m, j * self.m + 0.25
                        * self.m, i * self.m + 0.6 * self.m)
                    self.draw_wall(
                        j * self.m + 0.25 * self.m, i * self.m + 0.6 * self.m, j
                        * self.m + 0.4 * self.m, i * self.m + 0.7 * self.m)
                    self.draw_wall(
                        j * self.m + 0.4 * self.m, i * self.m + 0.7 * self.m, j *
                        self.m + 0.5 * self.m, i * self.m + 1.0 * self.m)
                if level[i][j] == 'f' or level[i][j] == 'r':
                    self.draw_wall(
                        j * self.m + 1.0 * self.m, i * self.m + 0.5 * self.m, j *
                        self.m + 0.75 * self.m, i * self.m + 0.6 * self.m)
                    self.draw_wall(
                        j * self.m + 0.75 * self.m, i * self.m + 0.6 * self.m, j
                        * self.m + 0.6 * self.m, i * self.m + 0.7 * self.m)
                    self.draw_wall(
                        j * self.m + 0.6 * self.m, i * self.m + 0.7 * self.m, j *
                        self.m + 0.5 * self.m, i * self.m + 1.0 * self.m)
                if level[i][j] == 's' or level[i][j] == 'w':
                    self.draw_wall(
                        j * self.m + 0.5 * self.m, i * self.m, j * self.m + 0.6 *
                        self.m, i * self.m + 0.3 * self.m)
                    self.draw_wall(
                        j * self.m + 0.6 * self.m, i * self.m + 0.3 * self.m, j *
                        self.m + 0.75 * self.m, i * self.m + 0.4 * self.m)
                    self.draw_wall(
                        j * self.m + 0.75 * self.m, i * self.m + 0.4 * self.m, j
                        * self.m + 1.0 * self.m, i * self.m + 0.5 * self.m)
                if level[i][j] == 'a' or level[i][j] == 'q':
                    self.draw_wall(
                        j * self.m + 0.5 * self.m, i * self.m, j * self.m + 0.4 *
                        self.m, i * self.m + 0.3 * self.m)
                    self.draw_wall(
                        j * self.m + 0.4 * self.m, i * self.m + 0.3 * self.m, j *
                        self.m + 0.25 * self.m, i * self.m + 0.4 * self.m)
                    self.draw_wall(
                        j * self.m + 0.25 * self.m, i * self.m + 0.4 * self.m, j
                        * self.m, i * self.m + 0.5 * self.m)
        count = 0
        for i in cp:
            if i[1][0] == 1:
                self.draw_checkpoint((track[i[0]][0] + 1.5) * self.m,
                                     (track[i[0]][1] - 1) * self.m,
                                     (track[i[0]][0] + 1.5) * self.m,
                                     (track[i[0]][1] + 2) * self.m, count)
            if i[1][0] == -1:
                self.draw_checkpoint((track[i[0]][0] - 0.5) * self.m,
                                     (track[i[0]][1] - 1) * self.m,
                                     (track[i[0]][0] - 0.5) * self.m,
                                     (track[i[0]][1] + 2) * self.m, count)
            if i[1][1] == 1:
                self.draw_checkpoint((track[i[0]][0] + 2) * self.m,
                                     (track[i[0]][1] + 1.5) * self.m,
                                     (track[i[0]][0] - 1) * self.m,
                                     (track[i[0]][1] + 1.5) * self.m, count)
            if i[1][1] == -1:
                self.draw_checkpoint((track[i[0]][0] + 2) * self.m,
                                     (track[i[0]][1] - 0.5) * self.m,
                                     (track[i[0]][0] - 1) * self.m,
                                     (track[i[0]][1] - 0.5) * self.m, count)
            cxy = ((track[i[0]][0] + i[1][0]) * self.m + self.m // 2, (track[i[0]][1] + i[1][1]) * self.m + self.m // 2)
            self.coords.append(cxy)
            self.draw_coord(cxy, self.colors[count])
            count += 1

    def load_images(self):
        self.image = load_image("vertical2.png")
        self.image = pygame.transform.scale(self.image, (self.m, self.m))
        self.image2 = pygame.transform.rotate(self.image, 90)
        self.image11 = pygame.transform.rotate(self.image, 180)
        self.image22 = pygame.transform.rotate(self.image2, 180)

        self.image3 = load_image("turn2.png")
        self.image3 = pygame.transform.scale(self.image3, (self.m, self.m))
        self.image4 = pygame.transform.rotate(self.image3, 90)
        self.image5 = pygame.transform.rotate(self.image3, 180)
        self.image6 = pygame.transform.rotate(self.image3, 270)

        self.image33 = load_image("turn3.png")
        self.image33 = pygame.transform.scale(self.image33, (self.m, self.m))
        self.image43 = pygame.transform.rotate(self.image33, 90)
        self.image53 = pygame.transform.rotate(self.image33, 180)
        self.image63 = pygame.transform.rotate(self.image33, 270)

        self.imageW = load_image("water.png")
        self.imageW = pygame.transform.scale(self.imageW, (self.m, self.m))

        self.imageO = load_image("ot.png")
        self.imageO = pygame.transform.scale(self.imageO, (self.m, self.m))

        self.imageK = load_image("kol.png")
        self.imageK = pygame.transform.scale(self.imageK, (self.m, self.m))

        self.imageS = load_image("start.png")
        self.imageS = pygame.transform.scale(self.imageS, (self.m, self.m))

    def generate_image(self, level, x, y):
        self.size = self.m * len(level), self.m * len(level[0])
        #self.size = 920, 700
        count = 0
        self.merged_image = pygame.Surface(self.size)
        for i in range(len(level)):
            for j in range(len(level[i])):
                if level[i][j] == '>':
                    self.merged_image.blit(
                        self.image2, (j * self.m, i * self.m))
                if level[i][j] == '<':
                    self.merged_image.blit(
                        self.image22, (j * self.m, i * self.m))
                if level[i][j] == '^':
                    self.merged_image.blit(
                        self.image11, (j * self.m, i * self.m))
                if level[i][j] == 'v':
                    self.merged_image.blit(
                        self.image, (j * self.m, i * self.m))

                if level[i][j] == 'd':
                    self.merged_image.blit(
                        self.image6, (j * self.m, i * self.m))
                if level[i][j] == 'e':
                    self.merged_image.blit(
                        self.image63, (j * self.m, i * self.m))
                if level[i][j] == 'f':
                    self.merged_image.blit(
                        self.image3, (j * self.m, i * self.m))
                if level[i][j] == 'r':
                    self.merged_image.blit(
                        self.image33, (j * self.m, i * self.m))
                if level[i][j] == 's':
                    self.merged_image.blit(
                        self.image4, (j * self.m, i * self.m))
                if level[i][j] == 'w':
                    self.merged_image.blit(
                        self.image43, (j * self.m, i * self.m))
                if level[i][j] == 'a':
                    self.merged_image.blit(
                        self.image5, (j * self.m, i * self.m))
                if level[i][j] == 'q':
                    self.merged_image.blit(
                        self.image53, (j * self.m, i * self.m))

                if level[i][j] == 1 or level[i][j] == 'c' or level[i][j] == 'x':
                    self.merged_image.blit(
                        self.imageW, (j * self.m, i * self.m))
                if level[i][j] == 8 or level[i][j] == 0:
                    a = randrange(100)
                    if a > 20:
                        self.merged_image.blit(
                            self.imageO, (j * self.m, i * self.m))
                    else:
                        self.merged_image.blit(
                            self.imageK, (j * self.m, i * self.m))
        if self.cp[1] == 1 or self.cp[1] == 1:
            self.merged_image.blit(self.imageS, (x * self.m, (y+1) * self.m))
        else:
            self.merged_image.blit(self.imageS, ((x+1) * self.m, y * self.m))
    
    def get_image(self):
        return self.merged_image

    def get_level(self):
        return self.merged_image

    def get_coords(self, checkpoint):
        return self.coords[checkpoint]

    def get_checkpoint_info(self, shape):
        return self.dict_checkpoint[shape], (
            self.dict_checkpoint[shape] + 1) % len(self.dict_checkpoint)

    def arrangeBoats(self, boats):
        if self.cp[1] == 1:
            c = [
                [self.track[self.lp][0] * self.m, (self.track[self.lp][1]+2) * self.m],
                [self.track[self.lp][0] * self.m + 120, (self.track[self.lp][1]+2) * self.m - 100],
                [self.track[self.lp][0] * self.m, (self.track[self.lp][1]+2) * self.m - 200],
                [self.track[self.lp][0] * self.m + 120, (self.track[self.lp][1]+2) * self.m - 300],
                [self.track[self.lp][0] * self.m, (self.track[self.lp][1]+2) * self.m - 400]]
            for i in range(len(boats)):
                boats[i].set_position(c[i][0], c[i][1], 0.5)
        if self.cp[1] == -1:
            c = [
                [self.track[self.lp][0] * self.m, (self.track[self.lp][1]+2) * self.m],
                [self.track[self.lp][0] * self.m + 120, (self.track[self.lp][1]+2) * self.m + 100],
                [self.track[self.lp][0] * self.m, (self.track[self.lp][1]+2) * self.m + 200],
                [self.track[self.lp][0] * self.m + 120, (self.track[self.lp][1]+2) * self.m + 300],
                [self.track[self.lp][0] * self.m, (self.track[self.lp][1]+2) * self.m + 400]]
            for i in range(len(boats)):
                boats[i].set_position(c[i][0], c[i][1], 1.5)
        if self.cp[0] == -1:
            c = [
                [self.track[self.lp][0] * self.m, (self.track[self.lp][1]) * self.m],
                [self.track[self.lp][0] * self.m + 100, (self.track[self.lp][1]) * self.m + 120],
                [self.track[self.lp][0] * self.m + 200, (self.track[self.lp][1]) * self.m],
                [self.track[self.lp][0] * self.m + 300, (self.track[self.lp][1]) * self.m + 120],
                [self.track[self.lp][0] * self.m + 400, (self.track[self.lp][1]) * self.m]]
            for i in range(len(boats)):
                boats[i].set_position(c[i][0], c[i][1], 1)
        if self.cp[0] == 1:
            c = [
                [self.track[self.lp][0] * self.m, (self.track[self.lp][1]) * self.m],
                [self.track[self.lp][0] * self.m - 100, (self.track[self.lp][1]) * self.m + 120],
                [self.track[self.lp][0] * self.m - 200, (self.track[self.lp][1]) * self.m],
                [self.track[self.lp][0] * self.m - 300, (self.track[self.lp][1]) * self.m + 120],
                [self.track[self.lp][0] * self.m - 400, (self.track[self.lp][1]) * self.m]]
            for i in range(len(boats)):
                boats[i].set_position(c[i][0], c[i][1], 0)
