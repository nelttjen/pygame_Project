from collections import defaultdict
from Boat.levelBuilder1 import LevelBuilder1

from Boat.mapGenerator import MapGenerator


class Collisiontypes:
    SENSOR = 1
    BOAT = 2
    SHORE = 3
    CHECKPOINT = 4


class Screen:
    WIDTH = 920
    HEIGHT = 700
    DEBUG = False


class Specifications:
    BOATS = [[0.5, "yacht_1.png", 150, 0.01, 0.005],
             [0.5, "yacht_2.png", 150, 0.01, 0.005],
             [0.5, "yacht_3.png", 150, 0.01, 0.005],
             [0.5, "yacht_4.png", 150, 0.01, 0.005],
             [0.5, "yacht_5.png", 150, 0.01, 0.005],
             [0.5, "yacht_6.png", 150, 0.01, 0.005]]


class Tracks:
    tracks = defaultdict()

    def get_track(self: int):
        if not Tracks.tracks.get(self):
            if self < 0:
                Tracks.tracks[self] = Tracks.get_trackgenerator1(self)
            else:
                func, argument = Tracks.TRACKS[self]
                Tracks.tracks[self] = func(argument)
        return Tracks.tracks[self]

    def get_trackgenerator1(self: int):
        if self < 0:
            map_generator = MapGenerator(*Tracks.TRACKSDEV1[1 + self])
        else:
            map_generator = MapGenerator(*Tracks.TRACKS1[self])
        return LevelBuilder1((100, 73), map_generator)

    TRACKS1 = [(23, 23, 27, 27, 2, 14),
               (24, 24, 29, 29, 2, 18),
               (25, 25, 30, 30, 2, 36),
               (15, 15, 19, 19, 2, 3)]

    TRACKSDEV1 = [(11, 11, 15, 15, 1, 5),
                  ]

    def get_trackgenerator2(self: int):
        pass
        # return LevelBuilder2(Tracks.TRACKS2[level_no])

    TRACKS2 = []

    TRACKS = [(get_trackgenerator1, 0), (get_trackgenerator1, 1), (get_trackgenerator1, 2), (get_trackgenerator1, 3)]
