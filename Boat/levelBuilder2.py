from collections import defaultdict
from config import Collisiontypes
from pygame.colordict import THECOLORS
import pymunk
from Utills.FieldGenerator import FiledGenerator


class SandBox2:
    def __init__(self):
        self.tag = 0
        self.dict_checkpoint = defaultdict()
        self.dx, self.dy = 70, 70
        self.level = FiledGenerator(self.dx, self.dy, 8, 16)

    def draw_wall(self, x, y, x2, y2, width=30):
        c = [[x, y, x2, y], [x2, y, x2, y2], [x2, y2, x, y2], [x, y2, x, y]]
        for i in c:
            segment_shape = pymunk.Segment(
                self.space.static_body, (i[0], i[1]), (i[2], i[3]), width
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
        self.space = space
        self.x, self.y = size
        self.level.generate_new()
        x, y = 0, 0
        x2, y2 = -3, 3
        x3, y3 = -5, 5
        x4, y4 = -8, 8
        schematic = self.level.get_field()
        for i, cell in enumerate(schematic):
            self.draw_wall(x * 150, y * 150, (x + cell[0]) * 150, (y + cell[1]) * 150)
            self.draw_wall(x2 * 150, y2 * 150, (x2 + cell[0]) * 150, (y2 + cell[1]) * 150)
            self.draw_wall(x3 * 150, y3 * 150, (x3 + cell[0]) * 150, (y3 + cell[1]) * 150)
            self.draw_wall(x4 * 150, y4 * 150, (x4 + cell[0]) * 150, (y4 + cell[1]) * 150)
            x += cell[0]
            y += cell[1]
            x2 += cell[0]
            y2 += cell[1]
            x3 += cell[0]
            y3 += cell[1]
            x4 += cell[0]
            y4 += cell[1]
        self.draw_left_corner()
        self.draw_right_corner(x4, y4, x3, y3)

        # schematic2 = self.level.get_back_field()
        # x, y = self.dx, self.dy
        # x2, y2 = self.dx - 3, self.dy + 3
        # for i, cell in enumerate(schematic2):
        #     self.draw_wall(x * 150, y * 150, (x - cell[0]) * 150, (y - cell[1]) * 150)
        #     self.draw_wall(x2 * 150, y2 * 150, (x2 - cell[0]) * 150, (y2 - cell[1]) * 150)
        #     x -= cell[0]
        #     y -= cell[1]
        #     x2 -= cell[0]
        #     y2 -= cell[1]

    def draw_left_corner(self):
        self.draw_wall(-8 * 150, 8 * 150, -8 * 150, 0)
        self.draw_wall(-8 * 150, 0, 0, 0)
        self.draw_wall(-5 * 150, 5 * 150, -5 * 150, 3 * 150)
        self.draw_wall(-5 * 150, 3 * 150, -3 * 150, 3 * 150)

    def draw_right_corner(self, x4, y4, x3, y3):
        self.draw_wall(x4 * 150, y4 * 150, (x4 + 8) * 150, y4 * 150)
        self.draw_wall((x4 + 8) * 150, y4 * 150, (x4 + 8) * 150, (y4 - 8) * 150)
        self.draw_wall(x3 * 150, y3 * 150, (x3 + 2) * 150, y3 * 150)
        self.draw_wall((x3 + 2) * 150, y3 * 150, (x3 + 2) * 150, (y3 - 2) * 150)

    def get_coords(self, checkpoint):
        c = [(self.x * 8.75, self.x * 7.5), (self.x * 2.5, self.x * 1.25)]
        return c[checkpoint]
    
    def get_checkpoint_info(self, shape):
        return self.dict_checkpoint[shape], (self.dict_checkpoint[shape] + 1) % 2

    def arrangeBoats(self, boats):
        x, y = -7, 7
        for i in range(len(boats)):
            boats[i].set_position((x + i) * 150, y * 150)

