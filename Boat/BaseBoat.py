import pymunk
from random import randrange


class BaseBoat:
    def __init__(self, app):
        self.app = app
        self.FPS = app.FPS

        car_mass = 0.5
        self.old_position_x = self.old_position_y = 100
        self.turn, self.move = 0, 0
        self.translation = pymunk.Transform()

        self.car_shape = pymunk.Poly.create_box(None, size=(100, 60))
        self.car_shape.color = [randrange(256) for _ in range(4)]
        car_moment = pymunk.moment_for_poly(car_mass / 5, self.car_shape.get_vertices())
        self.car_shape.body = pymunk.Body(car_mass, car_moment)
        self.car_shape.body.position = (100, 100)
        self.car_shape.body.angle = -1
        self.app.space.add(self.car_shape, self.car_shape.body)
