from Boat.RadarManager import Radar
from config import Collisiontypes
from pymunk.vec2d import Vec2d

class SimpleController:
    action2command = [(-1,1), (1,1), (1,0), (-1,0)]
    def __init__(self, boat, level):
        self.boatsSensors = {}
        self.shoreSensors = {}
        self.level = level
        self.boat = boat

        boat.radarCallbacks[Collisiontypes.BOAT].append(self.updateBoatSensors)
        boat.radarCallbacks[Collisiontypes.SHORE].append(self.updateShoreSensors)
        self.count = -1
    
    def updateBoatSensors(self, distance, tag, _):
        self.boatsSensors[tag] = distance
    
    def updateShoreSensors(self, distance, tag, _):
        self.shoreSensors[tag] = distance

    def update(self):
        self.count+=1
        if self.count % 1 == 0 :
            x, y = self.boat.get_position()
            dx, dy = self.boat.next_checkpoint_x - x, self.boat.next_checkpoint_y - y
            dxy = Vec2d(dx,dy)

            body = self.boat.car_shape.body
            orientationV = body.velocity.get_angle_between(dxy)
            orientationA = body.rotation_vector.get_angle_between(dxy)
            self.turn = -orientationA
            if(abs(orientationA)<1.5):
                self.move = 1
            else:
                self.move = 0
            if self.move == 1:
                self.turn+= 2*(1-self.shoreSensors[Radar.RIGTH])
                self.turn-= 2*(1-self.shoreSensors[Radar.LEFT])
                self.move -= 2*(1-self.shoreSensors[Radar.FRONT])
                self.turn+= 2*(1-self.boatsSensors[Radar.RIGTH])
                self.turn-= 2*(1-self.boatsSensors[Radar.LEFT])
                self.move -= 2*(1-self.boatsSensors[Radar.FRONT])

        self.boat.update(self.move, self.turn)

    def printSensors(self, label, line, sensors):
        str=""
        for key, distance in sensors.items():
                str+=f'{label}{key}: {distance:2f} '
        self.stdscr.addstr(line, 0, str)

    def processEvent(self, event):
        pass