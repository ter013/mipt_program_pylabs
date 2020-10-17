import pygame
import numpy as np

from pygame.draw import *
from random import randint
pygame.init()

FPS = 20
screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def cifra(x0,y0,a,color,n):
    '''
    функция рисует цифры от 0 до 9
    x0,y0 - координаты левого нижнего угла
    а - размер цифры
    color - цвет
    n - сама цифра
    '''
    if n == 0:
        pygame.draw.line(screen, color, [x0, y0], [x0+a, y0], 5)
        pygame.draw.line(screen, color, [x0+a, y0], [x0+a, y0-2*a], 5)
        pygame.draw.line(screen, color, [x0+a, y0-2*a], [x0, y0-2*a], 5)
        pygame.draw.line(screen, color, [x0, y0-2*a], [x0, y0], 5)
    if n == 1:
        pygame.draw.line(screen, color, [x0+a, y0], [x0+a, y0-2*a], 5)
    if n == 2:
        pygame.draw.line(screen, color, [x0, y0], [x0+a, y0], 5)
        pygame.draw.line(screen, color, [x0, y0-a], [x0+a, y0-a], 5)
        pygame.draw.line(screen, color, [x0, y0-2*a], [x0+a, y0-2*a], 5)
        pygame.draw.line(screen, color, [x0+a, y0-a], [x0+a, y0-2*a], 5)
        pygame.draw.line(screen, color, [x0, y0], [x0, y0-a], 5)
    if n == 3:
        pygame.draw.line(screen, color, [x0, y0], [x0+a, y0], 5)
        pygame.draw.line(screen, color, [x0, y0-a], [x0+a, y0-a], 5)
        pygame.draw.line(screen, color, [x0, y0-2*a], [x0+a, y0-2*a], 5)
        pygame.draw.line(screen, color, [x0+a, y0], [x0+a, y0-2*a], 5)
    if n == 4:
        pygame.draw.line(screen, color, [x0+a, y0], [x0+a, y0-2*a], 5)
        pygame.draw.line(screen, color, [x0, y0-a], [x0+a, y0-a], 5)
        pygame.draw.line(screen, color, [x0, y0-2*a], [x0, y0-a], 5)
    if n == 5:
        pygame.draw.line(screen, color, [x0, y0], [x0+a, y0], 5)
        pygame.draw.line(screen, color, [x0, y0-a], [x0+a, y0-a], 5)
        pygame.draw.line(screen, color, [x0, y0-2*a], [x0+a, y0-2*a], 5)
        pygame.draw.line(screen, color, [x0, y0-2*a], [x0, y0-a], 5)
        pygame.draw.line(screen, color, [x0+a, y0], [x0+a, y0-a], 5)
    if n == 6:
        pygame.draw.line(screen, color, [x0, y0-2*a], [x0, y0], 5)
        pygame.draw.line(screen, color, [x0, y0], [x0+a, y0], 5)
        pygame.draw.line(screen, color, [x0, y0-a], [x0+a, y0-a], 5)
        pygame.draw.line(screen, color, [x0, y0-2*a], [x0+a, y0-2*a], 5)                
        pygame.draw.line(screen, color, [x0+a, y0], [x0+a, y0-a], 5)
    if n == 7:
        pygame.draw.line(screen, color, [x0+a, y0], [x0+a, y0-2*a], 5)
        pygame.draw.line(screen, color, [x0+a, y0-2*a], [x0, y0-2*a], 5)
    if n == 8:
        pygame.draw.line(screen, color, [x0, y0-2*a], [x0, y0], 5)
        pygame.draw.line(screen, color, [x0+a, y0], [x0+a, y0-2*a], 5)
        pygame.draw.line(screen, color, [x0, y0], [x0+a, y0], 5)
        pygame.draw.line(screen, color, [x0, y0-a], [x0+a, y0-a], 5)
        pygame.draw.line(screen, color, [x0, y0-2*a], [x0+a, y0-2*a], 5)
    if n == 9:
        pygame.draw.line(screen, color, [x0, y0], [x0+a, y0], 5)
        pygame.draw.line(screen, color, [x0, y0-a], [x0+a, y0-a], 5)
        pygame.draw.line(screen, color, [x0, y0-2*a], [x0+a, y0-2*a], 5)
        pygame.draw.line(screen, color, [x0+a, y0], [x0+a, y0-2*a], 5)
        pygame.draw.line(screen, color, [x0, y0-2*a], [x0, y0-a], 5)
        
# score - счёт   
global score
score = 0

def schet(x0,y0,b,color1,color2,N):
    '''
    функция выводит счёт на экран
    xo,y0 - координаты левого верхнего угла квадратика
    b - сторона квадратика
    color1 - цвет квадратика
    color2 - цвет цифор
    N - счёт
    
    '''
    rect(screen, color1, (x0, y0, b, b))
    cifra(x0+b/5,y0+3/4*b,b/4,color2, int(N/10))
    cifra(x0+11*b/20,y0+3/4*b,b/4,color2, N-10*int(N/10))
    
    
#листы для шаров

ball_list_x = [] #координаты по оси X

ball_list_y = [] #координаты по оси Y

ball_list_dx = [] #элементарное перемещение по оси X

ball_list_dy = [] #элементарное перемещение по оси Y

ball_list_r = [] #радиус шара

ball_list_colors = [] #цвет шара

ball_list_time = [] #время жизни шара
    
def new_ball(x,y,r,color):
    '''
    рисует новый шарик
    x,y - координаты шарика
    r - радиус шариков
    color - цвет шарика
    '''

    circle(screen, color, (x, y), r)

def move_ball():
    '''
    функция создаёт движение шарика для i-ого элемента массива
    '''
    ball_list_x[i] += ball_list_dx[i]
    
    if ball_list_x[i] >= 1200:
        ball_list_dx[i] = -ball_list_dx[i]
    else:
        ball_list_dx[i] = ball_list_dx[i]
    if ball_list_x[i] <= 0:
        ball_list_dx[i] = -ball_list_dx[i]
    else:
        ball_list_dx[i] = ball_list_dx[i]
            
    ball_list_y[i] += ball_list_dy[i]
    
    if ball_list_y[i] >= 900:
        ball_list_dy[i] = -ball_list_dy[i]
    else:
        ball_list_dy[i] = ball_list_dy[i]
    if ball_list_y[i] <= 0:
        ball_list_dy[i] = -ball_list_dy[i]
    else:
        ball_list_dy[i] = ball_list_dy[i]

def pop_insert():
    '''
    функция позволяет пропадать i-ому шарику после клика
    '''
    ball_list_x.pop(i)
    ball_list_y.pop(i)
    ball_list_dx.pop(i)
    ball_list_dy.pop(i)
    ball_list_r.pop(i)
    ball_list_colors.pop(i)
    ball_list_time.pop(i)
    
    ball_list_x.insert(i,randint(0,1200))
    ball_list_y.insert(i,randint(0,900))
    dx0 = randint(20,40) 
    dy0 = randint(20,40)
    ball_list_dx.insert(i,dx0*(-1)**randint(1,2))
    ball_list_dy.insert(i,dy0*(-1)**randint(1,2))
    ball_list_r.insert(i,randint(10,40))
    ball_list_colors.insert(i,COLORS[randint(0,5)])
    ball_list_time.insert(i,randint(5,40))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

#заполняем листы
for  i in range(0,40,1):
    ball_list_x.append(randint(0,1200))
    ball_list_y.append(randint(0,900))
    dx0 = randint(20,40) 
    dy0 = randint(20,40)
    ball_list_dx.append(dx0*(-1)**randint(1,2))
    ball_list_dy.append(dy0*(-1)**randint(1,2))
    ball_list_r.append(randint(10,40))
    ball_list_colors.append(COLORS[randint(0,5)])
    ball_list_time.append(randint(5,40))
    
    
    
    
        
while not finished:
    clock.tick(FPS)

    for  i in range(0,40,1):
        new_ball(ball_list_x[i], ball_list_y[i],ball_list_r[i], ball_list_colors[i])
        ball_list_time[i] -= 1
        move_ball()
        if ball_list_time[i] == 0:
            pop_insert()
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(0,40,1):
                if (ball_list_x[i]-event.pos[0])*(ball_list_x[i]-event.pos[0])\
                    +(ball_list_y[i]-event.pos[1])*(ball_list_y[i]-event.pos[1])\
                    < ball_list_r[i]*ball_list_r[i]:
                    
                    pop_insert()
                    
                    score +=1
                else:
                    score +=0
            
            
    schet(100,100,70,RED,YELLOW,score)
    pygame.display.update()
    screen.fill(BLACK)

    
    
pygame.quit()
