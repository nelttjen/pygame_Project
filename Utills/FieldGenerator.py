import random
import copy


class FiledGenerator:
    def __init__(self, x, y, d_min=1, d_max=10):
        self.x, self.y, self.dx, self.dy = 0, 0, x, y
        self.d_min, self.d_max = d_min, d_max
        self.field = []
        # self.back_field = []

    def generate_new(self):
        self.field = []
        # self.back_field = []
        dx, dy = self.dx, self.dy
        step = 0
        while dx > 0 and dy > 0:
            move = random.randint(self.d_min, self.d_max)
            if not step % 2 and dx > 0:
                move = min(dx, move)
                dx -= move
                self.field.append([move, 0, 'right'])
            elif step % 2 and dy > 0:
                move = min(dy, move)
                dy -= move
                self.field.append([0, move, 'down'])
            step += 1
        # self.back_field = copy.deepcopy(self.field[::-1])
        # for i in self.back_field:
        #     i[2] = get_opposite(i[2])

    def set_values(self, x, y, d_min=1, d_max=10):
        self.x, self.y, self.dx, self.dy = 0, 0, x, y
        self.d_min, self.d_max = d_min, d_max

    def get_field(self):
        return self.field

    # def get_back_field(self):
    #     return self.back_field

    def clear(self):
        self.field = []
        # self.back_field = []


def get_opposite(txt: str):
    XY = [['down', 'up'], ['left', 'right']]
    for i in XY:
        if txt in i:
            return i[1 - i.index(txt)]