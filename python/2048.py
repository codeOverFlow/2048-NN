#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from random import randint
HAUT = 'HAUT'
BAS = 'BAS'
GAUCHE = 'GAUCHE'
DROITE = 'DROITE'

class Game():
    def __init__(self):
        self.mat = [[4,4,2,0],[0,0,0,0],[0,0,0,0], [0,0,0,0]]
        self.free = [(i, j) for i in range(4) for j in range(4) if not self.mat[i][j]]
        x,y = self.free[randint(0, len(self.free)-1)]
        self.mat[x][y] = 2
        self.free = [(i, j) for i in range(4) for j in range(4) if not self.mat[i][j]]
        self.score = 0


    def update(self, direction):
        if direction == DROITE:
            for i in range(4):
                for k in range(3, 0, -1):
                    for j in range(k-1, -1, -1):
                        if self.mat[i][k] == self.mat[i][j]:
                            self.mat[i][k] *= 2
                            self.mat[i][j] = 0
                            if self.mat[i][k] != 0:
                                self.score += 1
                        elif self.mat[i][k] == 0:
                            self.mat[i][k] = self.mat[i][j]
                            self.mat[i][j] = 0
        elif direction == GAUCHE:
            for i in range(4):
                for k in range(3):
                    for j in range(k+1, 4):
                        if self.mat[i][k] == self.mat[i][j]:
                            self.mat[i][k] *= 2
                            self.mat[i][j] = 0
                            if self.mat[i][k] != 0:
                                self.score += 1
                        elif self.mat[i][k] == 0:
                            self.mat[i][k] = self.mat[i][j]
                            self.mat[i][j] = 0
        elif direction == HAUT:
            for i in range(4):
                for k in range(3):
                    for j in range(k+1, 4):
                        if self.mat[k][i] == self.mat[j][i]:
                            self.mat[k][i] *= 2
                            self.mat[j][i] = 0
                            if self.mat[k][i] != 0:
                                self.score += 1
                        elif self.mat[k][i] == 0:
                            self.mat[k][i] = self.mat[j][i]
                            self.mat[j][i] = 0
        elif direction == BAS:
            for i in range(4):
                for k in range(3, 0, -1):
                    for j in range(k-1, -1, -1):
                        if self.mat[k][i] == self.mat[j][i]:
                            self.mat[k][i] *= 2
                            self.mat[j][i] = 0
                            if self.mat[i][k] != 0:
                                self.score += 1
                        elif self.mat[k][i] == 0:
                            self.mat[k][i] = self.mat[i][j]
                            self.mat[j][i] = 0

    def play(self, direction):
        for i in range(4):
            print(self.mat[i])
        print()
        self.update(direction)
        self.free = [(i, j) for i in range(4) for j in range(4) if not self.mat[i][j]]
        x,y = self.free[randint(0, len(self.free)-1)]
        self.mat[x][y] = 2
        self.free = [(i, j) for i in range(4) for j in range(4) if not self.mat[i][j]]
        for i in range(4):
            print(self.mat[i])
        print(self.free)
        print(self.score)
        print('\n')

g = Game()
g.play(GAUCHE)
g.play(HAUT)
g.play(BAS)
g.play(GAUCHE)
g.play(DROITE)
g.play(BAS)
