import pygame
import sys
import Config
from Utills.utils import load_image


class Startscreen:
    def __init__(self,
                 max_map=4,
                 boat=None):
        res = ['Track 1', 'yacht_1.png']
        if boat is None:
            boat = [['yacht_1.png', 23, 2, 3, 0.1], ['yacht_2.png', 30, 0.5, 17, 0.1], ['yacht_3.png', 10, 1, 5, 0.2], ['yacht_4.png', 10, 1, 5, 0.2], ['yacht_5.png', 10, 1, 5, 0.2], ['yacht_6.png', 10, 1, 5, 0.2]]
        mn = [[80, 'Track 1', (250, 250, 30), (250, 30, 250), 0, 0, 0, 0, 0],
              [210, 'yacht_1.png', (250, 250, 30), (250, 30, 250), 1, 0, 0, 0, 0],
              [410, 'Новая игра', (250, 250, 30), (250, 30, 250), 2, 0, 0, 0, 0],
              [510, 'Таблица рекордов', (250, 250, 30), (250, 30, 250), 3, 0, 0, 0, 0],
              [610, 'Выход', (250, 250, 30), (250, 30, 250), 4, 0, 0, 0, 0]]
        self.boat = {}
        for i in boat:
            self.boat[i[0]] = f'Масса: {i[1]}    ' \
                              f'Мощность двигателя: {i[2]}    ' \
                              f'Обтекаемость: {i[3]}    ' \
                              f'Устойчивость: {i[4]}'
        self.WIDTH = 900
        self.HEIGHT = 720
        self.res = res
        self.mn = mn
        self.max_map = max_map
        self.max_boat = len(self.boat)

    def render(self, screen, font, num_select):
        for i in self.mn:
            if i[1][-4::] != '.png':
                if i[1][:5] != 'Track':
                    if num_select == i[4]:
                        rnd = font.render(i[1], 1, i[3])
                        screen.blit(rnd, rnd.get_rect(center=(self.WIDTH / 2, int(i[0]))))
                        i[5], i[6], i[7], i[8] = rnd.get_rect(center=(self.WIDTH / 2, int(i[0])))
                    else:
                        rnd = font.render(i[1], 1, i[2])
                        screen.blit(rnd, rnd.get_rect(center=(self.WIDTH / 2, int(i[0]))))
                        i[5], i[6], i[7], i[8] = rnd.get_rect(center=(self.WIDTH / 2, int(i[0])))
                else:
                    if num_select == i[4]:
                        rnd = font.render(i[1], 1, i[3])
                        screen.blit(rnd, rnd.get_rect(center=(self.WIDTH / 2, int(i[0]))))
                        i[5], i[6], i[7], i[8] = rnd.get_rect(center=(self.WIDTH / 2, int(i[0])))
                        if self.max_map == 1:
                            leftarrow = pygame.image.load(f'data/leftarrowtransparent.png')
                            leftarrow = pygame.transform.scale(leftarrow, (leftarrow.get_width() // 10,
                                                                           leftarrow.get_height() // 10))
                            leftarrow_rect = leftarrow.get_rect(center=(self.WIDTH / 4, int(i[0])))
                            screen.blit(leftarrow, leftarrow_rect)
                            rightarrow = pygame.image.load(f'data/rightarrowtransparent.png')
                            rightarrow = pygame.transform.scale(rightarrow,
                                                                (rightarrow.get_width() // 10,
                                                                 rightarrow.get_height() // 10))
                            rightarrow_rect = rightarrow.get_rect(center=(self.WIDTH / 4 * 3, int(i[0])))
                            screen.blit(rightarrow, rightarrow_rect)
                        elif i[1][-1] == '1':
                            leftarrow = pygame.image.load(f'data/leftarrowtransparent.png')
                            leftarrow = pygame.transform.scale(leftarrow, (leftarrow.get_width() // 10,
                                                                           leftarrow.get_height() // 10))
                            leftarrow_rect = leftarrow.get_rect(center=(self.WIDTH / 4, int(i[0])))
                            screen.blit(leftarrow, leftarrow_rect)
                            rightarrow = pygame.image.load(f'data/rightarrowopaque.png')
                            rightarrow = pygame.transform.scale(rightarrow,
                                                                (rightarrow.get_width() // 10,
                                                                 rightarrow.get_height() // 10))
                            rightarrow_rect = rightarrow.get_rect(center=(self.WIDTH / 4 * 3, int(i[0])))
                            screen.blit(rightarrow, rightarrow_rect)
                        elif i[1][-1] == str(self.max_map):
                            leftarrow = pygame.image.load(f'data/leftarrowopaque.png')
                            leftarrow = pygame.transform.scale(leftarrow, (leftarrow.get_width() // 10,
                                                                           leftarrow.get_height() // 10))
                            leftarrow_rect = leftarrow.get_rect(center=(self.WIDTH / 4, int(i[0])))
                            screen.blit(leftarrow, leftarrow_rect)
                            rightarrow = pygame.image.load(f'data/rightarrowtransparent.png')
                            rightarrow = pygame.transform.scale(rightarrow,
                                                                (rightarrow.get_width() // 10,
                                                                 rightarrow.get_height() // 10))
                            rightarrow_rect = rightarrow.get_rect(center=(self.WIDTH / 4 * 3, int(i[0])))
                            screen.blit(rightarrow, rightarrow_rect)
                        else:
                            leftarrow = pygame.image.load(f'data/leftarrowopaque.png')
                            leftarrow = pygame.transform.scale(leftarrow, (leftarrow.get_width() // 10,
                                                                           leftarrow.get_height() // 10))
                            leftarrow_rect = leftarrow.get_rect(center=(self.WIDTH / 4, int(i[0])))
                            screen.blit(leftarrow, leftarrow_rect)
                            rightarrow = pygame.image.load(f'data/rightarrowopaque.png')
                            rightarrow = pygame.transform.scale(rightarrow,
                                                                (rightarrow.get_width() // 10,
                                                                 rightarrow.get_height() // 10))
                            rightarrow_rect = rightarrow.get_rect(center=(self.WIDTH / 4 * 3, int(i[0])))
                            screen.blit(rightarrow, rightarrow_rect)
                    else:
                        rnd = font.render(i[1], 1, i[2])
                        screen.blit(rnd, rnd.get_rect(center=(self.WIDTH / 2, int(i[0]))))
                        i[5], i[6], i[7], i[8] = rnd.get_rect(center=(self.WIDTH / 2, int(i[0])))
                        if self.max_map == 1:
                            leftarrow = pygame.image.load(f'data/leftarrowtransparent.png')
                            leftarrow = pygame.transform.scale(leftarrow, (leftarrow.get_width() // 10,
                                                                           leftarrow.get_height() // 10))
                            leftarrow_rect = leftarrow.get_rect(center=(self.WIDTH / 4, int(i[0])))
                            screen.blit(leftarrow, leftarrow_rect)
                            rightarrow = pygame.image.load(f'data/rightarrowtransparent.png')
                            rightarrow = pygame.transform.scale(rightarrow,
                                                                (rightarrow.get_width() // 10,
                                                                 rightarrow.get_height() // 10))
                            rightarrow_rect = rightarrow.get_rect(center=(self.WIDTH / 4 * 3, int(i[0])))
                            screen.blit(rightarrow, rightarrow_rect)
                        elif i[1][-1] == '1':
                            leftarrow = pygame.image.load(f'data/leftarrowtransparent.png')
                            leftarrow = pygame.transform.scale(leftarrow, (leftarrow.get_width() // 10,
                                                                           leftarrow.get_height() // 10))
                            leftarrow_rect = leftarrow.get_rect(center=(self.WIDTH / 4, int(i[0])))
                            screen.blit(leftarrow, leftarrow_rect)
                            rightarrow = pygame.image.load(f'data/rightarrowopaque.png')
                            rightarrow = pygame.transform.scale(rightarrow,
                                                                (rightarrow.get_width() // 10,
                                                                 rightarrow.get_height() // 10))
                            rightarrow_rect = rightarrow.get_rect(center=(self.WIDTH / 4 * 3, int(i[0])))
                            screen.blit(rightarrow, rightarrow_rect)
                        elif i[1][-1] == str(self.max_map):
                            leftarrow = pygame.image.load(f'data/leftarrowopaque.png')
                            leftarrow = pygame.transform.scale(leftarrow, (leftarrow.get_width() // 10,
                                                                           leftarrow.get_height() // 10))
                            leftarrow_rect = leftarrow.get_rect(center=(self.WIDTH / 4, int(i[0])))
                            screen.blit(leftarrow, leftarrow_rect)
                            rightarrow = pygame.image.load(f'data/rightarrowtransparent.png')
                            rightarrow = pygame.transform.scale(rightarrow,
                                                                (rightarrow.get_width() // 10,
                                                                 rightarrow.get_height() // 10))
                            rightarrow_rect = rightarrow.get_rect(center=(self.WIDTH / 4 * 3, int(i[0])))
                            screen.blit(rightarrow, rightarrow_rect)
                        else:
                            leftarrow = pygame.image.load(f'data/leftarrowopaque.png')
                            leftarrow = pygame.transform.scale(leftarrow, (leftarrow.get_width() // 10,
                                                                           leftarrow.get_height() // 10))
                            leftarrow_rect = leftarrow.get_rect(center=(self.WIDTH / 4, int(i[0])))
                            screen.blit(leftarrow, leftarrow_rect)
                            rightarrow = pygame.image.load(f'data/rightarrowopaque.png')
                            rightarrow = pygame.transform.scale(rightarrow,
                                                                (rightarrow.get_width() // 10,
                                                                 rightarrow.get_height() // 10))
                            rightarrow_rect = rightarrow.get_rect(center=(self.WIDTH / 4 * 3, int(i[0])))
                            screen.blit(rightarrow, rightarrow_rect)
            else:
                if num_select == i[4]:
                    font_infoboat = pygame.font.Font('fonts/8289.otf', 18)
                    yacht = pygame.image.load(f'data/{i[1]}')
                    yacht = pygame.transform.scale(yacht, (300, 100))
                    yacht_rect = yacht.get_rect(center=(self.WIDTH / 2, int(i[0])))
                    screen.blit(yacht, yacht_rect)
                    if self.max_boat == 1:
                        leftarrow = pygame.image.load(f'data/leftarrowtransparent.png')
                        leftarrow = pygame.transform.scale(leftarrow, (leftarrow.get_width() // 10,
                                                                       leftarrow.get_height() // 10))
                        leftarrow_rect = leftarrow.get_rect(center=(self.WIDTH / 4, int(i[0])))
                        screen.blit(leftarrow, leftarrow_rect)
                        rightarrow = pygame.image.load(f'data/rightarrowtransparent.png')
                        rightarrow = pygame.transform.scale(rightarrow, (rightarrow.get_width() // 10,
                                                                         rightarrow.get_height() // 10))
                        rightarrow_rect = rightarrow.get_rect(center=(self.WIDTH / 4 * 3, int(i[0])))
                        screen.blit(rightarrow, rightarrow_rect)
                        rnd = font_infoboat.render(self.boat[i[1]], True, i[3])
                        screen.blit(rnd, rnd.get_rect(center=(self.WIDTH / 2, int(i[0]) + 80)))
                    elif i[1] == 'yacht_1.png':
                        leftarrow = pygame.image.load(f'data/leftarrowtransparent.png')
                        leftarrow = pygame.transform.scale(leftarrow, (leftarrow.get_width() // 10,
                                                                       leftarrow.get_height() // 10))
                        leftarrow_rect = leftarrow.get_rect(center=(self.WIDTH / 4, int(i[0])))
                        screen.blit(leftarrow, leftarrow_rect)
                        rightarrow = pygame.image.load(f'data/rightarrowopaque.png')
                        rightarrow = pygame.transform.scale(rightarrow, (rightarrow.get_width() // 10,
                                                                         rightarrow.get_height() // 10))
                        rightarrow_rect = rightarrow.get_rect(center=(self.WIDTH / 4 * 3, int(i[0])))
                        screen.blit(rightarrow, rightarrow_rect)
                        rnd = font_infoboat.render(self.boat[i[1]], True, i[3])
                        screen.blit(rnd, rnd.get_rect(center=(self.WIDTH / 2, int(i[0]) + 80)))
                    elif i[1] == f'yacht_{self.max_boat}.png':
                        leftarrow = pygame.image.load(f'data/leftarrowopaque.png')
                        leftarrow = pygame.transform.scale(leftarrow, (leftarrow.get_width() // 10,
                                                                       leftarrow.get_height() // 10))
                        leftarrow_rect = leftarrow.get_rect(center=(self.WIDTH / 4, int(i[0])))
                        screen.blit(leftarrow, leftarrow_rect)
                        rightarrow = pygame.image.load(f'data/rightarrowtransparent.png')
                        rightarrow = pygame.transform.scale(rightarrow, (rightarrow.get_width() // 10,
                                                                         rightarrow.get_height() // 10))
                        rightarrow_rect = rightarrow.get_rect(center=(self.WIDTH / 4 * 3, int(i[0])))
                        screen.blit(rightarrow, rightarrow_rect)
                        rnd = font_infoboat.render(self.boat[i[1]], True, i[3])
                        screen.blit(rnd, rnd.get_rect(center=(self.WIDTH / 2, int(i[0]) + 80)))
                    else:
                        leftarrow = pygame.image.load(f'data/leftarrowopaque.png')
                        leftarrow = pygame.transform.scale(leftarrow, (leftarrow.get_width() // 10,
                                                                       leftarrow.get_height() // 10))
                        leftarrow_rect = leftarrow.get_rect(center=(self.WIDTH / 4, int(i[0])))
                        screen.blit(leftarrow, leftarrow_rect)
                        rightarrow = pygame.image.load(f'data/rightarrowopaque.png')
                        rightarrow = pygame.transform.scale(rightarrow, (rightarrow.get_width() // 10,
                                                                         rightarrow.get_height() // 10))
                        rightarrow_rect = rightarrow.get_rect(center=(self.WIDTH / 4 * 3, int(i[0])))
                        screen.blit(rightarrow, rightarrow_rect)
                        rnd = font_infoboat.render(self.boat[i[1]], True, i[3])
                        screen.blit(rnd, rnd.get_rect(center=(self.WIDTH / 2, int(i[0]) + 80)))
                    i[5], i[6], i[7], i[8] = yacht.get_rect(center=(self.WIDTH / 2, int(i[0])))
                else:
                    font_infoboat = pygame.font.Font('fonts/8289.otf', 18)
                    yacht = pygame.image.load(f'data/{i[1]}')
                    yacht = pygame.transform.scale(yacht, (300, 100))
                    yacht_rect = yacht.get_rect(center=(self.WIDTH / 2, int(i[0])))
                    screen.blit(yacht, yacht_rect)
                    if self.max_boat == 1:
                        leftarrow = pygame.image.load(f'data/leftarrowtransparent.png')
                        leftarrow = pygame.transform.scale(leftarrow, (leftarrow.get_width() // 10,
                                                                       leftarrow.get_height() // 10))
                        leftarrow_rect = leftarrow.get_rect(center=(self.WIDTH / 4, int(i[0])))
                        screen.blit(leftarrow, leftarrow_rect)
                        rightarrow = pygame.image.load(f'data/rightarrowtransparent.png')
                        rightarrow = pygame.transform.scale(rightarrow, (rightarrow.get_width() // 10,
                                                                         rightarrow.get_height() // 10))
                        rightarrow_rect = rightarrow.get_rect(center=(self.WIDTH / 4 * 3, int(i[0])))
                        screen.blit(rightarrow, rightarrow_rect)
                        rnd = font_infoboat.render(self.boat[i[1]], True, i[3])
                        screen.blit(rnd, rnd.get_rect(center=(self.WIDTH / 2, int(i[0]) + 80)))
                    elif i[1] == 'yacht_1.png':
                        leftarrow = pygame.image.load(f'data/leftarrowtransparent.png')
                        leftarrow = pygame.transform.scale(leftarrow, (leftarrow.get_width() // 10,
                                                                       leftarrow.get_height() // 10))
                        leftarrow_rect = leftarrow.get_rect(center=(self.WIDTH / 4, int(i[0])))
                        screen.blit(leftarrow, leftarrow_rect)
                        rightarrow = pygame.image.load(f'data/rightarrowopaque.png')
                        rightarrow = pygame.transform.scale(rightarrow, (rightarrow.get_width() // 10,
                                                                         rightarrow.get_height() // 10))
                        rightarrow_rect = rightarrow.get_rect(center=(self.WIDTH / 4 * 3, int(i[0])))
                        screen.blit(rightarrow, rightarrow_rect)
                        rnd = font_infoboat.render(self.boat[i[1]], True, i[2])
                        screen.blit(rnd, rnd.get_rect(center=(self.WIDTH / 2, int(i[0]) + 80)))
                    elif i[1] == f'yacht_{self.max_boat}.png':
                        leftarrow = pygame.image.load(f'data/leftarrowopaque.png')
                        leftarrow = pygame.transform.scale(leftarrow, (leftarrow.get_width() // 10,
                                                                       leftarrow.get_height() // 10))
                        leftarrow_rect = leftarrow.get_rect(center=(self.WIDTH / 4, int(i[0])))
                        screen.blit(leftarrow, leftarrow_rect)
                        rightarrow = pygame.image.load(f'data/rightarrowtransparent.png')
                        rightarrow = pygame.transform.scale(rightarrow, (rightarrow.get_width() // 10,
                                                                         rightarrow.get_height() // 10))
                        rightarrow_rect = rightarrow.get_rect(center=(self.WIDTH / 4 * 3, int(i[0])))
                        screen.blit(rightarrow, rightarrow_rect)
                        rnd = font_infoboat.render(self.boat[i[1]], True, i[2])
                        screen.blit(rnd, rnd.get_rect(center=(self.WIDTH / 2, int(i[0]) + 80)))
                    else:
                        leftarrow = pygame.image.load(f'data/leftarrowopaque.png')
                        leftarrow = pygame.transform.scale(leftarrow, (leftarrow.get_width() // 10,
                                                                       leftarrow.get_height() // 10))
                        leftarrow_rect = leftarrow.get_rect(center=(self.WIDTH / 4, int(i[0])))
                        screen.blit(leftarrow, leftarrow_rect)
                        rightarrow = pygame.image.load(f'data/rightarrowopaque.png')
                        rightarrow = pygame.transform.scale(rightarrow, (rightarrow.get_width() // 10,
                                                                         rightarrow.get_height() // 10))
                        rightarrow_rect = rightarrow.get_rect(center=(self.WIDTH / 4 * 3, int(i[0])))
                        screen.blit(rightarrow, rightarrow_rect)
                        rnd = font_infoboat.render(self.boat[i[1]], True, i[2])
                        screen.blit(rnd, rnd.get_rect(center=(self.WIDTH / 2, int(i[0]) + 80)))
                    i[5], i[6], i[7], i[8] = yacht.get_rect(center=(self.WIDTH / 2, int(i[0])))

    def start(self):
        pygame.init()
        window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Startscreen')
        screen = pygame.Surface((self.WIDTH, self.HEIGHT))
        pygame.font.init()
        running = True
        pygame.mouse.set_visible(True)
        pygame.key.set_repeat(0, 0)
        font_menu = pygame.font.Font('fonts/8289.otf', 50)
        select = 0
        img = Config.Tracks.get_track(self.mn[0][1].split()[1]).get_image()
        fon = pygame.transform.scale(img,  (self.WIDTH, self.HEIGHT))
        while running:
            screen.blit(fon, (0, 0))
            screen.fill((45, 45, 45), special_flags=8)
            mp = pygame.mouse.get_pos()
            for i in self.mn:
                if int(i[5]) < mp[0] < int(i[5]) + int(i[7]) and int(i[6]) < mp[1] < int(i[6]) + int(i[8]):
                    select = i[4]
            mp = pygame.mouse.get_pos()
            if 661 < mp[0] < 661 + 29 and 55 < mp[1] < 55 + 51:
                if int(self.mn[0][1].split()[1]) != self.max_map:
                    select = 0
            if 221 < mp[0] < 221 + 29 and 55 < mp[1] < 55 + 51:
                if int(self.mn[0][1].split()[1]) != 1:
                    select = 0
            if 661 < mp[0] < 661 + 29 and 185 < mp[1] < 185 + 51:
                if int(self.mn[1][1].split('_')[1][:-4]) != self.max_boat:
                    select = 1
            if 211 < mp[0] < 211 + 29 and 185 < mp[1] < 185 + 51:
                if int(self.mn[1][1].split('_')[1][:-4]) != 1:
                    select = 1
            self.render(screen, font_menu, select)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        if select == 2:
                            running = False
                            self.res[0] = int(self.mn[0][1][6:])
                            self.res[1] = int(self.mn[1][1][6:-4])
                            break
                        if select == 3:
                            running = False
                            self.res[0] = 'records'
                            self.res[1] = 'records'
                            break
                        if select == 4:
                            sys.exit()
                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                    if e.key == pygame.K_UP:
                        if select > 0:
                            select -= 1
                    if e.key == pygame.K_DOWN:
                        if select < len(self.mn) - 1:
                            select += 1
                    if e.key == pygame.K_LEFT:
                        if select == 0:
                            for i in self.mn:
                                if select == i[4]:
                                    numtrack = i[1].split()[1]
                                    if int(numtrack) > 1:
                                        i[1] = f'{i[1].split()[0]} {int(numtrack) - 1}'
                                        fon = pygame.transform.scale(
                                            load_image(f'{self.mn[0][1].split()[0]}_{self.mn[0][1].split()[1]}.jpg'),
                                            (self.WIDTH, self.HEIGHT))
                        if select == 1:
                            for i in self.mn:
                                if select == i[4]:
                                    numyacht = i[1].split("_")[1][:-4]
                                    if int(numyacht) > 1:
                                        i[1] = f'{i[1].split("_")[0]}_{int(numyacht) - 1}.png'
                    if e.key == pygame.K_RIGHT:
                        if select == 0:
                            for i in self.mn:
                                if select == i[4]:
                                    numtrack = i[1].split()[1]
                                    if int(numtrack) < self.max_map:
                                        i[1] = f'{i[1].split()[0]} {int(numtrack) + 1}'
                                        fon = pygame.transform.scale(
                                            load_image(f'{self.mn[0][1].split()[0]}_{self.mn[0][1].split()[1]}.jpg'),
                                            (self.WIDTH, self.HEIGHT))
                        if select == 1:
                            for i in self.mn:
                                if select == i[4]:
                                    numyacht = i[1].split("_")[1][:-4]
                                    if int(numyacht) < self.max_boat:
                                        i[1] = f'{i[1].split("_")[0]}_{int(numyacht) + 1}.png'
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    mp = pygame.mouse.get_pos()
                    for i in self.mn:
                        if int(i[5]) < mp[0] < int(i[5]) + int(i[7]) and int(i[6]) < mp[1] < int(i[6]) + int(i[8]):
                            if select == 2:
                                running = False
                                self.res[0] = int(self.mn[0][1][6:])
                                self.res[1] = int(self.mn[1][1][6:-4])
                            if select == 3:
                                running = False
                                self.res[0] = 'records'
                                self.res[1] = 'records'
                            if select == 4:
                                sys.exit()
                    mp = pygame.mouse.get_pos()
                    if 661 < mp[0] < 661 + 29 and 55 < mp[1] < 55 + 51:
                        numtrack = self.mn[0][1].split()[1]
                        if int(numtrack) < self.max_map:
                            self.mn[0][1] = f'{self.mn[0][1].split()[0]} {int(numtrack) + 1}'
                            fon = pygame.transform.scale(
                                load_image(f'{self.mn[0][1].split()[0]}_{self.mn[0][1].split()[1]}.jpg'),
                                (self.WIDTH, self.HEIGHT))
                    if 221 < mp[0] < 221 + 29 and 55 < mp[1] < 55 + 51:
                        numtrack = self.mn[0][1].split()[1]
                        if int(numtrack) > 1:
                            self.mn[0][1] = f'{self.mn[0][1].split()[0]} {int(numtrack) - 1}'
                            fon = pygame.transform.scale(
                                load_image(f'{self.mn[0][1].split()[0]}_{self.mn[0][1].split()[1]}.jpg'),
                                (self.WIDTH, self.HEIGHT))
                    if 661 < mp[0] < 661 + 29 and 185 < mp[1] < 185 + 51:
                        numyacht = self.mn[1][1].split("_")[1][:-4]
                        if int(numyacht) < self.max_boat:
                            self.mn[1][1] = f'{self.mn[1][1].split("_")[0]}_{int(numyacht) + 1}.png'
                    if 211 < mp[0] < 211 + 29 and 185 < mp[1] < 185 + 51:
                        numyacht = self.mn[1][1].split("_")[1][:-4]
                        if int(numyacht) > 1:
                            self.mn[1][1] = f'{self.mn[1][1].split("_")[0]}_{int(numyacht) - 1}.png'
            window.blit(screen, (0, 0))
            pygame.display.update()
        pygame.quit()
        return self.res
