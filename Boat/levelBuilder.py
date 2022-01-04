from config import Collisiontypes
from pygame.colordict import THECOLORS
import pymunk


class SandBox:
    def draw_wall(self, x, y, x2, y2):
        c = [[x, y, x2, y], [x2, y, x2, y2], [x2, y2, x, y2], [x, y2, x, y]]
        for i in c:
            segment_shape = pymunk.Segment(
                self.space.static_body, (i[0], i[1]), (i[2], i[3]), 26
            )
            segment_shape.collision_type = Collisiontypes.SHORE
            self.space.add(segment_shape)
            segment_shape.elasticity = 0.8
            segment_shape.friction = 1.0
        self.tag = 0
        self.dict_checkpoint = dict()

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

        self.space = space
        WIDTH, HEIGHT = self.x * 42, self.y * 30
        self.draw_wall(0, 0, WIDTH, HEIGHT)
        self.draw_wall(self.x * 5, self.x * 5,
                       self.x * 11, HEIGHT - self.x * 5)
        self.draw_wall(self.x * 14, 0, self.x * 28, self.y * 12)
        self.draw_wall(self.x * 14, HEIGHT - self.y * 12, self.x * 28, HEIGHT)
        self.draw_wall(WIDTH - self.x * 11, self.x * 5,
                       WIDTH - self.x * 5, HEIGHT - self.x * 5)
        self.draw_wall(self.x * 11, self.y * 15,
                       WIDTH - self.x * 11, self.y * 15)

        self.draw_checkpoint(
            0, self.x * 5, self.x * 5,
            self.x * 5, 1)
        self.draw_checkpoint(
            self.x * 11, 0, self.x * 11,
            self.x * 5, 2)
        self.draw_checkpoint(
            self.x * 11, self.y * 12,
            self.x * 14, self.y * 12, 3)
        self.draw_checkpoint(
            self.x * 28, self.y * 12,
            self.x * 28, self.y * 15, 4)
        self.draw_checkpoint(
            self.x * 28, self.x * 5,
            self.x * 31, self.x * 5, 5)
        self.draw_checkpoint(
            WIDTH - self.x * 5, 0,
            WIDTH - self.x * 5, self.x * 5, 6)
        self.draw_checkpoint(
            WIDTH - self.x * 5, HEIGHT - self.x * 5,
            WIDTH, HEIGHT - self.x * 5, 7)
        self.draw_checkpoint(
            self.x * 31, HEIGHT - self.x * 5,
            self.x * 31, HEIGHT, 8)
        self.draw_checkpoint(
            self.x * 28, HEIGHT - self.y * 12,
            self.x * 31, HEIGHT - self.y * 12, 9)
        self.draw_checkpoint(
            self.x * 14, self.y * 15,
            self.x * 14, self.y * 18, 10)
        self.draw_checkpoint(
            self.x * 11, HEIGHT - self.x * 5,
            self.x * 14, HEIGHT - self.x * 5, 11)
        self.draw_checkpoint(
            self.x * 5, HEIGHT - self.x * 5,
            self.x * 5, HEIGHT, 12)
        # стартовый
        self.draw_checkpoint(
            0, self.y * 15, self.x * 5,
            self.y * 15, 0)
    
    def get_coords(self, checkpoint):
        c = [(self.x * 2.5, self.x * 2.5), (self.x * 12.5, self.x * 2.5), (self.x * 12.5, self.y * 13.5),
             (self.x * 29.5, self.y * 13.5), (self.x * 29.5, self.x * 2.5), (self.x * 39.5, self.x * 2.5),
             (self.x * 39.5, self.y * 30 - self.x * 2.5), (self.x * 29.5, self.y * 30 - self.x * 2.5),
             (self.x * 29.5, self.y * 16.5), (self.x * 12.5, self.y * 16.5), (self.x * 12.5, self.y * 30 - self.x * 2.5),
             (self.x * 2.5, self.y * 30 - self.x * 2.5), (self.x * 2.5, self.y * 15)]
        return c[checkpoint]
    
    def get_tag(self, shape):
        return self.dict_checkpoint[shape]

    def arrangeBoats(self, boats):
        c = [
            (self.x * 2, self.y * 18),
            (self.x * 3, self.y * 19),
            (self.x * 2, self.y * 20),
            (self.x * 3, self.y * 21),
            (self.x * 2, self.y * 22)]
        for i in range(len(boats)):
            boats[i].set_position(c[i][0], c[i][1])
