from pygame import Vector2, Vector3
import pymunk
from pygame.colordict import THECOLORS
from pymunk import vec2d
from pymunk.vec2d import Vec2d
from collections import defaultdict

class RadarManager:
    class Radar:
        originalShape: pymunk.Shape
        shape: pymunk.Shape
        body: pymunk.Body
        angle: float
        tag: int

        def __init__(self, space: pymunk.Space, originalShape: pymunk.Shape, angle: float, distance:float, collisionType:int, callback, tag: int):
            self.originalShape = originalShape
            self.angle = angle
            self.distance = distance
            self.callback = callback
            self.tag = tag

            self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

            start_point = (0, 0)
            self.shape = pymunk.Segment(self.body, start_point, start_point, 0.0)
            self.shape.collision_type = collisionType
            self.shape.color = THECOLORS["white"]
            self.shape.sensor = True

            space.add(self.body, self.shape)

        def getVertices(self, shape):
            vertices = []
            for v in shape.get_vertices():
                vertex = v.rotated(shape.body.angle) + shape.body.position
                vertices.append(vertex)
            return vertices

        def update(self):
            vertices = self.getVertices(self.originalShape)
            self.body.position = ((vertices[1] + vertices[0]) / 2)
            direction = Vec2d(1, 0).rotated(self.originalShape.body.angle + self.angle)
            end_point = self.distance * direction
            self.shape.unsafe_set_endpoints(5 * direction, (self.distance + 5) * direction)

    COLLISION_TYPE = 7
  
    def __init__(self, space, sensorCollisionType):
        self.space = space
        self.collisionTypes = []
        self.collisionType = sensorCollisionType
        self.radars = defaultdict()
        self.sensor_range = 100
        pi=3.14

        self.sensor_angles = [0, pi / 3, -pi / 3]
    
    def registerCollisionType(self, collisionType):
#        collision_handler = self.space.add_wildcard_collision_handler(self.CollisionType)
        self.collisionTypes.append(collisionType)
        collision_handler = self.space.add_collision_handler(self.collisionType, collisionType)
        collision_handler.pre_solve = lambda arbiter, space, data: self.onCollision(arbiter, space, data, collisionType)
        for radar in self.radars.values():
            radar.callback(collisionType, 0, radar.tag, None)


    def onCollision(self, arbiter, space, data, collisionType):
        radar = self.radars[arbiter.shapes[0]]
        if not radar:
            radar = self.radars[arbiter.shapes[1]]
            collideShape = arbiter.shapes[0]
        else:
            collideShape = arbiter.shapes[1]
        if not radar:
            return False
        length = radar.distance
        for cp in arbiter.contact_point_set.points:
            for point in [cp.point_a, cp.point_b]:
                v = radar.body.position - point
                length = min(length, v.length)
        radar.callback(collisionType, length/radar.distance, radar.tag, collideShape)

        return False

    def createRadar(self, shape, callback):
        for i in range(len(self.sensor_angles)):
            sensor = self.Radar(space=self.space, originalShape=shape, angle=self.sensor_angles[i], distance=self.sensor_range, collisionType = self.collisionType, callback=callback, tag=i)
            sensor.update()
            for collisionType in self.collisionTypes:
                sensor.callback(collisionType, 0, sensor.tag, None)
            self.radars[sensor.shape] = sensor

    def updateSensors(self):
        for sensor in self.radars.values():
            sensor.update()
