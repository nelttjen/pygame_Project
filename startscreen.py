import pygame
import sys
import os

FPS = 60
WIDTH = 900
HEIGHT = 720
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Startscreen')
screen = pygame.Surface((WIDTH, HEIGHT))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print('Файл не найден')
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


class Startscreen:
    def __init__(self, mn_p=[410, 'Новая игра', (250, 250, 30), (250, 30, 250), 2, 0, 0, 0, 0]):
        self.mn_p = mn_p
        self.boat = {'yacht_1.png': 'Масса: 1    Мощность двигателя: 2    Обтекаемость: 3    Устойчивость: 4',
                     'yacht_2.png': 'Масса: 4    Мощность двигателя: 3    Обтекаемость: 2    Устойчивость: 1'}

    def render(self, screen, font, num_select):
        for i in self.mn_p:
            if i[1][-4::] != '.png':
                if i[1][:5] != 'Track':
                    if num_select == i[4]:
                        rnd = font.render(i[1], 1, i[3])
                        screen.blit(rnd, rnd.get_rect(center=(WIDTH / 2, int(i[0]))))
                        i[5], i[6], i[7], i[8] = rnd.get_rect(center=(WIDTH / 2, int(i[0])))
                    else:
                        rnd = font.render(i[1], 1, i[2])
                        screen.blit(rnd, rnd.get_rect(center=(WIDTH / 2, int(i[0]))))
                        i[5], i[6], i[7], i[8] = rnd.get_rect(center=(WIDTH / 2, int(i[0])))
                else:
                    if num_select == i[4]:
                        rnd = font.render(i[1], 1, i[3])
                        screen.blit(rnd, rnd.get_rect(center=(WIDTH / 2, int(i[0]))))
                        i[5], i[6], i[7], i[8] = rnd.get_rect(center=(WIDTH / 2, int(i[0])))
                        if i[1][-1] == '1':
                            leftarrowpaque = pygame.image.load(f'data/leftarrowtransparent.png')
                            leftarrowpaque = pygame.transform.scale(leftarrowpaque, (leftarrowpaque.get_width() // 10,
                                                                                     leftarrowpaque.get_height() // 10))
                            leftarrowpaque_rect = leftarrowpaque.get_rect(center=(WIDTH / 4, int(i[0])))
                            screen.blit(leftarrowpaque, leftarrowpaque_rect)
                            rightarrowpaque = pygame.image.load(f'data/rightarrowopaque.png')
                            rightarrowpaque = pygame.transform.scale(rightarrowpaque,
                                                                     (rightarrowpaque.get_width() // 10,
                                                                      rightarrowpaque.get_height() // 10))
                            rightarrowpaque_rect = rightarrowpaque.get_rect(center=(WIDTH / 4 * 3, int(i[0])))
                            screen.blit(rightarrowpaque, rightarrowpaque_rect)
                        elif i[1][-1] == '3':
                            leftarrowpaque = pygame.image.load(f'data/leftarrowopaque.png')
                            leftarrowpaque = pygame.transform.scale(leftarrowpaque, (leftarrowpaque.get_width() // 10,
                                                                                     leftarrowpaque.get_height() // 10))
                            leftarrowpaque_rect = leftarrowpaque.get_rect(center=(WIDTH / 4, int(i[0])))
                            screen.blit(leftarrowpaque, leftarrowpaque_rect)
                            rightarrowpaque = pygame.image.load(f'data/rightarrowtransparent.png')
                            rightarrowpaque = pygame.transform.scale(rightarrowpaque,
                                                                     (rightarrowpaque.get_width() // 10,
                                                                      rightarrowpaque.get_height() // 10))
                            rightarrowpaque_rect = rightarrowpaque.get_rect(center=(WIDTH / 4 * 3, int(i[0])))
                            screen.blit(rightarrowpaque, rightarrowpaque_rect)
                        else:
                            leftarrowpaque = pygame.image.load(f'data/leftarrowopaque.png')
                            leftarrowpaque = pygame.transform.scale(leftarrowpaque, (leftarrowpaque.get_width() // 10,
                                                                                     leftarrowpaque.get_height() // 10))
                            leftarrowpaque_rect = leftarrowpaque.get_rect(center=(WIDTH / 4, int(i[0])))
                            screen.blit(leftarrowpaque, leftarrowpaque_rect)
                            rightarrowpaque = pygame.image.load(f'data/rightarrowopaque.png')
                            rightarrowpaque = pygame.transform.scale(rightarrowpaque,
                                                                     (rightarrowpaque.get_width() // 10,
                                                                      rightarrowpaque.get_height() // 10))
                            rightarrowpaque_rect = rightarrowpaque.get_rect(center=(WIDTH / 4 * 3, int(i[0])))
                            screen.blit(rightarrowpaque, rightarrowpaque_rect)
                    else:
                        rnd = font.render(i[1], 1, i[2])
                        screen.blit(rnd, rnd.get_rect(center=(WIDTH / 2, int(i[0]))))
                        i[5], i[6], i[7], i[8] = rnd.get_rect(center=(WIDTH / 2, int(i[0])))
                        if i[1][-1] == '1':
                            leftarrowpaque = pygame.image.load(f'data/leftarrowtransparent.png')
                            leftarrowpaque = pygame.transform.scale(leftarrowpaque, (leftarrowpaque.get_width() // 10,
                                                                                     leftarrowpaque.get_height() // 10))
                            leftarrowpaque_rect = leftarrowpaque.get_rect(center=(WIDTH / 4, int(i[0])))
                            screen.blit(leftarrowpaque, leftarrowpaque_rect)
                            rightarrowpaque = pygame.image.load(f'data/rightarrowopaque.png')
                            rightarrowpaque = pygame.transform.scale(rightarrowpaque,
                                                                     (rightarrowpaque.get_width() // 10,
                                                                      rightarrowpaque.get_height() // 10))
                            rightarrowpaque_rect = rightarrowpaque.get_rect(center=(WIDTH / 4 * 3, int(i[0])))
                            screen.blit(rightarrowpaque, rightarrowpaque_rect)
                        elif i[1][-1] == '3':
                            leftarrowpaque = pygame.image.load(f'data/leftarrowopaque.png')
                            leftarrowpaque = pygame.transform.scale(leftarrowpaque, (leftarrowpaque.get_width() // 10,
                                                                                     leftarrowpaque.get_height() // 10))
                            leftarrowpaque_rect = leftarrowpaque.get_rect(center=(WIDTH / 4, int(i[0])))
                            screen.blit(leftarrowpaque, leftarrowpaque_rect)
                            rightarrowpaque = pygame.image.load(f'data/rightarrowtransparent.png')
                            rightarrowpaque = pygame.transform.scale(rightarrowpaque,
                                                                     (rightarrowpaque.get_width() // 10,
                                                                      rightarrowpaque.get_height() // 10))
                            rightarrowpaque_rect = rightarrowpaque.get_rect(center=(WIDTH / 4 * 3, int(i[0])))
                            screen.blit(rightarrowpaque, rightarrowpaque_rect)
                        else:
                            leftarrowpaque = pygame.image.load(f'data/leftarrowopaque.png')
                            leftarrowpaque = pygame.transform.scale(leftarrowpaque, (leftarrowpaque.get_width() // 10,
                                                                                     leftarrowpaque.get_height() // 10))
                            leftarrowpaque_rect = leftarrowpaque.get_rect(center=(WIDTH / 4, int(i[0])))
                            screen.blit(leftarrowpaque, leftarrowpaque_rect)
                            rightarrowpaque = pygame.image.load(f'data/rightarrowopaque.png')
                            rightarrowpaque = pygame.transform.scale(rightarrowpaque,
                                                                     (rightarrowpaque.get_width() // 10,
                                                                      rightarrowpaque.get_height() // 10))
                            rightarrowpaque_rect = rightarrowpaque.get_rect(center=(WIDTH / 4 * 3, int(i[0])))
                            screen.blit(rightarrowpaque, rightarrowpaque_rect)
            else:
                if num_select == i[4]:
                    font_infoboat = pygame.font.Font('fonts/8289.otf', 18)
                    yacht = pygame.image.load(f'data/{i[1]}')
                    yacht = pygame.transform.scale(yacht, (yacht.get_width() * 3, yacht.get_height() * 3))
                    yacht_rect = yacht.get_rect(center=(WIDTH / 2, int(i[0])))
                    screen.blit(yacht, yacht_rect)
                    if i[1] == 'yacht_1.png':
                        leftarrowpaque = pygame.image.load(f'data/leftarrowtransparent.png')
                        leftarrowpaque = pygame.transform.scale(leftarrowpaque, (leftarrowpaque.get_width() // 10,
                                                                                 leftarrowpaque.get_height() // 10))
                        leftarrowpaque_rect = leftarrowpaque.get_rect(center=(WIDTH / 4, int(i[0])))
                        screen.blit(leftarrowpaque, leftarrowpaque_rect)
                        rightarrowpaque = pygame.image.load(f'data/rightarrowopaque.png')
                        rightarrowpaque = pygame.transform.scale(rightarrowpaque, (rightarrowpaque.get_width() // 10,
                                                                                   rightarrowpaque.get_height() // 10))
                        rightarrowpaque_rect = rightarrowpaque.get_rect(center=(WIDTH / 4 * 3, int(i[0])))
                        screen.blit(rightarrowpaque, rightarrowpaque_rect)
                        rnd = font_infoboat.render(self.boat[i[1]], 1, i[3])
                        screen.blit(rnd, rnd.get_rect(center=(WIDTH / 2, int(i[0]) + 80)))
                    elif i[1] == 'yacht_2.png':
                        leftarrowpaque = pygame.image.load(f'data/leftarrowopaque.png')
                        leftarrowpaque = pygame.transform.scale(leftarrowpaque, (leftarrowpaque.get_width() // 10,
                                                                                 leftarrowpaque.get_height() // 10))
                        leftarrowpaque_rect = leftarrowpaque.get_rect(center=(WIDTH / 4, int(i[0])))
                        screen.blit(leftarrowpaque, leftarrowpaque_rect)
                        rightarrowpaque = pygame.image.load(f'data/rightarrowtransparent.png')
                        rightarrowpaque = pygame.transform.scale(rightarrowpaque, (rightarrowpaque.get_width() // 10,
                                                                                   rightarrowpaque.get_height() // 10))
                        rightarrowpaque_rect = rightarrowpaque.get_rect(center=(WIDTH / 4 * 3, int(i[0])))
                        screen.blit(rightarrowpaque, rightarrowpaque_rect)
                        rnd = font_infoboat.render(self.boat[i[1]], 1, i[3])
                        screen.blit(rnd, rnd.get_rect(center=(WIDTH / 2, int(i[0]) + 80)))
                    i[5], i[6], i[7], i[8] = yacht.get_rect(center=(WIDTH / 2, int(i[0])))
                else:
                    font_infoboat = pygame.font.Font('fonts/8289.otf', 18)
                    yacht = pygame.image.load(f'data/{i[1]}')
                    yacht = pygame.transform.scale(yacht, (yacht.get_width() * 3, yacht.get_height() * 3))
                    yacht_rect = yacht.get_rect(center=(WIDTH / 2, int(i[0])))
                    screen.blit(yacht, yacht_rect)
                    if i[1] == 'yacht_1.png':
                        leftarrowpaque = pygame.image.load(f'data/leftarrowtransparent.png')
                        leftarrowpaque = pygame.transform.scale(leftarrowpaque, (leftarrowpaque.get_width() // 10,
                                                                                 leftarrowpaque.get_height() // 10))
                        leftarrowpaque_rect = leftarrowpaque.get_rect(center=(WIDTH / 4, int(i[0])))
                        screen.blit(leftarrowpaque, leftarrowpaque_rect)
                        rightarrowpaque = pygame.image.load(f'data/rightarrowopaque.png')
                        rightarrowpaque = pygame.transform.scale(rightarrowpaque, (rightarrowpaque.get_width() // 10,
                                                                                   rightarrowpaque.get_height() // 10))
                        rightarrowpaque_rect = rightarrowpaque.get_rect(center=(WIDTH / 4 * 3, int(i[0])))
                        screen.blit(rightarrowpaque, rightarrowpaque_rect)
                        rnd = font_infoboat.render(self.boat[i[1]], 1, i[2])
                        screen.blit(rnd, rnd.get_rect(center=(WIDTH / 2, int(i[0]) + 80)))
                    elif i[1] == 'yacht_2.png':
                        leftarrowpaque = pygame.image.load(f'data/leftarrowopaque.png')
                        leftarrowpaque = pygame.transform.scale(leftarrowpaque, (leftarrowpaque.get_width() // 10,
                                                                                 leftarrowpaque.get_height() // 10))
                        leftarrowpaque_rect = leftarrowpaque.get_rect(center=(WIDTH / 4, int(i[0])))
                        screen.blit(leftarrowpaque, leftarrowpaque_rect)
                        rightarrowpaque = pygame.image.load(f'data/rightarrowtransparent.png')
                        rightarrowpaque = pygame.transform.scale(rightarrowpaque, (rightarrowpaque.get_width() // 10,
                                                                                   rightarrowpaque.get_height() // 10))
                        rightarrowpaque_rect = rightarrowpaque.get_rect(center=(WIDTH / 4 * 3, int(i[0])))
                        screen.blit(rightarrowpaque, rightarrowpaque_rect)
                        rnd = font_infoboat.render(self.boat[i[1]], 1, i[2])
                        screen.blit(rnd, rnd.get_rect(center=(WIDTH / 2, int(i[0]) + 80)))
                    i[5], i[6], i[7], i[8] = yacht.get_rect(center=(WIDTH / 2, int(i[0])))

    def start(self):
        pygame.font.init()
        running = True
        pygame.mouse.set_visible(True)
        pygame.key.set_repeat(0, 0)
        font_menu = pygame.font.Font('fonts/8289.otf', 50)
        select = 0
        max_map = 3
        max_boat = 2
        while running:
            # fon = pygame.transform.scale(load_image(self.mn_p[0][1]),
            #                              (WIDTH, HEIGHT))
            # screen.blit(fon, (0, 0))
            screen.fill((0, 100, 200))

            mp = pygame.mouse.get_pos()
            for i in self.mn_p:
                if int(i[5]) < mp[0] < int(i[5]) + int(i[7]) and int(i[6]) < mp[1] < int(i[6]) + int(i[8]):
                    select = i[4]
            mp = pygame.mouse.get_pos()
            if 661 < mp[0] < 661 + 29 and 55 < mp[1] < 55 + 51:
                if int(self.mn_p[0][1].split()[1]) != max_map:
                    print(max_map, self.mn_p[0][1].split()[1])
                    select = 0
            if 221 < mp[0] < 221 + 29 and 55 < mp[1] < 55 + 51:
                if int(self.mn_p[0][1].split()[1]) != 1:
                    print(1, self.mn_p[0][1].split()[1])
                    select = 0
            if 661 < mp[0] < 661 + 29 and 185 < mp[1] < 185 + 51:
                if int(self.mn_p[1][1].split('_')[1][:-4]) != max_boat:
                    print(max_boat, self.mn_p[1][1].split('_')[1][:-4])
                    select = 1
            if 211 < mp[0] < 211 + 29 and 185 < mp[1] < 185 + 51:
                if int(self.mn_p[1][1].split('_')[1][:-4]) != 1:
                    print(1, self.mn_p[1][1].split('_')[1][:-4])
                    select = 1
            self.render(screen, font_menu, select)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        if select == 2:
                            running = False
                        if select == 4:
                            sys.exit()
                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                    if e.key == pygame.K_UP:
                        if select > 0:
                            select -= 1
                    if e.key == pygame.K_DOWN:
                        if select < len(self.mn_p) - 1:
                            select += 1
                    if e.key == pygame.K_LEFT:
                        if select == 0:
                            for i in self.mn_p:
                                if select == i[4]:
                                    numtrack = i[1].split()[1]
                                    if int(numtrack) > 1:
                                        i[1] = f'{i[1].split()[0]} {int(numtrack) - 1}'
                        if select == 1:
                            for i in self.mn_p:
                                if select == i[4]:
                                    numyacht = i[1].split("_")[1][:-4]
                                    if int(numyacht) > 1:
                                        i[1] = f'{i[1].split("_")[0]}_{int(numyacht) - 1}.png'
                    if e.key == pygame.K_RIGHT:
                        if select == 0:
                            for i in self.mn_p:
                                if select == i[4]:
                                    numtrack = i[1].split()[1]
                                    if int(numtrack) < max_map:
                                        i[1] = f'{i[1].split()[0]} {int(numtrack) + 1}'
                        if select == 1:
                            for i in self.mn_p:
                                if select == i[4]:
                                    numyacht = i[1].split("_")[1][:-4]
                                    if int(numyacht) < max_boat:
                                        i[1] = f'{i[1].split("_")[0]}_{int(numyacht) + 1}.png'
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    mp = pygame.mouse.get_pos()
                    for i in self.mn_p:
                        if int(i[5]) < mp[0] < int(i[5]) + int(i[7]) and int(i[6]) < mp[1] < int(i[6]) + int(i[8]):
                            if select == 2:
                                running = False
                            if select == 4:
                                sys.exit()
                    mp = pygame.mouse.get_pos()
                    if 661 < mp[0] < 661 + 29 and 55 < mp[1] < 55 + 51:
                        numtrack = self.mn_p[0][1].split()[1]
                        if int(numtrack) < max_map:
                            self.mn_p[0][1] = f'{self.mn_p[0][1].split()[0]} {int(numtrack) + 1}'
                    if 221 < mp[0] < 221 + 29 and 55 < mp[1] < 55 + 51:
                        numtrack = self.mn_p[0][1].split()[1]
                        if int(numtrack) > 1:
                            self.mn_p[0][1] = f'{self.mn_p[0][1].split()[0]} {int(numtrack) - 1}'
                    if 661 < mp[0] < 661 + 29 and 185 < mp[1] < 185 + 51:
                        numyacht = self.mn_p[1][1].split("_")[1][:-4]
                        if int(numyacht) < max_boat:
                            self.mn_p[1][1] = f'{self.mn_p[1][1].split("_")[0]}_{int(numyacht) + 1}.png'
                    if 211 < mp[0] < 211 + 29 and 185 < mp[1] < 185 + 51:
                        numyacht = self.mn_p[1][1].split("_")[1][:-4]
                        if int(numyacht) > 1:
                            self.mn_p[1][1] = f'{self.mn_p[1][1].split("_")[0]}_{int(numyacht) - 1}.png'
            window.blit(screen, (0, 0))
            pygame.display.update()


mn_p = [[80, 'Track 1', (250, 250, 30), (250, 30, 250), 0, 0, 0, 0, 0],
        [210, 'yacht_1.png', (250, 250, 30), (250, 30, 250), 1, 0, 0, 0, 0],
        [410, 'Новая игра', (250, 250, 30), (250, 30, 250), 2, 0, 0, 0, 0],
        [510, 'Таблица рекордов', (250, 250, 30), (250, 30, 250), 3, 0, 0, 0, 0],
        [610, 'Выход', (250, 250, 30), (250, 30, 250), 4, 0, 0, 0, 0]]
game = Startscreen(mn_p)
game.start()
print(mn_p)
