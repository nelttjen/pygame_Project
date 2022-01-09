import random


class MapGenerator:
    def __init__(self, track_width, track_height, map_width, map_height, seed):
        random.seed(seed)
        self.track_width = track_width
        self.track_height = track_height
        self.map_width = map_width
        self.map_height = map_height

        self.map = [[0]*map_width for i in range(map_height)]

        for x in range(map_width):
            self.map[0][x] = 8
            self.map[map_height-1][x] = 8

        for y in range(map_height):
            self.map[y][0] = 8
            self.map[y][map_width-1] = 8

        startx = int((map_width - track_width)/2)
        starty = int((map_height - track_height)/2)

        trackh1 = []
        trackh2 = []
        for x in range(track_width):
            trackh1.append((startx + x, starty))
            trackh2.append((startx + track_width - x -
                           1, starty + track_height - 1))
        trackv1 = []
        trackv2 = []
        for y in range(1, track_height-1):
            trackv1.append((startx + track_width - 1, starty + y))
            trackv2.append((startx, starty + track_height - y - 1))
        self.track = trackh1 + trackv1 + trackh2 + trackv2

        for x, y in self.track:
            self.map[y][x] = 1

    def is_corner(self, point):
        return self.map[point[1]-1][point[0]] != self.map[point[1]+1][point[0]]

    def map_distance_to_corner(self, point, shift, direction):
        rotated = (-shift[1]*direction, shift[0]*direction)
        return self.map_distance_to(point, rotated, 0)

    def map_get(self, point, shift):
        return self.map[point[1]+shift[1]][point[0] + shift[0]]

    def track_set(self, point_n, c):
        point = self.track[point_n]
        self.map[point[1]][point[0]] = c

    def map_distance_to(self, point, shift, c):
        i = 0
        while True:
            i += 1
            shift_ = (shift[0]*i, shift[1]*i)
            c_ = self.map_get(point, shift_)
            if c_ == c:
                return i
            if c_ == 8:
                return -1

    def line_shift(self, point_n1, point_n2, shift, corner):
        point2 = self.track[point_n2]
        point1 = self.track[point_n1]
        min_offset = max(self.track_height, self.track_width)
        for point_n in range(point_n1, point_n2+1):
            offset = self.map_distance_to(self.track[point_n], shift, 1)
            if offset < 5:
                return False
            if offset < min_offset:
                min_offset = offset
        min_offset -= 3
        offset = random.randint(2, min_offset)
        for point_n in range(point_n1, point_n2+1):
            point = self.track[point_n]
            self.track_set(point_n, 0)
            self.track[point_n] = (
                point[0]+shift[0]*offset, point[1]+shift[1]*offset)
            self.track_set(point_n, 1)

        if corner != 0:
            point_d, point_i, point_i_delta = {
                -1: (point_n1-offset, point_n2, -1), 1: (point_n2+2, point_n1, -1)}[corner]
            point2 = self.track[point_i]

        for o in range(offset):
            if corner == 0:
                point_n2 += 1
                self.track.insert(
                    point_n2, ((point2[0]+shift[0]*o, point2[1]+shift[1]*o)))
                self.track_set(point_n2, 1)
                self.track.insert(
                    point_n1, ((point1[0]+shift[0]*(offset-o - 1), point1[1]+shift[1]*(offset-o - 1))))
                self.track_set(point_n1, 1)
            else:
                self.track_set(point_d, 0)
                self.track.pop(point_d)
                # self.track.insert(
                #    point_i, ((point2[0]+shift[0]*(offset-o - 1)*point_i_delta, point2[1]+shift[1]*(offset-o - 1)*point_i_delta)))
                self.track.insert(
                    point_i, ((point2[0]+shift[0]*(o + 1)*point_i_delta, point2[1]+shift[1]*(o + 1)*point_i_delta)))
                self.track_set(point_i, 1)

        return True

    def corner_shift(self, point_n, shift):
        point = self.track[point_n]
        offset1 = max(0, self.map_distance_to_corner(point, shift, 1) - 4)
        offset2 = max(0, self.map_distance_to_corner(point, shift, -1) - 4)

        if offset1 > 0:
            offset = random.randint(1, offset1)
            return self.line_shift(point_n-offset, point_n-1, shift, 1)
        if offset2 > 0:
            offset = random.randint(1, offset2)
            return self.line_shift(point_n+1, point_n + offset, shift, -1)

    def flat_shift(self, point_n, shift):
        point = self.track[point_n]
        offset1 = self.map_distance_to_corner(point, shift, 1)
        offset2 = self.map_distance_to_corner(point, shift, -1)
        max_width = offset1+offset2-8

        if max_width < 3:
            return False

        width = random.randint(3, max_width)
        start = 4+random.randint(0, max_width - width)
        point_n1 = point_n + start - offset1
        return self.line_shift(point_n1, point_n1 + width, shift, 0)

    def add_deformations(self, deformations):
        for i in range(deformations):
            while True:
                point_n = random.randint(1, len(self.track)-1)
                point = self.track[point_n]
                if(self.is_corner(point)):
                    if random.randint(0, 1) == 0:
                        if(self.map_get(point, [1, 0]) == 1):
                            shift = (1, 0)
                        else:
                            shift = (-1, 0)
                    else:
                        if(self.map_get(point, (0, 1)) == 1):
                            shift = (0, 1)
                        else:
                            shift = (0, -1)
                    if self.corner_shift(point_n, shift):
                        break
                else:
                    if self.map_get(point, (1, 0)) == 1:
                        if self.map_distance_to(point, [0, 1], 1) > 0:
                            shift = (0, 1)
                        else:
                            shift = (0, -1)
                    else:
                        if self.map_distance_to(point, (1, 0), 1) > 0:
                            shift = (1, 0)
                        else:
                            shift = (-1, 0)
                    if self.flat_shift(point_n, shift):
                        break

    def __repr__(self):
        txt = ""
        for row in self.map:
            txt += " ".join([str(c) for c in row])
            txt += "\n"
        return txt
