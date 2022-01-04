from collections import defaultdict
import math
from typing import DefaultDict
from config import Collisiontypes
import pymunk
import pygame as pg
from random import randrange

from Utills.utils import load_image

class BaseBoat:
    def __init__(self, space, radarManager, settings):
        mass, im, elasticity, friction = settings
        self.radarCallbacks = defaultdict(list)
        car_mass = mass
        self.turn, self.move = 0, 0
        self.logo_img = load_image(im)

        self.car_shape = pymunk.Poly.create_box(None, size=(100, 73))
        self.car_shape.color = [0, 0, 0, 0]
        self.car_shape.elasticity = elasticity
        self.car_shape.friction = friction
        self.car_shape.collision_type =Collisiontypes.BOAT

        car_moment = pymunk.moment_for_poly(car_mass / 5, self.car_shape.get_vertices())
        self.car_shape.body = pymunk.Body(car_mass, car_moment)        
        self.car_shape.body.angle = 0
        
        space.add(self.car_shape, self.car_shape.body)

        radarManager.createRadar(self.car_shape, self.radarCallback)

    def radarCallback(self, collisionType, distance, tag):
        for callback in self.radarCallbacks[collisionType]:
            callback(distance, tag)
        print(collisionType, tag, distance)

    def set_position(self, x, y):
        self.car_shape.body.position = (x, y)
        self.car_shape.body.angle = 11
    
    def update(self, move, turn):
        angularForce = 1 * self.car_shape.body.angular_velocity
        # компенсация вращения
        self.car_shape.body.apply_force_at_local_point((0, angularForce), (-50, 0))
        self.car_shape.body.apply_force_at_local_point((0, -angularForce), (50, 0))
        # компенсация заноса
        angle = self.car_shape.body.angle
        self.velocity = self.car_shape.body.velocity.rotated(-angle)
        self.car_shape.body.apply_force_at_local_point((0, 1 * -self.velocity.y))
        # естественное торможение
        self.car_shape.body.apply_force_at_local_point((0.1 * -self.velocity.x, 0))
        # мотор
        self.car_shape.body.apply_force_at_local_point(
            (10 * move, 3 * turn), (-50, 0)
        )

    def get_position(self):
        return self.car_shape.body.position.x, self.car_shape.body.position.y

    def get_velocity(self):
        return self.velocity.length

    def updateImage(self, surface, tx, ty, scaling):
        angle_degrees = math.degrees(self.car_shape.body.angle)
        self.scaled_logo_img = pg.transform.scale(self.logo_img, (self.logo_img.get_size()[0] * scaling, self.logo_img.get_size()[1] * scaling))
        self.rotated_logo_img = pg.transform.rotate(self.scaled_logo_img, -angle_degrees)
        self.p = (
            self.car_shape.body.position.x + tx,
            self.car_shape.body.position.y + ty,
        )
        offset = pymunk.Vec2d(*self.rotated_logo_img.get_size()) / (2 * scaling)
        self.p = self.p - offset

        surface.blit(self.rotated_logo_img, (round(self.p.x * scaling), round(self.p.y * scaling)))
