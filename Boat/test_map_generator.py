import unittest
from unittest import TestCase
from Boat.mapGenerator import MapGenerator


class Test_MapGenerator(TestCase):

    def create_map(self):
        return MapGenerator(11, 11, 15, 15, 0, 10)

    def test_corners(self):
        map = self.create_map()
        map.is_corner((2, 2))
        self.assertEqual(map.is_corner((2, 2)), True)
        self.assertEqual(map.is_corner((12, 2)), True)
        self.assertEqual(map.is_corner((2, 12)), True)
        self.assertEqual(map.is_corner((12, 12)), True)

    def test_corner_distance(self):
        map = self.create_map()
        self.assertEqual(map.map_distance_to_corner((2, 4), (1, 0), 1), 9)
        self.assertEqual(map.map_distance_to_corner((4, 2), (0, 1), 1), 3)
        self.assertEqual(map.map_distance_to_corner((12, 4), (-1, 0), 1), 3)
        self.assertEqual(map.map_distance_to_corner((4, 12), (0, -1), 1), 9)

        self.assertEqual(map.map_distance_to_corner((2, 4), (1, 0), -1), 3)
        self.assertEqual(map.map_distance_to_corner((4, 2), (0, 1), -1), 9)
        self.assertEqual(map.map_distance_to_corner((12, 4), (-1, 0), -1), 9)
        self.assertEqual(map.map_distance_to_corner((4, 12), (0, -1), -1), 3)

    def test_flat_shift(self):
        for point_n, shift in [(5, (0, 1)), (15, (-1, 0)), (20, (0, -1)), (25, (1, 0))]:
            map = self.create_map()
            map.flat_shift(point_n, shift)
            self.validate_track(map)

    def test_corner_shift(self):
        for point_n, shifts in [(30, [(0, -1), (1, 0)]), (10, [(0, 1), (-1, 0)]), (20, [(0, -1), (-1, 0)])]:
            for shift in shifts:
                map = self.create_map()
                map.corner_shift(point_n, shift)
                self.validate_track(map)

    def test_deformations(self):
        map = MapGenerator(23, 23, 27, 27, 0, 14)
        map.add_deformations(2)

        cp, lp = map.add_decorations()
        print(map)
        self.validate_track(map)
        return map, cp, lp

    def validate_track(self, map):
        first_point = map.track.pop()
        last_point = first_point
        for point in map.track:
            delta = abs(point[0] - last_point[0]) + abs(point[1] - last_point[1])
            self.assertEqual(delta < 1 or delta > 2, False)
            self.assertEqual(map.map[point[1]][point[0]] in [1, 'c', 'x'], True)
            last_point = point
        map.track.append(first_point)


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    unittest.main(testRunner=runner)
