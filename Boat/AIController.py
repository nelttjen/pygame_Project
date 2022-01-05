import math
from Boat.ai import Dqn
from config import Collisiontypes
from pymunk.vec2d import Vec2d
import curses

class AIController:
    action2command = [(-1,1), (1,1), (1,0), (-1,0)]
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
        self.brain = Dqn(7, len(AIController.action2command), 20, 0.9, 30)
        self.count = -1
        self.stdscr = curses.initscr()
    
    def updateBoatSensors(self, distance, tag, _):
        self.boatsSensors[tag] = distance
    
    def updateShoreSensors(self, distance, tag, _):
        self.shoreSensors[tag] = distance

    def update(self):
        self.count+=1
        if self.count % 10 == 0 :
            x, y = self.boat.get_position()
            dx, dy = self.boat.next_checkpoint_x - x, self.boat.next_checkpoint_y - y
            dxy = Vec2d(dx,dy)

            body = self.boat.car_shape.body
            orientationV = body.velocity.get_angle_between(dxy)
            orientationA = body.rotation_vector.get_angle_between(dxy)

            reward = 0
            if False:
                if abs(orientationV) < 0.2:
                    reward += 5 
                elif abs(orientationV) > 0.5:
                    reward -=1
            if dxy.length < self.lastDistance:
                reward += (5 + (self.lastDistance - dxy.length)*10)
                speed_reward = 3               
            else:
                speed_reward = 1

            if orientationA < 0.2:
                speed_reward +=2
            if orientationV < 0.2:
                speed_reward +=2

            if body.velocity.length > self.lastVelocity:
                reward += (1+ (body.velocity.length - self.lastVelocity)*speed_reward)
            if dxy.length > self.lastDistance:
                reward -= 5
            for shoreDistance in self.shoreSensors.values():
                if shoreDistance<0.3:
                    reward -= 10

            self.lastDistance = dxy.length
            self.lastVelocity = body.velocity.length

            
            #state = [orientationV, body.angular_velocity] + [*self.shoreSensors.values()] + [*self.boatsSensors.values()]
            state = [orientationA, orientationV] + [*self.shoreSensors.values()] 
        
            action = self.brain.update(reward, state)
            self.move, self.turn = AIController.action2command[action]
            self.stdscr.addstr(0, 0, f'Reward:{reward:.2f} Learn score:{self.brain.learn_score:.2f}')
            self.stdscr.addstr(1, 0, f'X:{x:.2f} Y:{y:.2f} GoalX:{self.boat.next_checkpoint_x:.2f} GoalY:{self.boat.next_checkpoint_y:.2f} ')
            self.stdscr.addstr(2, 0, f'OrientationV:{orientationV:.2f} OrientationA:{orientationA:.2f} ')
            self.printSensors("Shore", 3, self.shoreSensors)
            self.printSensors("Boat", 4, self.boatsSensors)
            self.stdscr.refresh()

        self.boat.update(self.move, self.turn)

    def printSensors(self, label, line, sensors):
        str=""
        for key, distance in sensors.items():
                str+=f'{label}{key}: {distance:2f} '
        self.stdscr.addstr(line, 0, str)

    def processEvent(self, event):
        pass