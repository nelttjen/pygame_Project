from collections import defaultdict
from Config import Collisiontypes
from pygame.colordict import THECOLORS
import pymunk


class SandBox2:
    def __init__(self):
        self.tag = 0
        self.dict_checkpoint = defaultdict()

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
        WIDTH, HEIGHT = self.x * 10, self.x * 10
        self.draw_wall(0, 0, WIDTH, HEIGHT)
        self.draw_wall(self.x * 5, 0,
                       WIDTH, self.x * 5)

        self.draw_checkpoint(
            0, self.x * 2.5, self.x * 5,
            self.x * 2.5, 1)
        self.draw_checkpoint(
            self.x * 7.5, self.x * 5, self.x * 7.5,
            HEIGHT, 0)
    
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

