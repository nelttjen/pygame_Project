import pygame as pg

class KeyboardController:
    def __init__(self, boat, left, right, up, down):
        self.left, self.right, self.up, self.down = left, right, up, down
        self.turn = 0
        self.move = 0
        self.boat = boat
    
    def update(self):
        lap = self.boat.update(self.move, self.turn)
        return lap

    def processEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == self.left:
                self.turn = -1
            elif event.key == self.right:
                self.turn = 1
            elif event.key == self.up:
                self.move = 1
            elif event.key == self.down:
                self.move = -1
        if event.type == pg.TEXTINPUT:
            if event.text == self.left:
                self.turn = -1
            elif event.text == self.right:
                self.turn = 1
            elif event.text == self.up:
                self.move = 1
            elif event.text == self.down:
                self.move = -1
        if event.type == pg.KEYUP:
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

