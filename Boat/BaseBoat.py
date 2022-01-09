from collections import defaultdict
import math
from typing import DefaultDict
from config import Collisiontypes
import pymunk
import pygame as pg
from random import randrange
from Boat.levelBuilder import SandBox
import sys
from pymunk.vec2d import Vec2d

from Utills.utils import load_image

class BaseBoat:
    def __init__(self, space, radarManager, settings, level):
        mass, im, power, stability, streamlining = settings

        car_mass = mass
        self.stability = stability
        self.power = power
        self.streamlining = streamlining
        self.radarCallbacks = defaultdict(list)

        self.turn, self.move = 0, 0
        self.level = level
        self.next_checkpoint = 0
        self.lap = 0
        self.logo_img = load_image(im)

        self.car_shape = pymunk.Poly.create_box(None, size=(100, 73))
        self.car_shape.color = [0, 0, 0, 0]
        self.car_shape.elasticity = 0.5
        self.car_shape.friction = 0.61
        self.car_shape.collision_type =Collisiontypes.BOAT

        car_moment = pymunk.moment_for_poly(car_mass, self.car_shape.get_vertices())
        self.car_shape.body = pymunk.Body(car_mass, car_moment)
        self.car_shape.body.angle = 0
        
        space.add(self.car_shape, self.car_shape.body)

        radarManager.createRadar(self.car_shape, self.radarCallback)
        self.radarCallbacks[Collisiontypes.CHECKPOINT].append(self.passCheckpoint)


    def radarCallback(self, collisionType, distance, tag, collideShape):
        for callback in self.radarCallbacks[collisionType]:
            callback(distance, tag, collideShape)
    
    def passCheckpoint(self, distance, tag, collideShape):
        if collideShape:
            #print(self.level.get_tag(collideShape), self.next_checkpoint)
            current, next = self.level.get_checkpoint_info(collideShape) 
            if current == self.next_checkpoint:
                self.next_checkpoint = next
                if current == 0:
                    self.lap += 1
        self.next_checkpoint_x, self.next_checkpoint_y = self.level.get_coords(self.next_checkpoint)
        print(self.next_checkpoint_x, self.next_checkpoint_y)

    def set_position(self, x, y):
        self.car_shape.body.position = (x, y)
        self.car_shape.body.angle = 11
    
    def update(self, move, turn):
        R = 150
        angularForce = self.stability * R * self.car_shape.body.angular_velocity / 2
        # компенсация вращения
        self.car_shape.body.apply_force_at_local_point((0, angularForce), (-R, 0))
        self.car_shape.body.apply_force_at_local_point((0, -angularForce), (R, 0))
        # компенсация заноса
        angle = self.car_shape.body.angle
        self.velocity = self.car_shape.body.velocity.rotated(-angle)
        self.car_shape.body.apply_force_at_local_point((0, 2 * R * self.stability * -self.velocity.y))
        # естественное торможение
        self.car_shape.body.apply_force_at_local_point((self.streamlining * -self.velocity.x, 0))
        # мотор
        motor_power = Vec2d(move * self.power,turn*self.power)
        K = max(1, motor_power.length/self.power)
        self.car_shape.body.apply_force_at_local_point(
            (motor_power.x/K, motor_power.y/K), (-50, 0)
        )

    def get_position(self):
        return self.car_shape.body.position.x, self.car_shape.body.position.y

    def get_velocity(self):
        return self.velocity.length
    
    def get_info(self):
        x, y = self.get_position()
        dx, dy = self.next_checkpoint_x - x, self.next_checkpoint_y - y
        dxy = Vec2d(dx,dy)

        return (self.lap, self.next_checkpoint, dxy.length)

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
