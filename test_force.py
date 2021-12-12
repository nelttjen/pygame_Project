from math import cos, sin
import pygame as pg
from random import randrange
from pygame.event import event_name
import pymunk.pygame_util
import pymunk

pymunk.pygame_util.positive_y_is_up = False

RES = WIDTH, HEIGHT = 2000, 2000
FPS = 60


pg.init()
surface = pg.display.set_mode((900, 720))
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)

space = pymunk.Space()
space.gravity = 0, 0


def draw_wall(x, y, x2, y2):
    c = [[x, y, x2, y], [x2, y, x2, y2], [x2, y2, x, y2], [x, y2, x, y]]
    for i in c:
        segment_shape = pymunk.Segment(
            space.static_body, (i[0], i[1]), (i[2], i[3]), 26)
        space.add(segment_shape)
        segment_shape.elasticity = 0.8
        segment_shape.friction = 1.0


draw_wall(0, 0, WIDTH, HEIGHT)
draw_wall(WIDTH / 3, HEIGHT / 3, WIDTH - WIDTH / 3, HEIGHT - HEIGHT / 3)
car_mass = 0.5

car_shape = pymunk.Poly.create_box(None, size=(100, 60))
car_shape.color = [randrange(256) for i in range(4)]
car_moment = pymunk.moment_for_poly(car_mass/5, car_shape.get_vertices())
car_shape.body = pymunk.Body(car_mass, car_moment)
car_shape.body.position = (100, 100)
car_shape.body.angle = -1
space.add(car_shape, car_shape.body)

RIGHT = "to the right"
LEFT = "to the left"
STOP = "stop"   
UP = "up"
DOWN = "down"

motion = STOP
motion2 = STOP

translation = pymunk.Transform()
scaling = 1

old_position_x = old_position_y = 100

turn, move = 0, 0
while True:
    pg.display.flip()
    clock.tick(FPS)

    surface.fill(pg.Color('black'))

# компенсация вращения
    angularForce = 1*car_shape.body.angular_velocity
    car_shape.body.apply_force_at_local_point((0, angularForce), (-50, 0))
    car_shape.body.apply_force_at_local_point((0, -angularForce), (50, 0))
# компенсация заноса
    angle = car_shape.body.angle
    velocity = car_shape.body.velocity.rotated(-angle)
    car_shape.body.apply_force_at_local_point((0, 1*-velocity.y))
# естественное торможение
    car_shape.body.apply_force_at_local_point((0.1*-velocity.x, 0))
# мотор
    car_shape.body.apply_force_at_local_point((10*move, 3*turn), (-50, 0))
    space.step(1 / FPS)
    space.debug_draw(draw_options)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                motion = LEFT
                turn = -1
            elif event.key == pg.K_RIGHT:
                motion = RIGHT
                turn = 1
            elif event.key == pg.K_UP:
                motion = UP
                move = 1
            elif event.key == pg.K_DOWN:
                motion2 = DOWN
                move = -1
        elif event.type == pg.KEYUP:
            if event.key in [pg.K_LEFT, pg.K_RIGHT]:
                motion = STOP
                turn = 0
            if event.key in [pg.K_UP, pg.K_DOWN]:
                motion2 = STOP
                move = 0

# позиция камеры
    translation = translation.translated(
        old_position_x - car_shape.body.position.x,
        old_position_y - car_shape.body.position.y,
    )
    old_position_x = car_shape.body.position.x
    old_position_y = car_shape.body.position.y

# зум камеры
    scaling = 1

    draw_options.transform = (
        pymunk.Transform.translation(300, 300)
        @ pymunk.Transform.scaling(scaling)
        @ translation
        @ pymunk.Transform.rotation(0)
        @ pymunk.Transform.translation(-300, -300)
    )
