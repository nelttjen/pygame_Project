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

    def build(self, space):
        self.space = space
        WIDTH, HEIGHT = 4000, 2000
        self.draw_wall(0, 0, WIDTH, HEIGHT)
        self.draw_wall(0, 0, (WIDTH - 600) // 3, HEIGHT - 300)
        self.draw_wall((WIDTH - 600) // 3 + 300, 300, (WIDTH - 600) // 3 * 2 + 300, HEIGHT)
        self.draw_wall((WIDTH - 600) // 3 * 2 + 600, 0, WIDTH, HEIGHT - 300)
    
    def get_next_checkpoint(self, x, y):
        return 1,1

    def arrangeBoats(self, boats):
        boats[0].set_position(50, 1800)
        boats[1].set_position(50, 1900)