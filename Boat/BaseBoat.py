from collections import defaultdict
import math

from pymunk.shape_filter import ShapeFilter
from Config import Collisiontypes
import pymunk
import pygame as pg
from pymunk.vec2d import Vec2d

from Utills.utils import load_image


# global BOAT_ID
# BOAT_ID = 0


class BaseBoat:
    def __init__(self, space, radarManager, settings, level):
        mass, im, power, stability, streamlining = settings
        self.BOAT_ID = 0
        car_mass = mass
        self.stability = stability
        self.power = power
        self.streamlining = streamlining
        self.radarCallbacks = defaultdict(list)

        self.turn, self.move = 0, 0
        self.FF = 1
        self.level = level
        self.next_checkpoint = 0
        self.lap = 0
        self.logo_img = pg.transform.scale(load_image(im), (150, 50))

        self.width = 50
        self.length = 150

        # self.car_shape = pymunk.Poly(None,  [(-self.length/2, -self.width/2), (self.length/2, -self.width/2),
        # (self.length/2, self.width/2), (-self.length/2, self.width/2)])
        self.car_shape = pymunk.Poly(None, [(-self.length / 2, -self.width / 3), (0, -self.width / 2),
                                            (self.length / 2, -self.width / 5), (self.length / 2, self.width / 5),
                                            (0, self.width / 2), (-self.length / 2, self.width / 3)])

        self.car_shape.filter = ShapeFilter(group=self.BOAT_ID)
        self.BOAT_ID += 1
        self.car_shape.color = [0, 0, 0, 0]
        self.car_shape.elasticity = 0.5
        self.car_shape.friction = 0.61
        self.car_shape.collision_type = Collisiontypes.BOAT

        car_moment = pymunk.moment_for_poly(car_mass, self.car_shape.get_vertices())
        self.car_shape.body = pymunk.Body(car_mass, car_moment)
        self.car_shape.body.angle = 0

        space.add(self.car_shape, self.car_shape.body)

        radarManager.create_radar(self.car_shape, self.radar_callback)
        self.radarCallbacks[Collisiontypes.CHECKPOINT].append(self.pass_checkpoint)

        self.next_checkpoint_x, self.next_checkpoint_y = 0, 0
        self.velocity = 0

        self.p = None
        self.scaled_logo_img = None
        self.rotated_logo_img = None

    def radar_callback(self, collisionType, distance, tag, collideShape):
        for callback in self.radarCallbacks[collisionType]:
            callback(distance, tag, collideShape)

    def pass_checkpoint(self, distance, tag, collideShape):
        if collideShape:
            current_c, next_c = self.level.get_checkpoint_info(collideShape)
            if current_c == self.next_checkpoint:
                self.next_checkpoint = next_c
                if current_c == 0:
                    self.lap += 1
        self.next_checkpoint_x, self.next_checkpoint_y = self.level.get_coords(self.next_checkpoint)
        return distance, tag

    def set_position(self, x, y, k):
        self.car_shape.body.position = (x, y)
        self.car_shape.body.angle = math.pi * k

    def update(self, move, turn):
        R = self.length / 2
        angularForce = self.stability * R * R * self.car_shape.body.angular_velocity / 2
        # компенсация вращения
        self.car_shape.body.apply_force_at_local_point((0, angularForce), (-R, 0))
        self.car_shape.body.apply_force_at_local_point((0, -angularForce), (R, 0))
        # компенсация заноса
        angle = self.car_shape.body.angle
        self.velocity = self.car_shape.body.velocity.rotated(-angle)
        self.car_shape.body.apply_force_at_local_point((0, 2 * R * self.stability * -self.velocity.y))
        # естественное торможение
        self.car_shape.body.apply_force_at_local_point((self.streamlining * self.width * -self.velocity.x, 0))
        # мотор
        motor_power = Vec2d(move * self.power, self.FF * turn * self.power)
        K = max(1, motor_power.length / self.power)
        self.car_shape.body.apply_force_at_local_point(
            (motor_power.x / K, motor_power.y / K), (self.FF * -50, 0)
        )

    def get_position(self):
        return self.car_shape.body.position.x, self.car_shape.body.position.y

    def get_velocity(self):
        return self.velocity.length

    def get_info(self):
        x, y = self.get_position()
        dx, dy = self.next_checkpoint_x - x, self.next_checkpoint_y - y
        dxy = Vec2d(dx, dy)
        if self.next_checkpoint == 0:
            return self.lap, 78, dxy.length
        else:
            return self.lap, self.next_checkpoint, dxy.length

    def update_image(self, surface, tx, ty, scaling):
        angle_degrees = math.degrees(self.car_shape.body.angle)
        self.scaled_logo_img = pg.transform.scale(self.logo_img, (
            self.logo_img.get_size()[0] * scaling, self.logo_img.get_size()[1] * scaling))
        self.rotated_logo_img = pg.transform.rotate(self.scaled_logo_img, -angle_degrees)
        self.p = (
            self.car_shape.body.position.x - tx,
            self.car_shape.body.position.y - ty,
        )
        offset = pymunk.Vec2d(*self.rotated_logo_img.get_size()) / (2 * scaling)
        self.p = self.p - offset

        surface.blit(self.rotated_logo_img, (round(self.p.x * scaling), round(self.p.y * scaling)))
