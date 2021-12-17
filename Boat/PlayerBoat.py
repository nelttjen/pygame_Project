import pymunk.pygame_util
import pygame as pg

from Boat.BaseBoat import BaseBoat


class PlayerBoat(BaseBoat):
    def __init__(self, left, right, up, down, app, scaling=1):
        super().__init__(app)
        self.left, self.right, self.up, self.down = left, right, up, down
        self.draw_options = pymunk.pygame_util.DrawOptions(self.app.screen)

        self.scaling = scaling

    def update(self, events):
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
        self.car_shape.body.apply_force_at_local_point((10 * self.move, 3 * self.turn), (-50, 0))
        self.app.space.step(1 / self.FPS)
        self.app.space.debug_draw(self.draw_options)
        for event in events:
            if event.type == pg.KEYDOWN or event.type == pg.TEXTINPUT:
                if (event.key if event.type == pg.KEYDOWN else event.text) == self.left:
                    self.turn = -1
                elif (event.key if event.type == pg.KEYDOWN else event.text) == self.right:
                    self.turn = 1
                elif (event.key if event.type == pg.KEYDOWN else event.text) == self.up:
                    self.move = 1
                elif (event.key if event.type == pg.KEYDOWN else event.text) == self.down:
                    self.move = -1
            if event.type == pg.KEYUP:
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
        scaling = self.scaling

        self.draw_options.transform = (
                pymunk.Transform.translation(300, 300)
                @ pymunk.Transform.scaling(scaling)
                @ self.translation
                @ pymunk.Transform.rotation(0)
                @ pymunk.Transform.translation(-300, -300)
        )
