from Boat.BaseController import BaseController
from Boat.RadarManager import Radar


class SimpleController(BaseController):

    def updateChild(self):

        self.turn = -self.orientationA
        if (abs(self.orientationA) < 1.5):
            self.move = 1
        else:
            self.move = 0
        kshore = 10
        kboat = 5
        if self.move > 0:
            self.turn += kshore * (1 - self.shoreSensors[Radar.RIGTH])
            self.turn -= kshore * (1 - self.shoreSensors[Radar.LEFT])
            self.move -= 3 * (1 - self.shoreSensors[Radar.FRONT])
            self.turn += kboat * (1 - self.boatsSensors[Radar.RIGTH])
            self.turn -= kboat * (1 - self.boatsSensors[Radar.LEFT])
            self.move -= kboat * (1 - self.boatsSensors[Radar.FRONT])
        if self.move < 0:
            self.move += kshore * (1 - self.shoreSensors[Radar.BACK])
            self.move += kshore * (1 - self.boatsSensors[Radar.BACK])

    def processEvent(self, event):
        pass
