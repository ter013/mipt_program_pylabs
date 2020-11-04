from random import randrange as rnd, choice
import pygame
from pygame.draw import *

pygame.init()
import math
import threading
import time
import numpy as np



length = 800  # длина экрана
height = 600  # высота экрана

ORANGERED = (255, 69, 0) #цвет для взрыва
GREY = (128, 128, 128) #цвет для взрыва
BOMB_COLOR = (34, 139, 34) #цвет снарядов

GREEN1 = (0, 128, 0)
GREEN2 = (50, 205, 50)
GREEN3 = (34, 139, 34)

ORANGE = (255, 140, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARKRAD = (139, 0, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN] #цвета для шариков из пушки
COLORS_TARGET = [RED, YELLOW] #цвета целей
FPS = 30
screen = pygame.display.set_mode((length, height))

font = pygame.font.Font('freesansbold.ttf', 14)
number_of_targets = int(input("Введите число целей"))




g = 2  # ускорение свободного падения

class ball():
    def __init__(self):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = 0
        self.y = 0
        self.r = 10
        self.Vx = 0
        self.Vy = 0
        self.color = choice(COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        X = length
        Y = height
        self.x += self.Vx

        if self.x >= X:
            self.Vx = -self.Vx
        else:
            self.Vx = self.Vx
        if self.x <= 0:
            self.Vx = -self.Vx
        else:
            self.Vx = self.Vx

        self.Vy += g
        self.y += self.Vy

        if self.y >= Y - 100:
            self.Vy = -self.Vy / 1.1
            self.Vx = self.Vx / 1.1
        else:
            self.Vy = self.Vy
        if self.y <= 0:
            self.Vy = -self.Vy
        else:
            self.Vy = self.Vy

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.r))

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (obj.x - self.x) ** 2 + (obj.y - self.y) ** 2 <= (obj.r + self.r) ** 2:
            return True
        else:
            return False


class gun():
    """
    Класс пушки, прицеливается, выстреливает шариком,
    может двигаться
    """
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.x = rnd(50, 600)
        self.y = rnd(420, 500)
        self.x1 = self.x + 30
        self.y1 = self.y
        self.color1 = BLACK #цвет в незаряженном состоянии
        self.color2 = ORANGE #цвет в заряденном состоянии
        pygame.draw.line(screen, self.color1, [self.x, self.y], [self.x1, self.y1], 7)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event, obj):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        #global balls, bullet
        obj.bullet += 1
        new_ball = ball()
        new_ball.x = self.x
        new_ball.y = self.y
        new_ball.r += 5

        if event.pos[0] != self.x:
            self.an = math.atan((event.pos[1] - new_ball.y) / (event.pos[0] - new_ball.x))
            if event.pos[0] > self.x:
                new_ball.Vx = self.f2_power * math.cos(self.an)
                new_ball.Vy = self.f2_power * math.sin(self.an)
            if event.pos[0] < self.x:
                new_ball.Vx = self.f2_power * math.cos(self.an + math.pi)
                new_ball.Vy = self.f2_power * math.sin(self.an + math.pi)
        else:
            if event.pos[1] - self.x > 0:
                new_ball.Vy = self.f2_power
            else:
                new_ball.Vy = -self.f2_power
        obj.balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event.pos[0] != self.x:
            self.an = math.atan((event.pos[1] - self.y) / (event.pos[0] - self.x))
            if event.pos[0] > self.x:
                self.x1 = self.x + max(self.f2_power, 20) * math.cos(self.an)
                self.y1 = self.y + max(self.f2_power, 20) * math.sin(self.an)
            if  event.pos[0] < self.x:
                self.x1 = self.x + max(self.f2_power, 20) * math.cos(self.an + math.pi)
                self.y1 = self.y + max(self.f2_power, 20) * math.sin(self.an + math.pi)
        else:
            self.x1 = self.x
            if event.pos[1] > self.y:
                self.y1 = self.y + max(self.f2_power, 20)
            else:
                self.y1 = self.y - max(self.f2_power, 20)
        if self.f2_on:
            pygame.draw.line(screen, self.color2, [self.x, self.y], [self.x1, self.y1], 7)
        else:
            pygame.draw.line(screen, self.color1, [self.x, self.y], [self.x1, self.y1], 7)
    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            pygame.draw.line(screen, self.color2, [self.x, self.y], [self.x1, self.y1], 7)
        else:
            pygame.draw.line(screen, self.color1, [self.x, self.y], [self.x1, self.y1], 7)
    def move(self):
        #движенние с учётом обработки нажатий
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= 3
            self.x1 -= 3
        elif keys[pygame.K_d]:
            self.x += 3
            self.x1 += 3
        if keys[pygame.K_w]:
            self.y -= 3
            self.y1 -= 3
        if keys[pygame.K_s]:
            self.y += 3
            self.y1 += 3

class BTR(gun):
    """
    Является подклассом пушки
    Представляет собой Бронетранспортёр
    """
    def __init__(self):
        super().__init__()
        self.color1 = GREEN1#цвет для пушки и корпуса
        self.color2 = GREEN2#цвет для заряженной пушки
        self.color3 = GREEN3#цвет для башни
        self.health = 100#количество жизней пушки
    def draw(self):
        r = 20 #радиус башни
        R1 = 12 #радиус колёс
        R2 = 4 #радиус диска колёс
        #рисуем башню
        circle(screen, self.color3, (self.x, self.y + r-5) , r)

        #рисуем корпус
        polygon(screen, self.color1,[(self.x - 60, self.y + r - 5), (self.x + 50, self.y + r - 5),
                                     (self.x + 50, self.y + r  + 6), (self.x + 28, self.y + r + 25),
                                     (self.x - 60, self.y + r + 25), (self.x - 60, self.y + r - 5)] )
        #рисуем колёса
        circle(screen, BLACK, (self.x - 40, self.y + r + 25), R1)
        circle(screen, WHITE, (self.x -40, self.y + r + 25), R2)

        circle(screen, BLACK, (self.x - 15, self.y + r + 25), R1)
        circle(screen, WHITE, (self.x - 15, self.y + r + 25), R2)

        circle(screen, BLACK, (self.x + 10, self.y + r + 25), R1)
        circle(screen, WHITE, (self.x + 10, self.y + r + 25), R2)

    def healthbar(self):
        #рисует отрезок жизней машины
        if 80 < self.health <= 100:
            rect(screen, GREEN1, (self.x - 50, self.y - 20, self.health, 5))
            rect(screen, WHITE, (self.x - 50 + self.health, self.y - 20, 100 - self.health, 5))
            rect(screen, BLACK, (self.x - 50, self.y - 20, 100 , 5), 1)

        if 60 < self.health <= 80:
            rect(screen, GREEN2, (self.x - 50, self.y - 20, self.health, 5))
            rect(screen, WHITE, (self.x - 50 + self.health, self.y - 20, 100 - self.health, 5))
            rect(screen, BLACK, (self.x - 50, self.y - 20, 100, 5), 1)
        if 40 < self.health <= 60:
            rect(screen, YELLOW, (self.x - 50, self.y - 20, self.health, 5))
            rect(screen, WHITE, (self.x - 50 + self.health, self.y - 20, 100 - self.health, 5))
            rect(screen, BLACK, (self.x - 50, self.y - 20, 100, 5), 1)
        if 20 < self.health <= 40:
            rect(screen, ORANGERED, (self.x - 50, self.y - 20, self.health, 5))
            rect(screen, WHITE, (self.x - 50 + self.health, self.y - 20, 100 - self.health, 5))
            rect(screen, BLACK, (self.x - 50, self.y - 20, 100, 5), 1)
        if 0 < self.health <= 20:
            rect(screen, DARKRAD , (self.x - 50, self.y - 20, self.health, 5))
            rect(screen, WHITE, (self.x - 50 + self.health, self.y - 20, 100 - self.health, 5))
            rect(screen, BLACK, (self.x - 50, self.y - 20, 100, 5), 1)



class target():
    def __init__(self):
        self.points = 0
        self.live = 1
        self.Vx = rnd(1, 5)
        self.Vy = rnd(1, 5)

        self.new_target()
    def new_target(self):
        """ Инициализация новой цели. """
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(10, 30)
        self.color = choice(COLORS_TARGET)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.Vx = 0
        self.Vy = 0
        self.x = -100
        self.y = -100

        self.points += points
    def create_bomb(self,obj):
        new_bomb = Bomb()
        new_bomb.x = self.x
        new_bomb.y = self.y
        obj.boombs.append(new_bomb)



    def move(self):
        """Переместить цель по прошествии единицы времени.

        Метод описывает перемещение цели за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy
        и стен по краям окна (размер окна 800х600).
        """
        X = length
        Y = height
        self.x += self.Vx

        if self.x >= X:
            self.Vx = -self.Vx
        else:
            self.Vx = self.Vx
        if self.x <= 0:
            self.Vx = -self.Vx
        else:
            self.Vx = self.Vx

        self.y += self.Vy

        if self.y >= Y - 100:
            self.Vy = -self.Vy
        else:
            self.Vy = self.Vy
        if self.y <= 0:
            self.Vy = -self.Vy
        else:
            self.Vy = self.Vy




class My_circle(target):
    # подкласс целей
    def __init__(self):
        super().__init__()

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)


class My_star(target):
    #подкласс целей
    def __init__(self):
        super().__init__()
        self.alpha = 0

    def draw(self):
        polygon(screen, self.color, [(self.x + self.r * np.sin(self.alpha / 180 * np.pi),
                                      self.y - self.r * np.cos(self.alpha / 180 * np.pi)),
                                     (self.x + self.r * np.sin((36 - self.alpha) / 180 * np.pi),
                                      self.y + self.r * np.cos((36 - self.alpha) / 180 * np.pi)),
                                     (self.x - self.r / (
                                                 4 * np.cos(18 / 180 * np.pi) * np.cos(18 / 180 * np.pi) - 1) * np.sin(
                                         self.alpha / 180 * np.pi),
                                      self.y + self.r / (
                                                  4 * np.cos(18 / 180 * np.pi) * np.cos(18 / 180 * np.pi) - 1) * np.cos(
                                          self.alpha / 180 * np.pi)),
                                     (self.x - self.r * np.sin((36 + self.alpha) / 180 * np.pi),
                                      self.y + self.r * np.cos((36 + self.alpha) / 180 * np.pi)),
                                     (self.x + self.r * np.sin(self.alpha / 180 * np.pi),
                                      self.y - self.r * np.cos(self.alpha / 180 * np.pi))])

        polygon(screen, self.color, [(self.x - self.r * np.sin((72 - self.alpha) / 180 * np.pi),
                                      self.y - self.r * np.cos((72 - self.alpha) / 180 * np.pi)),
                                     (self.x + self.r * np.sin((72 + self.alpha) / 180 * np.pi),
                                      self.y - self.r * np.cos((72 + self.alpha) / 180 * np.pi)),
                                     (self.x - self.r * np.sin((36 + self.alpha) / 180 * np.pi),
                                      self.y + self.r * np.cos((36 + self.alpha) / 180 * np.pi)),
                                     (self.x - self.r / (
                                                 4 * np.cos(18 / 180 * np.pi) * np.cos(18 / 180 * np.pi) - 1) * np.sin(
                                         (72 + self.alpha) / 180 * np.pi),
                                      self.y + self.r / (
                                                  4 * np.cos(18 / 180 * np.pi) * np.cos(18 / 180 * np.pi) - 1) * np.cos(
                                          (72 + self.alpha) / 180 * np.pi)),
                                     (self.x - self.r * np.sin((72 - self.alpha) / 180 * np.pi),
                                      self.y - self.r * np.cos((72 - self.alpha) / 180 * np.pi))])

        self.alpha += 20  # создаю вращение звезды

class Bomb():
    #класс снарядов
    def __init__(self):
        self.damage = rnd(5,15)
        self.x = 0
        self.y = 0
        self.Vy = rnd(1,5)
        self.color = BOMB_COLOR

    def draw(self):
        #основание снаряда
        polygon(screen, self.color, [(self.x - 10, self.y), (self.x + 10,self.y),
                         (self.x + 10, self.y + 10), (self.x - 10, self.y + 10)])
        #сердцевина снаряда
        polygon(screen, self.color, [(self.x - 5, self.y + 10), (self.x + 5, self.y + 10),
                         (self.x + 10, self.y + 25), (self.x + 10, self.y + 45),
                         (self.x - 10, self.y + 45), (self.x - 10, self.y + 25),
                         (self.x-5, self.y +10)])
        #вершина бомбы
        circle(screen, self.color, (self.x, self.y + 45), 10)
    def move(self):
        # перемещение с учетом гравитации
        self.y += self.Vy
        self.Vy += g

    def hit(self):
        # удаление бомбы
        self.x = -100
        self.y = -100
        self.Vx = 0
        self.Vy = 0
    def hittest(self,obj):
        """
        Функция проверяет сталкивалкивается ли бомба с obj или с землей.

        Args:
            obj: Обьект, с которым проверяется столкновение.
         Returns:
        Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if abs(obj.x-self.x) < 30 and abs(obj.y - self.y) < 30:
            return True
        else:
            return False

    def bang(self):
        """
        Функция рисует взрыв
        """
        #листы для координат шариков взрыва
        listx1 = [10, 30, 35, 32, 18, 8, -10, -10]
        listy1 = [27, 18, 2, -6, -18, -17, 0, 15]

        listx2 = [7, 17, 18, 6, -3, -3]
        listy2 = [17, 11, -1, -6, 2, 10]

        listx3 = [6, 10, 11, 5, 0, 0]
        listy3 = [10, 7, 2, -1, 3, 7]

        for i in range(0, 8, 1):
            circle(screen, GREY, (self.x + listx1[i], self.y + listy1[i]), 15)
        for i in range(0, 6, 1):
            circle(screen, ORANGERED, (self.x + listx2[i], self.y + listy2[i]), 12)
        for i in range(0, 6, 1):
            circle(screen, YELLOW, (self.x + listx3[i], self.y + listy3[i]), 10)

class manager():
    """
    Этот класс совершает различные операции с другими классами.
    """
    def __init__(self):
        self.finished = False
        self.bullet = 0
        self.score = 0
        self.j = 0 # параметр, отвечащий за выбор машины
        self.a = 0 # вывод текста на экран
        self.h = 0 # счётчик для бомбордировки
        self.time = 0 # для вывода текста
        #листы с объектами
        self.machine = []
        self.targets = []
        self.balls = []
        self.boombs = []
    def append(self):
        #заполняем листы с объектами
        for i in range(int(number_of_targets / 3)):
            self.targets.append(My_circle())
        for i in range(number_of_targets - int(number_of_targets / 3)):
            self.targets.append(My_star())
        for i in range(0,4,1):
            self.machine.append(BTR())
    def process(self):
        #проверяет события клавиатуры и мышм
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.finished = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.j < len(self.machine) - 1:
                        self.j += 1
                    else:
                        self.j = 0
            for i in range(len(self.machine)):
                if i == self.j:
                    if event.type == pygame.MOUSEMOTION:
                        self.machine[i].targetting(event)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.machine[i].fire2_start(event)
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.machine[i].fire2_end(event, self)


    def delete(self):
        #удаляет сломанные машины
        for i in range(len(self.machine) - 1):
            if self.machine[i].health <= 0:
                del self.machine[i]
    def tick(self):
        self.h += 1
        if self.time > 0:
            self.time -= 1
    def move_ball(self):
        for b in self.balls:
            if abs(b.Vx) >= 0.3:
                b.move()
                b.draw()

            for i in self.targets:
                if b.hittest(i):
                    i.hit()
                    self.score += i.points
                    self.a = self.targets.index(i) + 1
                    self.time = 30
    def move_target(self):
        for t in self.targets:
            if self.h % 100 == 0:
                t.create_bomb(self)
            t.move()
            t.draw()

    def move_bomb(self):
        for q in self.boombs:
            for i in self.machine:
                if q.hittest(i):
                    i.health -= q.damage
                    q.bang()
                    q.hit()
                if q.y > height - 100:
                    q.bang()
                    q.hit()
            q.move()
            q.draw()
    def move_machine(self):
        for i in range(len(self.machine)):
            if i == self.j:
                self.machine[i].move()
            self.machine[i].power_up()
            self.machine[i].draw()
            self.machine[i].healthbar()
    def text_on_screen(self):
        if self.time > 0:
            text = font.render('Вы уничтожили цель ' + str(self.a) + ' за ' + str(self.bullet)
                               + ' выстрелов', True, BLACK, WHITE)
            textRect = text.get_rect()
            place = text.get_rect(center=(length / 2, height / 2))
            screen.blit(text, place)

        text = font.render(str(self.score), True, BLACK, WHITE)
        textRect = text.get_rect()
        place = text.get_rect(center=(50, 50))
        screen.blit(text, place)

        text = font.render('Нажмите SPACE для смены машины, используйте WASD для управления', True, BLACK, WHITE)
        textRect = text.get_rect()
        place = text.get_rect(center=(400, 50))
        screen.blit(text, place)


clock = pygame.time.Clock()

game = manager()
game.append()
while not game.finished:
    clock.tick(FPS)
    game.process()
    game.delete()
    game.tick()
    game.move_ball()
    game.move_target()
    game.move_bomb()
    game.move_machine()
    game.text_on_screen()

    pygame.display.update()
    screen.fill(WHITE)
    rect(screen, GREEN, (0,height - 80, length, 80 ))

pygame.quit()

