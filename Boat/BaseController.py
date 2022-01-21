import curses
import Config
from pymunk.vec2d import Vec2d
import time

STDSCR = curses.initscr()
curses.start_color()
curses.use_default_colors()
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
curses.endwin()


class BaseController:
    STDSCR = STDSCR

    def __init__(self, boat, level):
        self.boatsSensors = {}
        self.shoreSensors = {}
        self.level = level
        self.boat = boat
        self.next_checkpoint = -1
        self.move_back_time = 0

        self.boat.stability *= 2
        self.boat.power *= 1.5
        self.boat.FF = -1
        self.boat.streamlining /= 2

        boat.radarCallbacks[Config.Collisiontypes.BOAT].append(self.update_boat_sensors)
        boat.radarCallbacks[Config.Collisiontypes.SHORE].append(self.update_shore_sensors)
        self.count = -1
        self.body = self.boat.car_shape.body

        SCRLINE = 0
        self.scrline = SCRLINE
        SCRLINE += 5

        self.turn = 0
        self.move = 0
        self.dxy = None
        self.orientationA = None
        self.min_distance = None
        self.move_time = None
        self.last_distance = None

    def update_boat_sensors(self, distance, tag, _):
        self.boatsSensors[tag] = distance

    def update_shore_sensors(self, distance, tag, _):
        self.shoreSensors[tag] = distance

    def update_child(self):
        pass

    def update(self):
        self.count += 1
        x, y = self.boat.get_position()
        dx, dy = self.boat.next_checkpoint_x - x, self.boat.next_checkpoint_y - y
        self.dxy = Vec2d(dx, dy)
        self.orientationA = self.body.rotation_vector.get_angle_between(self.dxy)

        self.update_child()
        if self.move_back_time > time.time():
            self.boat.update(-self.move, self.turn)
        else:
            if self.boat.next_checkpoint != self.next_checkpoint:
                self.next_checkpoint = self.boat.next_checkpoint
                self.min_distance = self.dxy.length
                self.move_time = time.time()
            else:
                if self.min_distance > self.dxy.length:
                    self.min_distance = self.dxy.length
                    self.move_time = time.time()
                else:
                    if time.time() - self.move_time > 5:
                        self.move_back_time = time.time() + 5
        self.boat.update(self.move, self.turn)
        self.last_distance = self.dxy.length
        if Config.Screen.DEBUG:
            self.STDSCR.addstr(self.scrline + 0, 0,
                               f'X:{x:.2f} Y:{y:.2f} GoalCP: {self.next_checkpoint} '
                               f'GoalX:{self.boat.next_checkpoint_x:.2f} '
                               f'GoalY:{self.boat.next_checkpoint_y:.2f} '
                               f'Force:{self.move:.2f} Turn:{self.turn:.2f}',
                               curses.color_pair(1))
            self.STDSCR.addstr(self.scrline + 1, 0,
                               f'OrientationA:{self.orientationA:.2f} '
                               f'Angular speed:{self.body.angular_velocity:.2f}')
            self.print_sensors("Shore", self.scrline + 2, self.shoreSensors)
            self.print_sensors("Boat", self.scrline + 3, self.boatsSensors)
            self.STDSCR.refresh()

    def print_sensors(self, label, line, sensors):
        strng = ""
        for key, distance in sensors.items():
            strng += f'{label}{key}: {distance:2f} '
        self.STDSCR.addstr(line, 0, strng)

    def process_event(self, event):
        pass
