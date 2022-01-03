from config import Collisiontypes
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

    def build(self, space, size):
        self.x, self.y = size

        self.space = space
        WIDTH, HEIGHT = self.x * 40, self.y * 30
        self.draw_wall(0, 0, WIDTH, HEIGHT)
        self.draw_wall(0, 0, self.x * 10, HEIGHT - self.y * 4)
        self.draw_wall(self.x * 10 + self.y * 4, self.y * 4, self.x * 20 + self.y * 4, HEIGHT)
        self.draw_wall(self.x * 20 + self.y * 8, 0, WIDTH, HEIGHT - self.y * 4)
    
    def get_next_checkpoint(self, pos_x, pos_y):
        if pos_x < self.x * 10:
            return self.x * 10, self.y * 37
        elif pos_x < self.x * 13 and pos_y > self.y * 4:
            return self.x * 11, self.y * 2
        elif pos_x < self.x * 20 + self.y * 4:
            return self.x * 20 + self.y * 6, self.y * 2
        elif pos_y < self.y * 26:
            return self.x * 20 + self.y * 6, self.y * 28
        else:
            if pos_x > self.x * 38:
                return 0, 0
            return self.x * 36 + self.y * 6, self.y * 28

    def arrangeBoats(self, boats):
        boats[0].set_position(50, self.y * 27)
        boats[1].set_position(50, self.y * 28)