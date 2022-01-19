from Utills.utils import DelayedUpdate
import pymunk


class Camera:
    def __init__(self):
        self.scalingUpdate = DelayedUpdate()
        self.cameraXUpdate = DelayedUpdate(initial=0, k=0.1)
        self.cameraYUpdate = DelayedUpdate(initial=0, k=0.1)
    
    def update(self, x, y, v):
        (cx, _) = self.cameraXUpdate.update(x)
        (cy, _) = self.cameraYUpdate.update(y)
        # зум камеры
        (scaling, _) = self.scalingUpdate.update(0.05) # 1 - (abs(v) / 250))
        return -cx, -cy, scaling
