from collections import defaultdict
from config import Collisiontypes, Tile
from pygame.colordict import THECOLORS
import pymunk
from Utills.FieldGenerator import FiledGenerator


class SandBox2:
    def __init__(self):
        self.tag = 0
        self.dict_checkpoint = defaultdict()
        self.dx, self.dy = 70, 70
        self.level = FiledGenerator(self.dx, self.dy, 8, 16)
        self.tile = Tile.TILE

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

    def draw_checkpoint(self, x, y, x2, y2, tag, width=0.0):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

        segment_shape = pymunk.Segment(
            self.body, (x, y), (x2, y2), width
        )
        segment_shape.collision_type = Collisiontypes.CHECKPOINT
        segment_shape.sensor = True
        self.space.add(self.body, segment_shape)
        self.dict_checkpoint[segment_shape] = tag

    # def build(self, space, size):
    #     self.space = space
    #     self.x, self.y = size
    #     self.level.generate_new()
    #     x, y = 0, 0
    #     x2, y2 = -3, 3
    #     x3, y3 = -5, 5
    #     x4, y4 = -8, 8
    #     schematic = self.level.get_field()
    #     schematic2 = self.level.get_back_field()
    #     for i, cell in enumerate(schematic):
    #         self.draw_2_walls(x, y, x2, y2, cell)
    #         self.draw_2_walls(x3, y3, x4, y4, cell)
    #         x += cell[0]
    #         y += cell[1]
    #         x2 += cell[0]
    #         y2 += cell[1]
    #         x3 += cell[0]
    #         y3 += cell[1]
    #         x4 += cell[0]
    #         y4 += cell[1]
    #     self.draw_left_corner()
    #     self.draw_right_corner(x4, y4, x3, y3)
    def build(self, space, size):
        self.checkpoints = []
        self.space = space
        self.x, self.y = size
        self.level.generate_new()
        x, y = 0, 0
        x2, y2 = -3, 3
        schematic = self.level.get_field()
        schematic2 = self.level.get_back_field()
        for i, cell in enumerate(schematic):
            self.draw_2_walls(x, y, x2, y2, cell)
            x += cell[0]
            y += cell[1]
            x2 += cell[0]
            y2 += cell[1]
        dv = 0
        if schematic2[0][2] == 'left':
            dv = schematic2[0][0]
            schematic2[1][1] += dv
            schematic2.pop(0)
        self.draw_left_corner(dv)
        self.draw_right_corner(x2, y2, x, y)
        x += 2
        y -= 2
        x2 += 8
        y2 -= 8
        for i, cell in enumerate(schematic2):
            self.draw_2_walls(x, y, x2, y2, cell)
            x -= cell[0]
            y -= cell[1]
            x2 -= cell[0]
            y2 -= cell[1]
        checkp = 0
        print(schematic)
        x, y = -3, 3
        temp = []
        if schematic[-1][2] == 'right':
            temp = schematic[-1]
            schematic.pop(-1)
        for i, cell in enumerate(schematic):
            if cell[2] == 'right':
                x += cell[0]
                dx, dy = x, y
                dx2, dy2 = x, y - 3
            else:
                y += cell[1]
                dx, dy = x, y - 3
                dx2, dy2 = x + 3, y - 3
            checkp = self.draw_and_add_checkpoint(dx, dy, dx2, dy2, cell, checkp)
        if temp:
            x += temp[0]
        dx, dy = x + 5, y
        dx2, dy2 = x + 5, y - 3
        self.draw_checkpoint(dx * self.tile, dy * self.tile, dx2 * self.tile, dy2 * self.tile, checkp, 30)
        self.checkpoints.append(Checkpoint(dx, dy, dx2, dy2, self.tile, 'right', checkp))
        checkp += 1
        x += 5
        y -= 5
        temp = []
        if schematic2[-1][2] == 'left':
            temp = schematic2[-1]
            schematic2.pop(-1)
        for i, cell in enumerate(schematic2):
            if cell[2] == 'left':
                x -= cell[0]
                dx, dy = x + 3, y
                dx2, dy2 = x + 3, y - 3
            else:
                y -= cell[1]
                dx, dy = x + 3, y
                dx2, dy2 = x, y
            checkp = self.draw_and_add_checkpoint(dx, dy, dx2, dy2, cell, checkp)
        if temp:
            x -= temp[0]
        dx, dy = x - 2 - dv, y
        dx2, dy2 = x - 2 - dv, y - 3
        self.draw_checkpoint(dx * self.tile, dy * self.tile, dx2 * self.tile, dy2 * self.tile, checkp, 30)
        self.checkpoints.append(Checkpoint(dx, dy, dx2, dy2, self.tile, 'left', checkp))
        checkp += 1
        dx, dy, dx2, dy2 = -3, 0, 0, 0
        self.draw_checkpoint(dx * self.tile, dy * self.tile, dx2 * self.tile, dy2 * self.tile, checkp, 30)
        self.checkpoints.append(Checkpoint(dx, dy, dx2, dy2, self.tile, 'down', checkp))
        checkp += 1

    def draw_and_add_checkpoint(self, dx, dy, dx2, dy2, cell, cp):
        self.draw_checkpoint(dx * self.tile, dy * self.tile, dx2 * self.tile, dy2 * self.tile, cp, 30)
        self.checkpoints.append(Checkpoint(dx, dy, dx2, dy2, self.tile, cell[2], cp))
        return cp + 1

    def draw_2_walls(self, x1, y1, x2, y2, cell):
        direction = 1
        if cell[2] in ['left', 'up']:
            direction *= -1
        self.draw_wall(x1 * self.tile, y1 * self.tile, (x1 + cell[0] * direction) * self.tile, (y1 + cell[1] * direction) * self.tile)
        self.draw_wall(x2 * self.tile, y2 * self.tile, (x2 + cell[0] * direction) * self.tile, (y2 + cell[1] * direction) * self.tile)

    def draw_left_corner(self, dv):
        self.draw_wall(-3 * self.tile, 3 * self.tile, -3 * self.tile, (-5 - dv) * self.tile)
        self.draw_wall(-3 * self.tile, (-5 - dv) * self.tile, (5 + dv) * self.tile, (-5 - dv) * self.tile)
        self.draw_wall(0, 0, 0, (-2 - dv) * self.tile)
        self.draw_wall(0, (-2 - dv) * self.tile, (2 + dv) * self.tile, (-2 - dv) * self.tile)

    def draw_right_corner(self, x4, y4, x3, y3):
        self.draw_wall(x4 * self.tile, y4 * self.tile, (x4 + 8) * self.tile, y4 * self.tile)
        self.draw_wall((x4 + 8) * self.tile, y4 * self.tile, (x4 + 8) * self.tile, (y4 - 8) * self.tile)
        self.draw_wall(x3 * self.tile, y3 * self.tile, (x3 + 2) * self.tile, y3 * self.tile)
        self.draw_wall((x3 + 2) * self.tile, y3 * self.tile, (x3 + 2) * self.tile, (y3 - 2) * self.tile)

    def get_coords(self, checkpoint):
        c = [(self.x * 8.75, self.x * 7.5), (self.x * 2.5, self.x * 1.25)]
        return c[checkpoint]
    
    def get_checkpoint_info(self, shape):
        return self.dict_checkpoint[shape], (self.dict_checkpoint[shape] + 1) % 2

    def arrangeBoats(self, boats):
        x, y = -20, -10
        for i in range(len(boats)):
            boats[i].set_position((x + i) * self.tile, y * self.tile)


class Checkpoint:
    def __init__(self, x, y, x2, y2, tile, direction, c_id):
        self.x, self.y, self.x2, self.y2 = x, y, x2, y2
        self.tile = tile
        self.c_id = c_id
        self.direction = direction
        if self.direction in ['left', 'right']:
            self.center = x * self.tile, (y + (y2 - y) / 2) * self.tile
        else:
            self.center = (x + (x2 - x) / 2) * self.tile, y * self.tile

    def get_center(self):
        return self.center

    def get_id(self):
        return self.c_id

    def get_info(self):
        return self.x, self.y, self.x2, self.y2, self.center, self.direction, self.c_id
