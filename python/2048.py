#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from random import randint
import numpy as np

HAUT = 'HAUT'
BAS = 'BAS'
GAUCHE = 'GAUCHE'
DROITE = 'DROITE'

class Game():
    def __init__(self):
        self.mat = np.zeros([4,4])
        self.generateRandom()
        self.score = 0

    def reFree(self):
        self.free = np.array([(i, j) for i in range(4) for j in range(4) if not self.mat[i][j]])
        
    def generateRandom(self):
        self.reFree()
        x,y = self.free[randint(0, len(self.free)-1)]
        self.mat[x][y] = 2
        self.reFree()

    def getLinearMap(self):
        return self.mat.flatten()

    @staticmethod
    def moveTab(tab, inverse=False):
        if inverse:
            tab = tab[::-1]

        ind = 0
        next_values = [i+1 for i,v in enumerate(tab[1:]) if tab[1:][i] != 0]

        mouv = False
        score = 0

        for n in next_values:
            print n
            if tab[ind] == 0:
                tab[ind] = tab[n]
                tab[n] = 0
                mouv = True
            elif tab[ind] == tab[n]:
                tab[ind] *= 2
                tab[n] = 0
                ind += 1
                score += 1
                mouv = True
            elif n != ind+1:
                tab[ind+1] = tab[n]
                tab[n] = 0
                ind += 1
                mouv = True
            else:
                ind+=1

        return mouv, score

    @staticmethod
    def move(mat, direction):
        mouv = False
        score = 0
        if direction == DROITE:
            for i in xrange(4):
                m,s = Game.moveTab(mat[i], inverse=True)
                mouv = m or mouv
                score += s
        elif direction == GAUCHE:
            for i in xrange(4):
                m,s = Game.moveTab(mat[i])
                mouv = m or mouv
                score += s
        elif direction == HAUT:
            for i in xrange(4):
                m,s = Game.moveTab(mat[:,i])
                mouv = m or mouv
                score += s
        elif direction == BAS:
            for i in xrange(4):
                m,s = Game.moveTab(mat[:,i], inverse=True)
                mouv = m or mouv
                score += s

        return mouv, score

    def update(self, direction):
        return Game.move(self.mat, direction)

    def play(self, direction):
        for i in range(4):
            print self.mat[i] 
        print 
        if self.update(direction):
            self.generateRandom()
        for i in xrange(4):
            print self.mat[i]
        print self.free.ravel() 
        print self.score 
        print '\n' 

g = Game()

while True:
    g.play(raw_input())
