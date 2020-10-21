import pygame
import numpy as np

from pygame.draw import *
from random import randint
pygame.init()

FPS = 20


print("Ваше имя:")#узнаём имя игрока
username=input()

global length, height, N0

length = 1200 #длина экрана
height = 900  #высота экрана
N0 = 30      #число шариков на экране

screen = pygame.display.set_mode((length, height))

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
    

ball_list = []
'''
создаём массив со словарями-шарами
x,y - координаты
dx,dy - элементарные перемещения
r - радиус
color - цвет
time - время жизни
    
'''
for i in range(0,N0,1):
    ball_list.append({'ball_x':randint(0,length),'ball_y':randint(0,height),
                    'ball_dx':randint(5,20)*(-1)**randint(1,2),
                    'ball_dy':randint(5,20)*(-1)**randint(1,2),
                    'ball_r':randint(10,40),'ball_color':COLORS[randint(0,5)],
                    'ball_time':randint(50,100)} )

star_list = []
'''
создаём массив со словарями-звёздами
x,y - координаты
dx,dy - элементарные перемещения
r - радиус
color - цвет
time - время жизни
alpha - угол поворота
    
'''
for i in range(0,int(N0/10),1):
    star_list.append({'star_x':randint(0,length),'star_y':randint(0,height),
                    'star_dx':randint(5,20)*(-1)**randint(1,2),
                    'star_dy':randint(5,20)*(-1)**randint(1,2),
                    'star_r':randint(10,40),'star_color':COLORS[randint(0,5)],
                    'star_time':randint(50,100),'star_alpha':randint(0,180)} )


    
def new_ball(x,y,r,color):
    '''
    рисует новый шарик
    x,y - координаты шарика
    r - радиус шариков
    color - цвет шарика
    '''

    circle(screen, color, (x, y), r)

    
def new_star(x,y,R,color,alpha):
    '''
    рисует новую звезду
    x,y - координаты звезды
    R - радиус окружности, описывающую звезду
    alpha - угол поворота звезды
    color - цвет звезды
    '''
    polygon(screen, color, [(x+R*np.sin(alpha/180*np.pi),y-R*np.cos(alpha/180*np.pi)),
                            (x+R*np.sin((36-alpha)/180*np.pi), y+R*np.cos((36-alpha)/180*np.pi)),
                            (x-R/(4*np.cos(18/180*np.pi)*np.cos(18/180*np.pi)-1)*np.sin(alpha/180*np.pi)
                             ,y+R/(4*np.cos(18/180*np.pi)*np.cos(18/180*np.pi)-1)*np.cos(alpha/180*np.pi)),
                            (x-R*np.sin((36+alpha)/180*np.pi), y+R*np.cos((36+alpha)/180*np.pi)),
                            (x+R*np.sin(alpha/180*np.pi),y-R*np.cos(alpha/180*np.pi))])
    polygon(screen, color, [(x-R*np.sin((72-alpha)/180*np.pi),y - R*np.cos((72-alpha)/180*np.pi)),
                            (x+R*np.sin((72+alpha)/180*np.pi),y - R*np.cos((72+alpha)/180*np.pi)),
                            (x-R*np.sin((36+alpha)/180*np.pi), y+R*np.cos((36+alpha)/180*np.pi)),
                            (x-R/(4*np.cos(18/180*np.pi)*np.cos(18/180*np.pi)-1)*np.sin((72+alpha)/180*np.pi), 
                             y+R/(4*np.cos(18/180*np.pi)*np.cos(18/180*np.pi)-1)*np.cos((72+alpha)/180*np.pi)),
                            (x-R*np.sin((72-alpha)/180*np.pi),y - R*np.cos((72-alpha)/180*np.pi))]) 

def move_ball(i):
    '''
    i - номер нужного объкта
    функция создаёт движение шарика для i-ого элемента массива
    '''
    ball_list[i]['ball_x'] += ball_list[i]['ball_dx']
    
    if ball_list[i]['ball_x'] >= length:
        ball_list[i]['ball_dx'] = -ball_list[i]['ball_dx']
    else:
        ball_list[i]['ball_dx'] = ball_list[i]['ball_dx']
    if ball_list[i]['ball_x'] <= 0:
        ball_list[i]['ball_dx'] = -ball_list[i]['ball_dx']
    else:
        ball_list[i]['ball_dx'] = ball_list[i]['ball_dx']
            
    ball_list[i]['ball_y'] += ball_list[i]['ball_dy']
    
    if ball_list[i]['ball_y'] >= height:
        ball_list[i]['ball_dy'] = -ball_list[i]['ball_dy']
    else:
        ball_list[i]['ball_dy'] = ball_list[i]['ball_dy']
    if ball_list[i]['ball_y'] <= 0:
        ball_list[i]['ball_dy'] = -ball_list[i]['ball_dy']
    else:
        ball_list[i]['ball_dy'] = ball_list[i]['ball_dy']
        
def move_star(i):
    '''
    i - номер нужного объекта
    функция создаёт движение шарика для i-ого элемента массива
    '''
    star_list[i]['star_x'] += star_list[i]['star_dx']
    
    if star_list[i]['star_x'] >= length:
        star_list[i]['star_dx'] = -star_list[i]['star_dx']
    else:
        star_list[i]['star_dx'] = star_list[i]['star_dx']
    if star_list[i]['star_x'] <= 0:
        star_list[i]['star_dx'] = -star_list[i]['star_dx']
    else:
        star_list[i]['star_dx'] = star_list[i]['star_dx']
            
    star_list[i]['star_y'] += star_list[i]['star_dy']
    
    if star_list[i]['star_y'] >= height:
        star_list[i]['star_dy'] = -star_list[i]['star_dy']
    else:
        star_list[i]['star_dy'] = star_list[i]['star_dy']
    if star_list[i]['star_y'] <= 0:
        star_list[i]['star_dy'] = -star_list[i]['star_dy']
    else:
        star_list[i]['star_dy'] = star_list[i]['star_dy']

pygame.display.update()
clock = pygame.time.Clock()
finished = False

    
        
while not finished:
    clock.tick(FPS)
    for  i in range(len(ball_list)):
        new_ball(ball_list[i]['ball_x'], ball_list[i]['ball_y'],
                 ball_list[i]['ball_r'], ball_list[i]['ball_color'])
        ball_list[i]['ball_time'] -= 1
        move_ball(i)
        if ball_list[i]['ball_time'] == 0:
            ball_list[i]['ball_time'] = randint(50,100)
            ball_list[i]['ball_x'] = (randint(0,length))
            ball_list[i]['ball_y'] = (randint(0,height))
            ball_list[i]['ball_color'] = (COLORS[randint(0,5)])
    for  i in range(0,int(N0/10),1):
        new_star(star_list[i]['star_x'], star_list[i]['star_y'],
                 star_list[i]['star_r'], star_list[i]['star_color'],
                 star_list[i]['star_alpha'])
        star_list[i]['star_time'] -= 1
        move_star(i)
        star_list[i]['star_alpha'] += 10
        if star_list[i]['star_time'] == 0:
            star_list[i]['star_time'] = randint(50,100)
            star_list[i]['star_x'] = (randint(0,length))
            star_list[i]['star_y'] = (randint(0,height))
            star_list[i]['star_color'] = (COLORS[randint(0,5)])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(0,N0,1):
                if (ball_list[i]['ball_x']-event.pos[0])*(ball_list[i]['ball_x']-event.pos[0])\
                    +(ball_list[i]['ball_y']-event.pos[1])*(ball_list[i]['ball_y']-event.pos[1])\
                    < ball_list[i]['ball_r']*ball_list[i]['ball_r']:
                    
                    #"исчезновение" шарика
                    ball_list[i]['ball_time'] = randint(50,100)
                    ball_list[i]['ball_x'] = (randint(0,length))
                    ball_list[i]['ball_y'] = (randint(0,height))
                    ball_list[i]['ball_color'] = (COLORS[randint(0,5)])
                    score +=1
                else:
                    score +=0
            for i in range(0,int(N0/10),1):
                if (star_list[i]['star_x']-event.pos[0])*(star_list[i]['star_x']-event.pos[0])\
                    +(star_list[i]['star_y']-event.pos[1])*(star_list[i]['star_y']-event.pos[1])\
                    < star_list[i]['star_r']*star_list[i]['star_r']:
                    #"исчезновение" звезды
                    star_list[i]['star_time'] = randint(50,100)
                    star_list[i]['star_x'] = (randint(0,length))
                    star_list[i]['star_y'] = (randint(0,height))
                    star_list[i]['star_color'] = (COLORS[randint(0,5)])
                    
                    score +=5
                else:
                    score +=0
                
    schet(100,100,70,RED,YELLOW,score)        
    pygame.display.update()
    screen.fill(BLACK)

    
    
pygame.quit()

#создаём рейтинг
table=[]
file = open('Results.txt','r')
for i in file.readlines():
    table.append(i.split(':'))
file.close()
table.append([0,username,str(score),'\n'])
tables=sorted(table, key=lambda t: -int(t[2]))

file1 = open('Results.txt','w')
file1.flush()
for i in range(len(tables)):
    file1.write(str(i+1)+':'+tables[i][1]+':'+tables[i][2]+':\n')
file1.close()

print(username,':',score)
