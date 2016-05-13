#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from random import randint, random
from keras.models import Sequential
from keras.layers.recurrent import SimpleRNN
from keras.layers.core import Dense
from keras.utils.visualize_util import plot
from keras.utils.np_utils import to_categorical
from theano import Variable
from game import Game
import tensorflow as tf
import numpy as np


class RNN():
    def __init__(self, game):
        self.game = game
        self.model = Sequential()
        self.model.add(SimpleRNN(input_dim=17, input_length=1, output_dim=4, activation='softmax', return_sequences=True))
        self.model.compile(optimizer='rmsprop', loss=self.loss, metrics=[self.loss])
        plot(self.model, to_file='model.png', show_shapes=True) 

    def play(self):
        self.model
        x = self.game.getLinearMap();
        x = np.append(x, [self.game.score])
        x = np.array([x]).reshape((-1, 1, 17))
        return self.model.predict_classes(x)

    def loss(self, o, X):
        return tf.Variable(float(1/(self.game.score+1)))
        



if __name__ == '__main__':
    g = Game()
    rnn = RNN(g)
    dirs = {0: 'HAUT', 1: 'BAS', 2: 'GAUCHE', 3: 'DROITE'}
    rnn.play()
    p = True
    while p:
        p = g.play(dirs[rnn.play()[0][0]])
