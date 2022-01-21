import unittest
from unittest import TestCase
from Boat.mapGenerator import MapGenerator


def create_map():
    return MapGenerator(11, 11, 15, 15, 0, 10)


class Test_MapGenerator(TestCase):

    def test_corners(self):
        mapa = create_map()
        mapa.is_corner((2, 2))
        self.assertEqual(mapa.is_corner((2, 2)), True)
        self.assertEqual(mapa.is_corner((12, 2)), True)
        self.assertEqual(mapa.is_corner((2, 12)), True)
        self.assertEqual(mapa.is_corner((12, 12)), True)

    def test_corner_distance(self):
        mapa = create_map()
        self.assertEqual(mapa.map_distance_to_corner((2, 4), (1, 0), 1), 9)
        self.assertEqual(mapa.map_distance_to_corner((4, 2), (0, 1), 1), 3)
        self.assertEqual(mapa.map_distance_to_corner((12, 4), (-1, 0), 1), 3)
        self.assertEqual(mapa.map_distance_to_corner((4, 12), (0, -1), 1), 9)

        self.assertEqual(mapa.map_distance_to_corner((2, 4), (1, 0), -1), 3)
        self.assertEqual(mapa.map_distance_to_corner((4, 2), (0, 1), -1), 9)
        self.assertEqual(mapa.map_distance_to_corner((12, 4), (-1, 0), -1), 9)
        self.assertEqual(mapa.map_distance_to_corner((4, 12), (0, -1), -1), 3)

    def test_flat_shift(self):
        for point_n, shift in [(5, (0, 1)), (15, (-1, 0)), (20, (0, -1)), (25, (1, 0))]:
            mapa = create_map()
            mapa.flat_shift(point_n, shift)
            self.validate_track(mapa)

    def test_corner_shift(self):
        for point_n, shifts in [(30, [(0, -1), (1, 0)]), (10, [(0, 1), (-1, 0)]), (20, [(0, -1), (-1, 0)])]:
            for shift in shifts:
                mapa = create_map()
                mapa.corner_shift(point_n, shift)
                self.validate_track(mapa)

    def test_deformations(self):
        mapa = MapGenerator(23, 23, 27, 27, 0, 14)
        mapa.add_deformations(2)

        cp, lp = mapa.add_decorations()
        print(mapa)
        self.validate_track(mapa)
        return mapa, cp, lp

    def validate_track(self, mapa):
        first_point = mapa.track.pop()
        last_point = first_point
        for point in mapa.track:
            delta = abs(point[0] - last_point[0]) + abs(point[1] - last_point[1])
            self.assertEqual(delta < 1 or delta > 2, False)
            self.assertEqual(mapa.map[point[1]][point[0]] in [1, 'c', 'x'], True)
            last_point = point
        mapa.track.append(first_point)


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    unittest.main(testRunner=runner)
