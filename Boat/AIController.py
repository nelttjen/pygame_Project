import math
from Boat.ai import Dqn
from config import Collisiontypes
from pymunk.vec2d import Vec2d

class AIController:
    action2command = [(1,1), (-1,1), (1,-1), (-1,-1), (1,0), (-1,0)]
    def __init__(self, boat, level):        
        self.boatsSensors = {}
        self.shoreSensors = {}
        self.level = level
        self.boat = boat
        self.lastReward = 0
        self.lastDistance = 1e6
        self.lastVelocity = 0
        boat.radarCallbacks[Collisiontypes.BOAT].append(self.updateBoatSensors)
        boat.radarCallbacks[Collisiontypes.SHORE].append(self.updateShoreSensors)
        self.brain = Dqn(8, len(AIController.action2command), 20, 0.9)
    
    def updateBoatSensors(self, distance, tag, _):
        self.boatsSensors[tag] = distance
    
    def updateShoreSensors(self, distance, tag, _):
        self.shoreSensors[tag] = distance

    def update(self):
        x, y = self.boat.get_position()
        dx, dy = self.boat.next_checkpoint_x - x, self.boat.next_checkpoint_y - y
        dxy = Vec2d(dx,dy)

        body = self.boat.car_shape.body
        orientationV = body.velocity.get_angle_between(dxy)

        reward = 0
        if abs(orientationV) < 0.2:
            reward += 5 
        elif abs(orientationV) > 0.5:
            reward -=1
        if dxy.length < self.lastDistance:
            reward += 10 
            if body.velocity.length > self.lastVelocity:
                reward += 5
        if dxy.length > self.lastDistance:
            reward -= 5
        for shoreDistance in self.shoreSensors.values():
            if shoreDistance<0.2:
                reward -= 3

        self.lastDistance = dxy.length
        self.lastVelocity = body.velocity.length

        
        state = [orientationV, body.angular_velocity] + [*self.shoreSensors.values()] + [*self.boatsSensors.values()]
       
        action = self.brain.update(reward, state)
        move, turn = AIController.action2command[action]
        self.boat.update(move, turn)
        print(reward)
        pass

    def processEvent(self, event):
        pass