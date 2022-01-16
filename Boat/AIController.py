import math
from random import randint
from Boat.BaseController import BaseController
from Boat.RadarManager import Radar
from Boat.ai import Dqn, Network
from Config import Collisiontypes
from pymunk.vec2d import Vec2d
import curses

ACTION2COMMAND = [1, -1]
MODEL = Network(14, len(ACTION2COMMAND), 150)

class AIController(BaseController):
    lastDistance = 0
    turn=0
    move = 0
    velocity=(0,0)
    angular_velocity = 0

    def __init__(self, boat, level):
        super().__init__(boat, level)
        self.brain = Dqn(0.9, 100, MODEL)

    def updateChild(self):
        if(self.dxy.length< self.lastDistance):
            reward = 0.1    
#        if (abs(orientationA)< 1):
#            reward = abs(orientationA)
        else:
            reward = -0.2        

        if next(filter(lambda x:x<0.3, self.shoreSensors.values()), None):
            reward = -1
        if next(filter(lambda x:x<0.3, self.boatsSensors.values()), None):
            reward = -0.3

        velocity = [self.boat.velocity.x, self.boat.velocity.y]
        axeleration = [velocity[0] - self.velocity[0], velocity[1] - self.velocity[1]]
        self.velocity = velocity
        angular_axeleration = self.body.angular_velocity - self.angular_velocity
        self.angular_velocity = self.body.angular_velocity

        #state = [orientationA/3.14, body.angular_velocity/10, angular_axeleration, self.move, self.turn] + [*self.shoreSensors.values()] +  [*self.boatsSensors.values()]

        if self.shoreSensors[Radar.FRONT]<0.5 or self.boatsSensors[Radar.FRONT]<0.5: 
            self.move = -1
        else:
            self.move+=0.1

        state = [self.orientationA/3.14, self.move] + [*self.shoreSensors.values()] +  [*self.boatsSensors.values()]
        self.action = self.brain.update(reward, state)
        turn = ACTION2COMMAND[self.action]

      
        self.turn = turn
        self.move = min(max(self.move, -1), 1)
        self.turn = min(max(self.turn, -1), 1)
        self.STDSCR.addstr(self.scrline + 4, 0, f'Reward:{reward:.2f} Learn score:{self.brain.learn_score:.2f}')        


    def printSensors(self, label, line, sensors):
        str=""
        for key, distance in sensors.items():
                str+=f'{label}{key}: {distance:2f} '
        self.STDSCR.addstr(line, 0, str)

    def processEvent(self, event):
        pass