import pymunk
from pygame.colordict import THECOLORS
from pymunk.vec2d import Vec2d
from collections import defaultdict

class RadarManager:
    class Radar:
        originalShape: pymunk.Shape
        shape: pymunk.Shape
        body: pymunk.Body
        angle: float
        tag: int

        def __init__(self, space: pymunk.Space, originalShape: pymunk.Shape, angle: float, distance:float, callback, tag: int):
            self.originalShape = originalShape
            self.angle = angle
            self.distance = distance
            self.callback = callback
            self.tag = tag

            self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

            start_point = (0, 0)
            self.shape = pymunk.Segment(self.body, start_point, start_point, 0.0)
            self.shape.collision_type = RadarManager.COLLISION_TYPE
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
            self.body.position = (vertices[1] + vertices[0]) / 2
            direction = Vec2d(1, 0).rotated(self.originalShape.body.angle + self.angle)
            end_point = self.distance * direction
            self.shape.unsafe_set_endpoints(10 * direction, self.distance * direction)

    COLLISION_TYPE = 7
  
    def __init__(self, space):
        self.space = space
        self.sensors = defaultdict()
        self.sensor_range = 100
        pi=3.14

        self.sensor_angles = [0, pi / 6, -pi / 6, pi / 3, -pi / 3]
        collision_handler = self.space.add_wildcard_collision_handler(self.COLLISION_TYPE)
        collision_handler.pre_solve = self.onCollision

    def onCollision(self, arbiter, space, data):
        sensor = self.sensors[arbiter.shapes[0]]
        if not sensor:
            sensor = self.sensors[arbiter.shapes[1]]
        if not sensor:
            return False
       # for cp in arbiter.contact_point_set.points:
       #     cp.poimt_a
       #     cp.poimt_b
        sensor.callback(0, sensor.tag)

        return False

    def createRadar(self, shape, callback):
        for i in range(len(self.sensor_angles)):
            sensor = self.Radar(space=self.space, originalShape=shape, angle=self.sensor_angles[i], distance=self.sensor_range, callback=callback, tag=i)
            sensor.update()
            self.sensors[sensor.shape] = sensor

    def updateSensors(self):
        for sensor in self.sensors.values():
            sensor.update()
