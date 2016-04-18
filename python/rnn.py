#/bin/env python
# -*- encoding: utf-8 -*-

import tensorflow as tf
from tensorflow.models.rnn import rnn, rnn_cell
import numpy as np

import game

class Rnn_2048:

    def __init__(self, instance_game, size_rnn, learning_rate):
        self.game = instance_game
        self.learning_rate=learning_rate
        self.size_rnn = size_rnn
        self.outputs = game.dirs.values()
        self.output_size = len(self.outputs)
        self.input_size = len(self.game.getLinearMap())


        self.projection_output = {'weights' : tf.Variable(tf.random_normal([self.size_rnn, self.output_size], dtype=tf.float32), name="Output_Weights"),
                                    'biais' : tf.Variable(tf.random_normal([self.output_size], dtype=tf.float32), name="Output_Biais")
                                    }

        self.input_placeholder = tf.placeholder(tf.float32, [None, self.input_size], name="Input_Placeholder")
        self.expect_placeholder = tf.placeholder(tf.float32, [None, self.output_size], name="Expect_Placeholder")
        self.state_placeholder = tf.placeholder(tf.float32, [None, self.size_rnn], name="State_Placeholder")

        self.cell = rnn_cell.BasicRNNCell(self.size_rnn)
        self.state = np.zeros((1, size_rnn))

        self.learning_state, self.learning_output, self.optimizer = self.iteration(self.input_placeholder, self.state_placeholder, self.expect_placeholder)
        self.init = tf.initialize_all_variables()

        self.sess = tf.Session()
        self.sess.run(self.init)

    def initialize(self):
        self.state = np.zeros((1, self.size_rnn))
        self.game.reset()

    def iteration(self, inputs, state, expect):
        new_state, _ = self.cell(inputs, state)
        output = tf.nn.softmax(tf.matmul(new_state, self.projection_output['weights']) + self.projection_output['biais'])

        loss=tf.reduce_mean(-tf.reduce_sum(expect*tf.log(tf.clip_by_value(output, 1e-10, 1.0)), 1))
        optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(loss)

        return new_state, output, optimizer

    @staticmethod
    def softmax(x):
        """Compute softmax values for each sets of scores in x."""
        return np.exp(x) / np.sum(np.exp(x), axis=0)

    def get_expect(self):
        e = []
        for o in self.outputs:
            m,s = self.game.simulate(o)
            e.append(s - 100*(0 if m else 1))

        expect = Rnn_2048.softmax(np.array(e))

        return expect

    def learn(self, nb_game):
        for i in range(nb_game):
            self.initialize()
            playing=True

            while playing:
                self.state, output, opt = self.sess.run([self.learning_state, self.learning_output, self.optimizer], 
                                                                {self.input_placeholder : np.array([self.game.getLinearMap()]), 
                                                                    self.state_placeholder : self.state,
                                                                    self.expect_placeholder : np.array([self.get_expect()])})
                choice = self.outputs[np.argmax(output)]
                playing = self.game.play(choice)

            print self.game.score
            if self.game.score > 150:
                for i in xrange(4):
                    print self.game.mat[i]
            

    def play(self):
        self.state, output = self.sess.run([self.learning_state, self.learning_output], {self.input_placeholder : np.array([self.game.getLinearMap()]), 
                                                                                            self.state_placeholder : self.state})

        choice = self.outputs[np.argmax(output)]
        
        self.game.play(choice)
        print choice


a=Rnn_2048(game.Game(), 80, 0.001)
a.learn(100)
