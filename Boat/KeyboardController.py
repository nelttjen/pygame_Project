import pygame as pg

class KeyboardController:
    def __init__(self, boat, left, right, up, down):
        self.left, self.right, self.up, self.down = left, right, up, down
        self.boat = boat

    def processEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == self.left:
                self.boat.turn = -1
            elif event.key == self.right:
                self.boat.turn = 1
            elif event.key == self.up:
                self.boat.move = 1
            elif event.key == self.down:
                self.boat.move = -1
        if event.type == pg.TEXTINPUT:
            if event.text == self.left:
                self.boat.turn = -1
            elif event.text == self.right:
                self.boat.turn = 1
            elif event.text == self.up:
                self.boat.move = 1
            elif event.text == self.down:
                self.boat.move = -1
        if event.type == pg.KEYUP:
            if event.key in [self.left, self.right] or event.unicode in [   
                self.left,
                self.right,
            ]:
                self.boat.turn = 0
            if event.key in [self.up, self.down] or event.unicode in [
                self.up,
                self.down,
            ]:
                self.boat.move = 0

