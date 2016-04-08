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

    def update(self, direction):
        if direction == DROITE:
            for i in xrange(4):
                for k in xrange(3, 0, -1):
                    for j in xrange(k-1, -1, -1):
                        if self.mat[i][k] == self.mat[i][j]:
                            self.mat[i][k] *= 2
                            self.mat[i][j] = 0
                            if self.mat[i][k] != 0:
                                self.score += 1
                                break
                        elif self.mat[i][k] == 0:
                            self.mat[i][k] = self.mat[i][j]
                            self.mat[i][j] = 0
        elif direction == GAUCHE:
            for i in xrange(4):
                for k in xrange(3):
                    for j in xrange(k+1, 4):
                        if self.mat[i][k] == self.mat[i][j]:
                            self.mat[i][k] *= 2
                            self.mat[i][j] = 0
                            if self.mat[i][k] != 0:
                                self.score += 1
                                break
                        elif self.mat[i][k] == 0:
                            self.mat[i][k] = self.mat[i][j]
                            self.mat[i][j] = 0
        elif direction == HAUT:
            for i in xrange(4):
                for k in xrange(3):
                    for j in xrange(k+1, 4):
                        if self.mat[k][i] == self.mat[j][i]:
                            self.mat[k][i] *= 2
                            self.mat[j][i] = 0
                            if self.mat[k][i] != 0:
                                self.score += 1
                                break
                        elif self.mat[k][i] == 0:
                            self.mat[k][i] = self.mat[j][i]
                            self.mat[j][i] = 0
        elif direction == BAS:
            for i in xrange(4):
                for k in xrange(3, 0, -1):
                    for j in xrange(k-1, -1, -1):
                        if self.mat[k][i] == self.mat[j][i]:
                            self.mat[k][i] *= 2
                            self.mat[j][i] = 0
                            if self.mat[k][i] != 0:
                                self.score += 1
                                break
                        elif self.mat[k][i] == 0:
                            self.mat[k][i] = self.mat[j][i]
                            self.mat[j][i] = 0

    def play(self, direction):
        for i in range(4):
            print self.mat[i] 
        print 
        self.update(direction)
        self.generateRandom()
        for i in xrange(4):
            print self.mat[i]
        print self.free.ravel() 
        print self.score 
        print '\n' 

g = Game()

while True:
    g.play(raw_input())
