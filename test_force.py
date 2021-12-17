from math import cos, sin
import pygame
from random import randrange, triangular
from pygame.event import event_name
import pymunk.pygame_util
import pymunk
import os
import sys

def draw_wall(x, y, x2, y2):
    c = [[x, y, x2, y], [x2, y, x2, y2], [x2, y2, x, y2], [x, y2, x, y]]
    for i in c:
        segment_shape = pymunk.Segment(
            space.static_body, (i[0], i[1]), (i[2], i[3]), 26)
        space.add(segment_shape)
        segment_shape.elasticity = 0.8
        segment_shape.friction = 1.0
    return space

class Boat:
    def __init__(self):
        self.fps = 60
        car_mass = 0.5
        self.old_position_x = self.old_position_y = 100
        self.turn, self.move = 0, 0
        self.translation = pymunk.Transform()

        self.car_shape = pymunk.Poly.create_box(None, size=(100, 60))
        self.car_shape.color = [randrange(256) for i in range(4)]
        car_moment = pymunk.moment_for_poly(car_mass/5, self.car_shape.get_vertices())
        self.car_shape.body = pymunk.Body(car_mass, car_moment)
        self.car_shape.body.position = (100, 100)
        self.car_shape.body.angle = -1
        space.add(self.car_shape, self.car_shape.body)


class Player_Boat(Boat):
    def __init__(self, left, right, up, down):
        super().__init__()
        self.left, self.right, self.up, self.down = left, right, up, down
    
    def update(self, event):
        angularForce = 1*self.car_shape.body.angular_velocity
        self.car_shape.body.apply_force_at_local_point((0, angularForce), (-50, 0))
        self.car_shape.body.apply_force_at_local_point((0, -angularForce), (50, 0))
        # компенсация заноса
        angle = self.car_shape.body.angle
        velocity = self.car_shape.body.velocity.rotated(-angle)
        self.car_shape.body.apply_force_at_local_point((0, 1*-velocity.y))
        # естественное торможение
        self.car_shape.body.apply_force_at_local_point((0.1*-velocity.x, 0))
        # мотор
        self.car_shape.body.apply_force_at_local_point((10*self.move, 3*self.turn), (-50, 0))
        space.step(1 / self.fps)
        space.debug_draw(draw_options)
        if event.type == pygame.KEYDOWN:
            if event.key == self.left:
                self.turn = -1
            elif event.key == self.right:
                self.turn = 1
            elif event.key == self.up:
                self.move = 1
            elif event.key == self.down:
                self.move = -1
        if event.type == pygame.TEXTINPUT:
            if event.text == self.left:
                self.turn = -1
            elif event.text == self.right:
                self.turn = 1
            elif event.text == self.up:
                self.move = 1
            elif event.text == self.down:
                self.move = -1
        if event.type == pygame.KEYUP:
            if event.key in [self.left, self.right]:
                self.turn = 0
            if event.key in [self.up, self.down]:
                self.move = 0
        self.translation = self.translation.translated(
            self.old_position_x - self.car_shape.body.position.x,
            self.old_position_y - self.car_shape.body.position.y,
        )
        self.old_position_x = self.car_shape.body.position.x
        self.old_position_y = self.car_shape.body.position.y

    def camera(self):
        # зум камеры
        scaling = 1

        draw_options.transform = (
            pymunk.Transform.translation(300, 300)
            @ pymunk.Transform.scaling(scaling)
            @ self.translation
            @ pymunk.Transform.rotation(0)
            @ pymunk.Transform.translation(-300, -300)
        )

def main():
    pymunk.pygame_util.positive_y_is_up = False

    RES = WIDTH, HEIGHT = 2000, 2000
    FPS = 60

    pygame.init()
    surface = pygame.display.set_mode((900, 720))
    clock = pygame.time.Clock()
    global draw_options
    draw_options = pymunk.pygame_util.DrawOptions(surface)

    global space
    space = pymunk.Space()
    space.gravity = 0, 0

    space = draw_wall(0, 0, WIDTH, HEIGHT)
    space = draw_wall(WIDTH / 3, HEIGHT / 3, WIDTH - WIDTH / 3, HEIGHT - HEIGHT / 3)

    running = True

    c = Player_Boat(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)
    c2 = Player_Boat('a', 'd', 'w', 's')
    while running:
        pygame.display.flip()
        clock.tick(FPS)
        surface.fill(pygame.Color('black'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        c.update(event)
        c2.update(event)
        c.camera()
        
    pygame.quit()
if __name__ == '__main__':
    main()
