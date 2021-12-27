from math import cos, sin
import pygame as pg
from random import randint, randrange, triangular
from pygame.event import event_name
import pymunk.pygame_util
import pymunk
from Boat.Camera import Camera
from Boat.PlayerBoat import PlayerBoat
from Boat.levelBuilder import SandBox

def main():
    pymunk.pygame_util.positive_y_is_up = False

    FPS = 60

    pg.init()

    surface = pg.display.set_mode((920, 700))
    clock = pg.time.Clock()    
    draw_options = pymunk.pygame_util.DrawOptions(surface)

    space = pymunk.Space()
    space.gravity = 0, 0

    c = PlayerBoat(space, pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN)
    c2 = PlayerBoat(space, "a", "d", "w", "s")

    level = SandBox()
    level.build(space)
    level.arrangeBoats([c, c2])

    camera = Camera()

    while True:
        pg.display.flip()
        clock.tick(FPS)
        surface.fill(pg.Color("black"))
        for event in pg.event.get():
            if event.type == pg.QUIT:
               break
            c.processEvent(event)
            c2.processEvent(event)
        else:
            playerX, playerY, playerVelocity = c.update()
            c2.update()
            cx, cy, scaling = camera.update(playerX-300, playerY-300, playerVelocity)
            space.step(1 /FPS)
            draw_options.transform = (
                pymunk.Transform.scaling(scaling)
                @ pymunk.Transform(tx=cx, ty=cy)
            )
            space.debug_draw(draw_options)
            c.updateImage(surface, cx, cy, scaling)
            c2.updateImage(surface, cx, cy, scaling)
            continue
        break
    pg.quit()


if __name__ == "__main__":
    main()
