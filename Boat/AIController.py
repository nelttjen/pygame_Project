import math
from random import randint
from Boat.ai import Dqn, Network
from Config import Collisiontypes
from pymunk.vec2d import Vec2d
import curses

ACTION2COMMAND = [(-1,1), (1,1), (1,-1), (-1,-1)]
MODEL = Network(13, len(ACTION2COMMAND), 50)
STDSCR = curses.initscr()
global SCRLINE
SCRLINE = 0
class AIController:
    def __init__(self, boat, level):
        self.boatsSensors = {}
        self.shoreSensors = {}
        self.level = level
        self.boat = boat
        self.lastDistance = 0
        self.lastVelocity = 0
        self.lastReward = 0
        boat.radarCallbacks[Collisiontypes.BOAT].append(self.updateBoatSensors)
        boat.radarCallbacks[Collisiontypes.SHORE].append(self.updateShoreSensors)        
        self.brain = Dqn(0.9, 50, MODEL)
        global SCRLINE
        self.scrline = SCRLINE
        SCRLINE += 5
        self.count = 0
    
    def updateBoatSensors(self, distance, tag, _):
        self.boatsSensors[tag] = distance
    
    def updateShoreSensors(self, distance, tag, _):
        self.shoreSensors[tag] = distance

    def update(self):
        x, y = self.boat.get_position()
        dx, dy = self.boat.next_checkpoint_x - x, self.boat.next_checkpoint_y - y
        dxy = Vec2d(dx,dy)
        if self.count % 50 == 0:
            if self.lastDistance > dxy.length:
                self.lastReward+=0.1
            else:
                self.lastReward-=0.2
            self.lastDistance = dxy.length
        if self.count % 6 == 0 :
            body = self.boat.car_shape.body
            orientationV = body.velocity.get_angle_between(dxy)
            orientationA = body.rotation_vector.get_angle_between(dxy)
            reward = (self.lastDistance - dxy.length)
#            self.lastReward += max(0.1, (self.lastDistance - dxy.length)*0.1)
#            self.lastReward += max(0, 0.5*(0.4-abs(orientationA)))
#            reward +=5*(0.4-abs(orientationV))

            for shoreDistance in self.shoreSensors.values():
                reward -= (1-shoreDistance)*6
            for boatDistance in self.boatsSensors.values():
                reward -= (1-boatDistance)*2

            reward += self.lastReward
            self.lastDistance = dxy.length
            self.lastVelocity = body.velocity.length

            
            #state = [orientationV, body.angular_velocity] + [*self.shoreSensors.values()] + [*self.boatsSensors.values()]
            state = [orientationA/3.14] + [*self.shoreSensors.values()] +  [*self.boatsSensors.values()]
        
            self.action = self.brain.update(reward, state)
            
            STDSCR.addstr(self.scrline + 0, 0, f'Reward:{reward:.2f} Learn score:{self.brain.learn_score:.2f}')
            STDSCR.addstr(self.scrline + 1, 0, f'X:{x:.2f} Y:{y:.2f} GoalX:{self.boat.next_checkpoint_x:.2f} GoalY:{self.boat.next_checkpoint_y:.2f} ')
            STDSCR.addstr(self.scrline + 2, 0, f'OrientationV:{orientationV:.2f} OrientationA:{orientationA:.2f} Angular speed:{body.angular_velocity:.2f}')
            self.printSensors("Shore", self.scrline + 3, self.shoreSensors)
            self.printSensors("Boat", self.scrline + 4, self.boatsSensors)
            STDSCR.refresh()

        self.count+=1
        self.move, self.turn = ACTION2COMMAND[self.action]
        self.boat.update(self.move, self.turn)

    def printSensors(self, label, line, sensors):
        str=""
        for key, distance in sensors.items():
                str+=f'{label}{key}: {distance:2f} '
        STDSCR.addstr(line, 0, str)

    def processEvent(self, event):
        pass