import pygame
from pygame.draw import rect
from pygame.image import load
from Config import Specifications
from Utills.utils import load_image
import sys

from Config import Tracks
from peewee import *

from database import Records

from Config import Levels

number = 0
number_yacht = 0
class Back(Exception):
    pass


class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, image2, x, y, tag, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image(image), (50, 50))
        self.image1 = self.image
        self.image2 = pygame.transform.scale(load_image(image2), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tag = tag
    
    def update_image(self, number):
        if self.tag == 1:
            if number != len(Specifications.BOATS):
                self.image = self.image1
            else:
                self.image = self.image2
        elif self.tag == -1:
            if number != 1:
                self.image = self.image1
            else:
                self.image = self.image2

    def update(self, *args):
        global number
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and args[0].button == 1:
            if self.tag == 1:
                if number != len(Tracks.TRACKS):
                    number += 1
            elif self.tag == -1:
                if number != 1:
                    number -= 1
        self.update_image(number)


class Cross(pygame.sprite.Sprite):
    def __init__(self, image, x, y, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image(image), (50, 48))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = type

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and args[0].button == 1:
            sys.exit()


class Back(pygame.sprite.Sprite):
    def __init__(self, image, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image(image), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.type = type

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and args[0].button == 1:
            raise Back


class Yacht(pygame.sprite.Sprite):
    def __init__(self, image, x, y, sizex, sizey, tag, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image(image), (sizex, sizey))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tag = tag

    def update(self, *args):
        global number_yacht
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos) and args[0].button == 1:
            number_yacht = self.tag


class Table_records:
    def start(self):
        global number
        global number_yacht
        boat = Specifications.BOATS

        db = SqliteDatabase('yacht.db')

        pygame.init()
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        width, height = screen.get_size()
        running = True
        rect_color = pygame.Color('green')
        count_yacht = len(boat) + 1
        f1 = pygame.font.Font('fonts/8289.otf', 50)
        number = 1
        text = 'Track 1'
        all_sprites = pygame.sprite.Group()

        checkmark = pygame.transform.scale(load_image("checkmark.png"), (width / count_yacht, width / count_yacht / 3))
        Arrow("rightarrowopaque.png", "rightarrowtransparent.png", width / 2 + 150, 50, 1, all_sprites)
        Arrow("leftarrowopaque.png", "leftarrowtransparent.png", width / 2 - 200, 50, -1, all_sprites)
        Cross("cross.png", width - 50, 0, all_sprites)
        Back("arrow.png", all_sprites)
        for i in range(count_yacht - 1):
            Yacht(boat[i][1], width / count_yacht * (i + 1), height / 15 * 2, width / count_yacht, width / count_yacht / 3, i + 1, all_sprites)
        Yacht("nothing.png", 0, height / 15 * 2, width / count_yacht, width / count_yacht / 3, 0, all_sprites)
        
        rast = height / 15

        images_yacht = {'yacht_1.png': (pygame.transform.scale(load_image("yacht_1.png"), (width / 5, height / 15)), 1),
                        'yacht_2.png': (pygame.transform.scale(load_image("yacht_2.png"), (width / 5, height / 15)), 2),
                        'yacht_3.png': (pygame.transform.scale(load_image("yacht_3.png"), (width / 5, height / 15)), 3),
                        'yacht_4.png': (pygame.transform.scale(load_image("yacht_4.png"), (width / 5, height / 15)), 4),
                        'yacht_5.png': (pygame.transform.scale(load_image("yacht_5.png"), (width / 5, height / 15)), 5),
                        'yacht_6.png': (pygame.transform.scale(load_image("yacht_6.png"), (width / 5, height / 15)), 6),}
        while running:
            #screen.fill((50, 80, 200))
            fon = pygame.transform.scale(load_image(Tracks.TRACKS[number-1][0]), (width, height))
            screen.blit(fon, (0, 0))
            screen.fill((45, 45, 45), special_flags=8)
            all_sprites.draw(screen)
            
            for event in pygame.event.get():
                all_sprites.update(event)
                if event.type == pygame.QUIT:
                    running = False
            for i in range(count_yacht + 1):
                pygame.draw.rect(screen, rect_color, (width / count_yacht * i, height / 15 * 2, width / count_yacht, width / count_yacht / 3), 4)
            for i in range(10):
                for j in range(3):
                    pygame.draw.rect(screen, rect_color, ((width / 5) * (j + 1), rast * (i + 4), width / 5, height / 15), 4)
            count = 5
            text1, text2, text3 = 'Имя', 'Яхта', 'Очки'
            screen.blit(f1.render(text1, True, (30, 250, 250)), ((width / 5) * 1, rast * 4))
            screen.blit(f1.render(text2, True, (30, 250, 250)), ((width / 5) * 2, rast * 4))
            screen.blit(f1.render(text3, True, (30, 250, 250)), ((width / 5) * 3, rast * 4))
            for i in Records.select().order_by(Records.points.desc()):
                if i.track == number and (number_yacht == 0 or number_yacht == images_yacht[i.yacht][1]):
                    text1, text2, text3 = i.name, images_yacht[i.yacht][0], str(i.points)
                    screen.blit(f1.render(text1, True, (250, 250, 30)), ((width / 5) * 1, rast * count))
                    screen.blit(text2, ((width / 5) * 2, rast * count))
                    screen.blit(f1.render(text3, True, (250, 250, 30)), ((width / 5) * 3, rast * count))
                    count += 1
                    if count > 13:
                        break
            text = f'Track {number}'
            screen.blit(f1.render(text, True, (250, 250, 30)), (width / 2 - 100, 50))
            screen.blit(checkmark, (number_yacht * width / count_yacht, height / 15 * 2))
            pygame.display.flip()
        pygame.quit()

#w = Table_records().start()
