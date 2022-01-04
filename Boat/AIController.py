from Boat.ai import Dqn
from config import Collisiontypes
from pymunk.vec2d import Vec2d

class AIController:
    action2command = [(1,1), (-1,1), (1,-1), (-1,-1)]
    def __init__(self, boat, level):        
        self.boatsSensors = {}
        self.shoreSensors = {}
        self.level = level
        self.boat = boat
        self.lastReward = 0
        self.lastDistance = 1e6
        boat.radarCallbacks[Collisiontypes.BOAT].append(self.updateBoatSensors)
        boat.radarCallbacks[Collisiontypes.SHORE].append(self.updateShoreSensors)
        self.brain = Dqn(9, 4, 0.9)
    
    def updateBoatSensors(self, distance, tag, _):
        self.boatsSensors[tag] = distance
    
    def updateShoreSensors(self, distance, tag, _):
        self.shoreSensors[tag] = distance

    def update(self):
        x, y = self.boat.get_position()
        dx, dy = self.boat.next_checkpoint_x - x, self.boat.next_checkpoint_y - y
        dxy = Vec2d(dx,dy)

        shoreContact = next(filter(lambda x:x < 0.2, self.shoreSensors), None)
        reward = 0
        if dxy.length < self.lastDistance:
            reward = 10
            self.lastDistance = dxy.length
        if shoreContact:
            reward -= 5

        body = self.boat.car_shape.body
        orientationV = body.velocity.get_angle_between(dxy)
        orientationA = dxy.angle - body.angle/180*3.14
        state = [orientationA, orientationV, body.angular_velocity] + [*self.shoreSensors.values()] + [*self.boatsSensors.values()]
       
        action = self.brain.update(reward, state)
        move, turn = AIController.action2command[action]
        self.boat.update(move, turn)
        print(reward)
        pass

    def processEvent(self, event):
        pass