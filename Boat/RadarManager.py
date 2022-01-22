import pymunk
from pygame.colordict import THECOLORS
from pymunk.vec2d import Vec2d
from collections import defaultdict


class Radar:
    LEFT = 0
    FRONT = 1
    RIGTH = 2
    BACKLEFT = 3
    BACK = 4
    BACKRIGTH = 5


class RadarManager:
    pi = 3.14
    RADARS = [
        (Radar.LEFT, -pi / 4, [2, 2], 100, 1),
        (Radar.FRONT, 0, [2, 3], 100, 1),
        (Radar.RIGTH, pi / 4, [3, 3], 100, 1),
        (Radar.BACKRIGTH, pi - pi / 4, [5, 5], 50, 1),
        (Radar.BACK, pi, [0, 5], 50, 1),
        (Radar.BACKLEFT, pi + pi / 4, [0, 0], 50, 1)
    ]

    class RadarSensor:
        originalShape: pymunk.Shape
        shape: pymunk.Shape
        body: pymunk.Body
        angle: float
        tag: int

        def __init__(
                self,
                space: pymunk.Space,
                originalShape: pymunk.Shape,
                angle: float,
                distance: float,
                offset: float,
                vertices: list,
                collisionType: int,
                callback,
                tag: int):
            self.originalShape = originalShape
            self.angle = angle
            self.distance = distance
            self.callback = callback
            self.tag = tag
            self.vertices = vertices
            self.offset = offset

            self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

            start_point = (0, 0)
            self.shape = pymunk.Segment(
                self.body, start_point, start_point, 0.0)
            self.shape.collision_type = collisionType
            self.shape.filter = originalShape.filter
            self.shape.color = THECOLORS["white"]
            self.shape.sensor = True

            self.temp1, self.temp2 = None, None

            space.add(self.body, self.shape)
            self.update()

        def get_vertices(self, shape):
            self.temp1 = 0
            vertices = []
            for v in shape.get_vertices():
                vertex = v.rotated(shape.body.angle) + shape.body.position
                vertices.append(vertex)
            return vertices

        def run_callback(self, collisionType, distance, collideShape):
            if distance > 0.3:
                self.shape.color = THECOLORS["white"]
            else:
                self.shape.color = THECOLORS["red"]
            self.callback(collisionType, distance, self.tag, collideShape)

        def update(self):
            vertices = self.get_vertices(self.originalShape)
            self.body.position = (
                (vertices[self.vertices[1]] + vertices[self.vertices[0]]) / 2)
            direction = Vec2d(
                1,
                0).rotated(
                self.originalShape.body.angle +
                self.angle)
            self.shape.unsafe_set_endpoints(
                self.offset * direction,
                (self.distance + self.offset) * direction)

    def __init__(self, space, sensorCollisionType):
        self.space = space
        self.collisionTypes = []
        self.collisionType = sensorCollisionType
        self.radars = defaultdict()

        self.temp1, self.temp2 = None, None

    def register_collision_type(self, collisionType):
        self.collisionTypes.append(collisionType)
        collision_handler = self.space.add_collision_handler(
            self.collisionType, collisionType)
        collision_handler.pre_solve = lambda arbiter, space, data: \
            self.on_collision(arbiter, space, data, collisionType)
        collision_handler.separate = lambda arbiter, space, data: self.on_collision(
            arbiter, space, data, collisionType)
        for radar in self.radars.values():
            radar.run_callback(collisionType, 1, None)

    def on_collision(self, arbiter, space, data, collisionType):
        self.temp1, self.temp2 = space, data
        radar = self.radars[arbiter.shapes[0]]
        if not radar:
            radar = self.radars[arbiter.shapes[1]]
            collideShape = arbiter.shapes[0]
        else:
            collideShape = arbiter.shapes[1]
        if collideShape == radar.originalShape:
            return False
        if not radar:
            return False
        length = radar.distance
        for cp in arbiter.contact_point_set.points:
            for point in [cp.point_a, cp.point_b]:
                v = radar.body.position - point
                length = min(length, v.length)
        radar.run_callback(
            collisionType,
            length / radar.distance,
            collideShape)

        return False

    def create_radar(self, shape, callback):
        for tag, angle, vertices, distance, offset in RadarManager.RADARS:
            radar = self.RadarSensor(
                space=self.space,
                originalShape=shape,
                angle=angle,
                vertices=vertices,
                distance=distance,
                offset=offset,
                collisionType=self.collisionType,
                callback=callback,
                tag=tag)
            for collisionType in self.collisionTypes:
                radar.run_callback(collisionType, 1, None)
            self.radars[radar.shape] = radar

    def update_sensors(self):
        for sensor in self.radars.values():
            sensor.update()
