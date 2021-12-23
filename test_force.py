from math import cos, sin
import math
import pygame
from random import randint, randrange, triangular
from pygame.event import event_name
import pymunk.pygame_util
import pymunk
import os
import sys
from pymunk import Vec2d


def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    if not os.path.isfile(fullname):
        print("Файл не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def draw_wall(x, y, x2, y2):
    c = [[x, y, x2, y], [x2, y, x2, y2], [x2, y2, x, y2], [x, y2, x, y]]
    for i in c:
        segment_shape = pymunk.Segment(
            space.static_body, (i[0], i[1]), (i[2], i[3]), 26
        )
        space.add(segment_shape)
        segment_shape.elasticity = 0.8
        segment_shape.friction = 1.0
    return space


class Boat:
    def __init__(self, x):
        self.fps = 60
        car_mass = 0.5
        self.old_position_x = self.old_position_y = x
        self.turn, self.move = 0, 0

        self.car_shape = pymunk.Poly.create_box(None, size=(100, 60))
        self.car_shape.color = [0 for i in range(4)]
        car_moment = pymunk.moment_for_poly(car_mass / 5, self.car_shape.get_vertices())
        self.car_shape.body = pymunk.Body(car_mass, car_moment)
        self.car_shape.body.position = (x, x)
        self.car_shape.body.angle = 0
        space.add(self.car_shape, self.car_shape.body)


class Player_Boat(Boat):
    def __init__(self, x, left, right, up, down):
        super().__init__(x)
        self.left, self.right, self.up, self.down = left, right, up, down
        self.logo_img = load_image("yacht.png")
        global translation

    def update(self, event):
        angularForce = 1 * self.car_shape.body.angular_velocity
        self.car_shape.body.apply_force_at_local_point((0, angularForce), (-50, 0))
        self.car_shape.body.apply_force_at_local_point((0, -angularForce), (50, 0))
        # компенсация заноса
        angle = self.car_shape.body.angle
        velocity = self.car_shape.body.velocity.rotated(-angle)
        self.car_shape.body.apply_force_at_local_point((0, 1 * -velocity.y))
        # естественное торможение
        self.car_shape.body.apply_force_at_local_point((0.1 * -velocity.x, 0))
        # мотор
        self.car_shape.body.apply_force_at_local_point(
            (10 * self.move, 3 * self.turn), (-50, 0)
        )
        space.step(1 / self.fps)
        space.debug_draw(draw_options)
        self.p = (
            self.car_shape.body.position.x + translation.tx,
            self.car_shape.body.position.y + translation.ty,
        )
        angle_degrees = math.degrees(self.car_shape.body.angle)
        self.rotated_logo_img = pygame.transform.rotate(self.logo_img, -angle_degrees)

        offset = Vec2d(*self.rotated_logo_img.get_size()) / 2
        self.p = self.p - offset

        surface.blit(self.rotated_logo_img, (round(self.p.x), round(self.p.y)))
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
            if event.key in [self.left, self.right] or event.unicode in [
                self.left,
                self.right,
            ]:
                self.turn = 0
            if event.key in [self.up, self.down] or event.unicode in [
                self.up,
                self.down,
            ]:
                self.move = 0

    def camera(self):
        global translation
        translation = translation.translated(
            self.old_position_x - self.car_shape.body.position.x,
            self.old_position_y - self.car_shape.body.position.y,
        )
        self.old_position_x = self.car_shape.body.position.x
        self.old_position_y = self.car_shape.body.position.y
        # зум камеры
        scaling = 1
        draw_options.transform = (
            pymunk.Transform.translation(300, 300)
            @ pymunk.Transform.scaling(scaling)
            @ translation
            @ pymunk.Transform.rotation(0)
            @ pymunk.Transform.translation(-300, -300)
        )
        surface.blit(self.rotated_logo_img, (round(self.p.x), round(self.p.y)))


def main():
    pymunk.pygame_util.positive_y_is_up = False

    RES = WIDTH, HEIGHT = 2000, 2000
    FPS = 60

    pygame.init()
    global surface
    surface = pygame.display.set_mode((920, 700))
    clock = pygame.time.Clock()
    global draw_options
    draw_options = pymunk.pygame_util.DrawOptions(surface)

    global space
    space = pymunk.Space()
    space.gravity = 0, 0

    global translation
    translation = pymunk.Transform()

    space = draw_wall(0, 0, WIDTH, HEIGHT)
    space = draw_wall(WIDTH / 3, HEIGHT / 3, WIDTH - WIDTH / 3, HEIGHT - HEIGHT / 3)

    running = True

    c = Player_Boat(100, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)
    c2 = Player_Boat(200, "a", "d", "w", "s")

    while running:
        pygame.display.flip()
        clock.tick(FPS)
        surface.fill(pygame.Color("black"))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        c.update(event)
        c2.update(event)
        c.camera()

    pygame.quit()


if __name__ == "__main__":
    main()
