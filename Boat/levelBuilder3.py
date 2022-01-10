from collections import defaultdict
from config import Collisiontypes
from pygame.colordict import THECOLORS
import pymunk
import pygame
from Utills.utils import load_image

class SandBox3:
    def __init__(self):
        self.tag = 0
        self.dict_checkpoint = defaultdict()

    def draw_wall(self, x, y, x2, y2):
        segment_shape = pymunk.Segment(
            self.space.static_body, (x, y), (x2, y2), 4
        )
        segment_shape.collision_type = Collisiontypes.SHORE
        self.space.add(segment_shape)
        segment_shape.elasticity = 0.8
        segment_shape.friction = 1.0

    def draw_checkpoint(self, x, y, x2, y2, tag):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

        segment_shape = pymunk.Segment(
            self.body, (x, y), (x2, y2), 0.0
        )
        segment_shape.collision_type = Collisiontypes.CHECKPOINT
        segment_shape.sensor = True
        self.space.add(self.body, segment_shape)
        self.dict_checkpoint[segment_shape] = tag

    def build(self, space, size):
        self.x, self.y = size
        self.m = self.x * 3
        self.load_images()
        
        level = [["*", "*", "к", "*", "*", "*", "*", "*", "*", "*", "*"],
                 ["*", "*", "*", "2", "-", "-", "-", "-", "1", "*", "*"],
                 ["*", "2", "-", "4", "в", "в", "в", "в", "3", "1", "*"],
                 ["*", "|", "в", "в", "в", "в", "в", "в", "в", "|", "*"],
                 ["*", "|", "в", "2", "-", "-", "1", "в", "в", "|", "*"],
                 ["*", "|", "в", "|", "*", "2", "4", "в", "2", "4", "*"],
                 ["*", "|", "в", "3", "-", "4", "в", "2", "4", "*", "*"],
                 ["*", "|", "в", "в", "в", "в", "2", "4", "*", "*", "к"],
                 ["*", "3", "-", "-", "-", "-", "4", "*", "к", "*", "*"],
                 ["к", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*"]]
        self.space = space
        for i in range(len(level)):
            for j in range(len(level[i])):
                if level[i][j] == '-':
                    self.draw_wall(j * self.m, i * self.m + self.m / 2, j * self.m + self.m, i * self.m + self.m / 2)
                if level[i][j] == '|':
                    self.draw_wall(j * self.m + self.m / 2, i * self.m, j * self.m + self.m / 2, i * self.m + self.m)
                if level[i][j] == '1':
                    self.draw_wall(j * self.m, i * self.m + 0.5 * self.m, j * self.m + 0.25 * self.m, i * self.m + 0.6 * self.m)
                    self.draw_wall(j * self.m + 0.25 * self.m, i * self.m + 0.6 * self.m, j * self.m + 0.4 * self.m, i * self.m + 0.7 * self.m)
                    self.draw_wall(j * self.m + 0.4 * self.m, i * self.m + 0.7 * self.m, j * self.m + 0.5 * self.m, i * self.m + 1.0 * self.m)
                if level[i][j] == '2':
                    self.draw_wall(j * self.m + 1.0 * self.m, i * self.m + 0.5 * self.m, j * self.m + 0.75 * self.m, i * self.m + 0.6 * self.m)
                    self.draw_wall(j * self.m + 0.75 * self.m, i * self.m + 0.6 * self.m, j * self.m + 0.6 * self.m, i * self.m + 0.7 * self.m)
                    self.draw_wall(j * self.m + 0.6 * self.m, i * self.m + 0.7 * self.m, j * self.m + 0.5 * self.m, i * self.m + 1.0 * self.m)
                if level[i][j] == '3':
                    self.draw_wall(j * self.m + 0.5 * self.m, i * self.m, j * self.m + 0.6 * self.m, i * self.m + 0.3 * self.m)
                    self.draw_wall(j * self.m + 0.6 * self.m, i * self.m + 0.3 * self.m, j * self.m + 0.75 * self.m, i * self.m + 0.4 * self.m)
                    self.draw_wall(j * self.m + 0.75 * self.m, i * self.m + 0.4 * self.m, j * self.m + 1.0 * self.m, i * self.m + 0.5 * self.m)
                if level[i][j] == '4':
                    self.draw_wall(j * self.m + 0.5 * self.m, i * self.m, j * self.m + 0.4 * self.m, i * self.m + 0.3 * self.m)
                    self.draw_wall(j * self.m + 0.4 * self.m, i * self.m + 0.3 * self.m, j * self.m + 0.25 * self.m, i * self.m + 0.4 * self.m)
                    self.draw_wall(j * self.m + 0.25 * self.m, i * self.m + 0.4 * self.m, j * self.m, i * self.m + 0.5 * self.m)
        self.generate_image(level)
        
    
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
    
    def generate_image(self, level):
        size = self.m * len(level), self.m * len(level[0])
        self.merged_image = pygame.display.set_mode(size)
        for i in range(len(level)):
            for j in range(len(level[i])):
                if level[i][j] == '-':
                    if level[i+1][j] == 'в':
                        self.merged_image.blit(self.image, (j * self.m, i * self.m))
                    else:
                        self.merged_image.blit(self.image11, (j * self.m, i * self.m))
                if level[i][j] == '|':
                    if level[i][j + 1] == 'в':
                        self.merged_image.blit(self.image2, (j * self.m, i * self.m))
                    else:
                        self.merged_image.blit(self.image22, (j * self.m, i * self.m))
                if level[i][j] == '1':
                    if level[i][j + 1] == '*' or level[i][j - 1] == 'в':
                        self.merged_image.blit(self.image6, (j * self.m, i * self.m))
                    else:
                        self.merged_image.blit(self.image63, (j * self.m, i * self.m))
                if level[i][j] == '2':
                    if level[i][j + 1] == 'в' or level[i][j - 1] == '*':
                        self.merged_image.blit(self.image3, (j * self.m, i * self.m))
                    else:
                        self.merged_image.blit(self.image33, (j * self.m, i * self.m))
                if level[i][j] == '3':
                    if level[i][j + 1] == 'в' or level[i][j - 1] == '*':
                        self.merged_image.blit(self.image4, (j * self.m, i * self.m))
                    else:
                        self.merged_image.blit(self.image43, (j * self.m, i * self.m))
                if level[i][j] == '4':
                    if level[i][j + 1] == '*' or level[i][j - 1] == 'в':
                        self.merged_image.blit(self.image5, (j * self.m, i * self.m))
                    else:
                        self.merged_image.blit(self.image53, (j * self.m, i * self.m))
                if level[i][j] == 'в':
                    self.merged_image.blit(self.imageW, (j * self.m, i * self.m))
                if level[i][j] == '*':
                    self.merged_image.blit(self.imageO, (j * self.m, i * self.m))
                if level[i][j] == 'к':
                    self.merged_image.blit(self.imageK, (j * self.m, i * self.m))
        pygame.image.save(self.merged_image,'data\\temp.png')
    def get_level(self):
        return self.merged_image
    
    def get_coords(self, checkpoint):
        c = [(self.x * 8.75, self.x * 7.5), (self.x * 2.5, self.x * 1.25)]
        return c[checkpoint]
    
    def get_checkpoint_info(self, shape):
        return self.dict_checkpoint[shape], (self.dict_checkpoint[shape] + 1) % 2

    def arrangeBoats(self, boats):
        c = [
            (self.x * 9, self.x * 8),
            (self.x * 8, self.x * 9),
            (self.x * 7, self.x * 9),
            (self.x * 6, self.x * 8),
            (self.x * 5, self.x * 9)]
        for i in range(len(boats)):
            boats[i].set_position(c[i][0], c[i][1])

