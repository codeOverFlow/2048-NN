import tensorflow as tf
from tensorflow.models.rnn import rnn, rnn_cell
import numpy as np

import game

class Rnn_2048:

    def __init__(self, instance_game, size_rnn):
        self.game = instance_game
        self.size_rnn = size_rnn
        self.outputs = game.dirs.values()
        self.output_size = len(self.outputs)
        self.input_size = len(self.game.getLinearMap())


        self.projection_output = {'weights' : tf.Variable(tf.random_normal([self.size_rnn, self.output_size], dtype=tf.float32), name="Output_Weights"),
                                    'biais' : tf.Variable(tf.random_normal([self.output_size], dtype=tf.float32), name="Output_Biais")
                                    }

        self.input_placeholder = tf.placeholder(tf.float32, [None, self.input_size], name="Input_Placeholder")
        self.state_placeholder = tf.placeholder(tf.float32, [None, self.size_rnn], name="State_Placeholder")

        self.cell = rnn_cell.BasicRNNCell(self.size_rnn)
        self.state = np.zeros((1, size_rnn))

        self.learning_state, self.learning_output = self.iteration(self.input_placeholder, self.state_placeholder)
        self.init = tf.initialize_all_variables()

        self.sess = tf.Session()
        self.sess.run(self.init)

    def iteration(self, inputs, state):
        new_state, _ = self.cell(inputs, state)
        output = tf.matmul(new_state, self.projection_output['weights']) + self.projection_output['biais']

        return new_state, output

    def play(self):
        self.state, output = self.sess.run([self.learning_state, self.learning_output], {self.input_placeholder : np.array([self.game.getLinearMap()]), 
                                                                                            self.state_placeholder : self.state})

        choice = self.outputs[np.argmax(output)]
        
        self.game.play(choice)
        print choice


a=Rnn_2048(game.Game(), 80)
a.play()
a.play()
a.play()
