import curses
from config import Collisiontypes
from pymunk.vec2d import Vec2d

STDSCR = curses.initscr()
curses.start_color()
curses.use_default_colors()
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)


global SCRLINE
SCRLINE = 0

class BaseController:
    STDSCR = STDSCR
    def __init__(self, boat, level):
        self.boatsSensors = {}
        self.shoreSensors = {}
        self.level = level
        self.boat = boat

        boat.radarCallbacks[Collisiontypes.BOAT].append(self.updateBoatSensors)
        boat.radarCallbacks[Collisiontypes.SHORE].append(self.updateShoreSensors)
        self.count = -1
        self.body = self.boat.car_shape.body

        global SCRLINE
        self.scrline = SCRLINE
        SCRLINE += 5
    
    def updateBoatSensors(self, distance, tag, _):
        self.boatsSensors[tag] = distance
    
    def updateShoreSensors(self, distance, tag, _):
        self.shoreSensors[tag] = distance

    def updateChild(self):
        pass

    def update(self):
        self.count+=1
        x, y = self.boat.get_position()
        dx, dy = self.boat.next_checkpoint_x - x, self.boat.next_checkpoint_y - y
        self.dxy = Vec2d(dx,dy)
        self.orientationA = self.body.rotation_vector.get_angle_between(self.dxy)

        self.updateChild()

        self.boat.update(self.move, self.turn)
        self.lastDistance = self.dxy.length

        self.STDSCR.addstr(self.scrline + 0, 0, f'X:{x:.2f} Y:{y:.2f} GoalX:{self.boat.next_checkpoint_x:.2f} GoalY:{self.boat.next_checkpoint_y:.2f} Force:{self.move:.2f} Turn:{self.turn:.2f}', curses.color_pair(1))
        self.STDSCR.addstr(self.scrline + 1, 0, f'OrientationA:{self.orientationA:.2f} Angular speed:{self.body.angular_velocity:.2f}')
        self.printSensors("Shore", self.scrline + 2, self.shoreSensors)
        self.printSensors("Boat", self.scrline + 3, self.boatsSensors)
        self.STDSCR.refresh()


    def printSensors(self, label, line, sensors):
        str=""
        for key, distance in sensors.items():
                str+=f'{label}{key}: {distance:2f} '
        self.STDSCR.addstr(line, 0, str)

    def processEvent(self, event):
        pass