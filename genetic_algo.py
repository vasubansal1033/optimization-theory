# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 16:14:57 2020

@author: VASU
"""

from PIL import Image
import sys, pygame
from pygame.locals import *
import random
import pygame.gfxdraw as gfx
import math

target = Image.open("flower.jpg")
target = target.resize((150, 150))
totalx = target.size[0]
totaly = target.size[1]

pygame.init()
DISPLAYSURF = pygame.display.set_mode((totalx,totaly))
pygame.display.set_caption('Art')

trigno = 50
mutation_rate = 0.5
pop_no = 5

WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0)

DISPLAYSURF.fill(WHITE)

def diff(first, second):
    a = (first[0]-second[0])**2
    b = (first[1]-second[1])**2
    c = (first[2]-second[2])**2
    return a + b + c

class Triangle:
    """Triangles that make up each Drawing"""
    def __init__(self):
        self.color = (random.randint(0,255),
        random.randint(0,255),
        random.randint(0,255))
        self.alpha = random.randint(0,255)
        self.points = [
        (random.randint(0,totalx),random.randint(0,totaly)),
        (random.randint(0,totalx),random.randint(0,totaly)),
        (random.randint(0,totalx),random.randint(0,totaly))]        

class Drawing:
    """Pieces of art"""

    def __init__(self):
        self.triangles = []
        for _ in range(trigno):
            t = Triangle()
            self.triangles.append(t)

    def calcfitness(self):
    # calculates fitness via how different each pixel's color is
        totaldiff = 0
        for x in range(target.size[0]):
            for y in range(target.size[1]):
                totaldiff += diff(target.getpixel((x,y)), DISPLAYSURF.get_at((x,y))[:3])
        self.fitness = totaldiff

    def crossover(self, partner):
        child = Drawing()
        for i in range(trigno):
            child.triangles[i].color = random.choice([self.triangles[i].color, partner.triangles[i].color])
            child.triangles[i].points = random.choice([self.triangles[i].points, partner.triangles[i].points])

        return child

    def mutate(self):
        pick_index = random.randint(0, trigno-1)

        if random.random() < mutation_rate:
            index = random.randint(0, 3)
            change = random.randint(0, 255)
            if index == 3:
                self.triangles[pick_index].alpha = change
            else:
                colors = list(self.triangles[pick_index].color)
                colors[index] = change
                self.triangles[pick_index].color = tuple(colors)

        else:
            index = random.randint(0, 2)
            p1 = self.triangles[pick_index].points[0]
            p2 = self.triangles[pick_index].points[1]
            p3 = self.triangles[pick_index].points[2]
            changex = random.randint(0, totalx)
            changey = random.randint(0, totaly)
            change = [p1, p2, p3]
            change[index] = (changex, changey)
            self.triangles[pick_index].points = change

population = []
for _ in range(pop_no):
    population.append(Drawing())

def minfit(drawing):
    return drawing.fitness

gen = 0

record = []

while True:

    print("Generation: " + str(gen))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # calculating fitness...

    count = 1

    for d in population:

        DISPLAYSURF.fill(WHITE)    

        for x in d.triangles:
            surface = pygame.Surface((totalx, totaly))
            surface.set_colorkey((0,0,0))
            surface.set_alpha(x.alpha)
            pygame.draw.polygon(surface, x.color, x.points)
            DISPLAYSURF.blit(surface, (0,0))

        d.calcfitness()
        print(str(count) + ": " + str(d.fitness))
        count += 1

    # choosing best...

    best = min(population, key=minfit)
    record.append(best.fitness)

    # drawing...    

    DISPLAYSURF.fill(WHITE)  

    for x in best.triangles:
        surface = pygame.Surface((totalx, totaly))
        surface.set_colorkey((0,0,0))
        surface.set_alpha(x.alpha)
        pygame.draw.polygon(surface, x.color, x.points)
        DISPLAYSURF.blit(surface, (0,0))

    pygame.display.update()

    # creating mating pool... 

    st = best.triangles

    c1 = Drawing()
    for i in range(trigno):
        c1.triangles[i].color = st[i].color
        c1.triangles[i].alpha = st[i].alpha
        c1.triangles[i].points = st[i].points
    c1.mutate()

    c2 = Drawing()
    for i in range(trigno):
        c2.triangles[i].color = st[i].color
        c2.triangles[i].alpha = st[i].alpha
        c2.triangles[i].points = st[i].points
    c2.mutate()

    c3 = Drawing()
    for i in range(trigno):
        c3.triangles[i].color = st[i].color
        c3.triangles[i].alpha = st[i].alpha
        c3.triangles[i].points = st[i].points
    c3.mutate()

    c4 = Drawing()
    for i in range(trigno):
        c4.triangles[i].color = st[i].color
        c4.triangles[i].alpha = st[i].alpha
        c4.triangles[i].points = st[i].points
    c4.mutate()

    population = []
    population.append(best)
    population.append(c1)
    population.append(c2)
    population.append(c3)
    population.append(c4)

    if gen % 5 == 0:
        pygame.image.save(DISPLAYSURF, str(gen) + ".jpeg")

    print(record)

    gen += 1