import pymunk

class SandBox:
    def draw_wall(self, x, y, x2, y2):
        c = [[x, y, x2, y], [x2, y, x2, y2], [x2, y2, x, y2], [x, y2, x, y]]
        for i in c:
            segment_shape = pymunk.Segment(
                self.space.static_body, (i[0], i[1]), (i[2], i[3]), 26
            )
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
    
    def get_coords(self, checkpoint):
        c = [(self.x * 2.5, self.x * 2.5), (self.x * 12.5, self.x * 2.5), (self.x * 12.5, self.y * 13.5),
             (self.x * 29.5, self.y * 13.5), (self.x * 29.5, self.x * 2.5), (self.x * 39.5, self.x * 2.5),
             (self.x * 39.5, self.y * 30 - self.x * 2.5), (self.x * 29.5, self.y * 30 - self.x * 2.5),
             (self.x * 29.5, self.y * 16.5), (self.x * 12.5, self.y * 16.5), (self.x * 12.5, self.y * 30 - self.x * 2.5),
             (self.x * 2.5, self.y * 30 - self.x * 2.5), (self.x * 2.5, self.y * 15)]
        if checkpoint == 0:
            return c[checkpoint]
        return c[checkpoint - 1]
    
    def get_checkpoint_info(self, shape):
        return self.dict_checkpoint[shape], (self.dict_checkpoint[shape] + 1) % 13

    def arrangeBoats(self, boats):
        boats[0].set_position(50, self.y * 27)
        boats[1].set_position(50, self.y * 28)