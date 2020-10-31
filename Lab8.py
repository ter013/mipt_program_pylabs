from random import randrange as rnd, choice
import pygame
from pygame.draw import *
pygame.init()
import math
import threading
import time

global length, height

length = 800 #длина экрана
height = 600 #высота экрана



ORANGE = (255,140,0)
WHITE =(255,255,255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

FPS = 30
screen = pygame.display.set_mode((length, height))

font = pygame.font.Font('freesansbold.ttf', 14)
number_of_targets = int(input("Введите число целей"))

score = 0

g = 2 #ускорение свободного падения

class ball():
    def __init__(self, x=20, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.Vx = 0
        self.Vy = 0
        self.color =  choice(COLORS)
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
    
        if self.y >= Y-100:
            self.Vy = -self.Vy
            self.Vx = self.Vx/1.1
        else:
            self.Vy = self.Vy
        if self.y <= 0:
            self.Vy = -self.Vy
        else:
            self.Vy = self.Vy
    def draw(self):
        pygame.draw.circle(screen,self.color, (int(self.x),int(self.y)),int(self.r))

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (obj.x-self.x)**2+(obj.y-self.y)**2<=(obj.r+self.r)**2:
            return True
        else:
            return False


class gun():
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        pygame.draw.line(screen, BLACK, [20, 450], [50, 420], 7)
        self.x1 = 50
        self.y1 = 420  
    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = ball()
        new_ball.r += 5
        self.an = math.atan((event.pos[1]-new_ball.y) / (event.pos[0]-new_ball.x))
        new_ball.Vx = self.f2_power * math.cos(self.an)
        new_ball.Vy = self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
      
        self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        self.x1 = 20 + max(self.f2_power, 20)*math.cos(self.an)
        self.y1 = 450 + max(self.f2_power, 20) * math.sin(self.an)
        if self.f2_on:
            pygame.draw.line(screen, ORANGE, [20, 450], [self.x1, self.y1], 7)
        else:
            pygame.draw.line(screen, BLACK , [20, 450], [self.x1, self.y1], 7)
                    

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            pygame.draw.line(screen, ORANGE, [20, 450], [self.x1, self.y1], 7)
        else:
            pygame.draw.line(screen, BLACK, [20, 450], [self.x1, self.y1], 7)


class target():
    def __init__(self):
        self.points = 0
        self.live = 1
        self.Vx = rnd(1,5)
        self.Vy = rnd(1,5)

        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(10, 30)
        color = self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.Vx = 0
        self.Vy = 0
        self.x = -100
        self.y = -100
        
        self.points += points

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
    
        if self.y >= Y-100:
            self.Vy = -self.Vy
        else:
            self.Vy = self.Vy
        if self.y <= 0:
            self.Vy = -self.Vy
        else:
            self.Vy = self.Vy
    def draw(self):
        pygame.draw.circle(screen,self.color, (self.x,self.y),self.r)

        
            
    

g1 = gun()
bullet = 0

balls = []

a = 0 #отвечает за вывод текста на экран

targets = []
for i in range(number_of_targets):
    targets.append(target())

    
clock = pygame.time.Clock()



time = 0
finished = False
while not finished:
    if time > 0:
        time -= 1
    clock.tick(FPS)
    global gun,targets, score, balls, bullet
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEMOTION:
            g1.targetting(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            g1.fire2_start(event)
            
        if event.type == pygame.MOUSEBUTTONUP:
            g1.fire2_end(event)
        
    g1.power_up()
    
    global a

    
    if time > 0:
        text = font.render('Вы уничтожили цель ' +str(a) +' за ' + str(bullet)
                                    + ' выстрелов', True, BLACK, WHITE)
        textRect = text.get_rect()
        place = text.get_rect(center=(length/2, height/2))
        screen.blit(text, place)
    
    for b in balls:
        if abs(b.Vx) >= 0.3:
            b.move()
            b.draw()

        for i in range(len(targets)):
            if b.hittest(targets[i]):
                targets[i].hit()
                score+=targets[i].points
                a = i+1
                time = 30
    for t in targets:
        t.move()
        t.draw()

    pygame.display.update()
    screen.fill(WHITE)
    text = font.render(str(score), True, BLACK, WHITE)
    textRect = text.get_rect()
    place = text.get_rect(center=(50, 50))
    screen.blit(text, place)        

pygame.quit()

