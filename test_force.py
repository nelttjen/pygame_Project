from math import cos, sin
import pygame as pg
from random import randrange
from pygame.event import event_name
import pymunk.pygame_util
import pymunk

pymunk.pygame_util.positive_y_is_up = False

RES = WIDTH, HEIGHT = 900, 720
FPS = 60


pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)

space = pymunk.Space()
space.gravity = 0, 0

segment_shape = pymunk.Segment(space.static_body, (2, HEIGHT), (WIDTH, HEIGHT), 26)
space.add(segment_shape)
segment_shape.elasticity = 0.8
segment_shape.friction = 1.0

segment_shape = pymunk.Segment(space.static_body, (WIDTH / 4, 0), (WIDTH / 4, HEIGHT), 26)
space.add(segment_shape)
segment_shape.elasticity = 0.8
segment_shape.friction = 1.0

segment_shape = pymunk.Segment(space.static_body, (WIDTH / 4 * 3, 0), (WIDTH / 4 * 3, HEIGHT), 26)
space.add(segment_shape)
segment_shape.elasticity = 0.8
segment_shape.friction = 1.0

segment_shape = pymunk.Segment(space.static_body, (2, 0), (WIDTH, 0), 26)
space.add(segment_shape)
segment_shape.elasticity = 0.8
segment_shape.friction = 1.0

car_mass = 0.5

car_shape = pymunk.Poly.create_box(None, size=(100, 60))
car_shape.color = [randrange(256) for i in range(4)]
car_moment = pymunk.moment_for_poly(car_mass/5, car_shape.get_vertices())
car_shape.body = pymunk.Body(car_mass, car_moment)
car_shape.body.position = (400, 300)
car_shape.body.angle = -1
space.add(car_shape, car_shape.body)

RIGHT = "to the right"
LEFT = "to the left"
STOP = "stop"
UP = "up"
DOWN = "down"

motion = STOP
motion2 = STOP

turn, move = 0, 0
while True:
    pg.display.flip()
    clock.tick(FPS)

    surface.fill(pg.Color('black'))

#компенсация вращения
    angularForce = 1*car_shape.body.angular_velocity
    car_shape.body.apply_force_at_local_point((0, angularForce), (-50, 0))
    car_shape.body.apply_force_at_local_point((0, -angularForce), (50, 0))
#компенсация заноса
    angle = car_shape.body.angle
    velocity = car_shape.body.velocity.rotated(-angle)
    car_shape.body.apply_force_at_local_point((0, 1*-velocity.y))
#естественное торможение
    car_shape.body.apply_force_at_local_point((0.1*-velocity.x, 0))
#мотор
    car_shape.body.apply_force_at_local_point((10*move, 3*turn), (-50, 0))
    space.step(1 / FPS)
    space.debug_draw(draw_options)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()        
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                create_square(space, event.pos)
                print(event.pos)
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
