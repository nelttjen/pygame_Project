from typing import Tuple

from Utills.utils import DelayedUpdate


class Camera:
    screen_size: Tuple[int, int]
    level_size: Tuple[int, int]

    def __init__(self, level_size: Tuple[int, int], screen_size: Tuple[int, int]):
        self.screen_size = screen_size
        self.level_size = level_size
        self.min_scale = max(screen_size[0] / level_size[0], screen_size[1] / level_size[1])
        self.scalingUpdate = DelayedUpdate(k=0.01)
        self.cameraXUpdate = DelayedUpdate(initial=0, k=0.1)
        self.cameraYUpdate = DelayedUpdate(initial=0, k=0.1)
        self.max_speed = 300

    def update(self, x, y, v) -> Tuple[Tuple[int, int], Tuple[float, float], float]:
        (cx, _) = self.cameraXUpdate.update(x)
        (cy, _) = self.cameraYUpdate.update(y)
        if v > self.max_speed:
            self.max_speed = v
        # v=1000

        (scaling, _) = self.scalingUpdate.update(1 - (abs(v) / self.max_speed))
        scaling = max(self.min_scale, scaling)

        wx = self.screen_size[0] / scaling
        wy = self.screen_size[1] / scaling

        cx = max(0, min(int(self.level_size[0] - wx), x - wx / 2))
        cy = max(0, min(int(self.level_size[1] - wy), y - wy / 2))
        # зум камеры

        return (cx, cy), (wx, wy), scaling
