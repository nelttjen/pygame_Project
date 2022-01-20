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

class Specifications:
    BOATS = [[0.5, "yacht_1.png", 150, 0.01, 0.005],
             [0.5, "yacht_2.png", 150, 0.01, 0.005],
             [0.5, "yacht_3.png", 150, 0.01, 0.005],
             [0.5, "yacht_4.png", 150, 0.01, 0.005],
             [0.5, "yacht_5.png", 150, 0.01, 0.005],
             [0.5, "yacht_6.png", 150, 0.01, 0.005]]

class Tracks:
    tracks = defaultdict()

    def get_track(level_no:int):
        if not Tracks.tracks.get(level_no):
            func, argument = Tracks.TRACKS[0]
            Tracks.tracks[level_no] = func(argument)
        return Tracks.tracks[level_no]

    def get_trackgenerator1(track_no:int):
        map_generator = MapGenerator(*Tracks.TRACKS1[track_no])
        map_generator.add_deformations(2)
        return LevelBuilder1((100, 73), map_generator)

    TRACKS1 = [(23, 23, 27, 27, 14),
               (24, 24, 29, 29, 18),
               (25, 25, 30, 30, 36),
               (15, 15, 19, 19, 3)]

    def get_trackgenerator2(level_no:int):
        pass
        #return LevelBuilder2(Tracks.TRACKS2[level_no])

    TRACKS2 = []

    TRACKS = [(get_trackgenerator1, 0), (get_trackgenerator1, 1), (get_trackgenerator1, 2), (get_trackgenerator1, 3)]
 