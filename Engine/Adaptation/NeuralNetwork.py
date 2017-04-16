import numpy as np
import tensorflow as tf
import math


class neuralnetwork():

    def __init__(self):
        self.numInputs = 30
        self.numOutputs = 2
        # Create the model
        self.x = tf.placeholder(tf.float32, [None, self.numInputs]) #placeholder is a value that is given when computing, None means dimension of any length
        self.W = tf.Variable(tf.ones([self.numInputs, self.numOutputs])) #model paramaters are generally variables
        self.b = tf.Variable(tf.zeros([self.numOutputs]))
        self.eta = 0.1

        # Define loss and optimizer
        self.y_ = tf.placeholder(tf.float32, [None, self.numOutputs])

        # So here we use tf.nn.softmax_cross_entropy_with_logits on the raw
        # outputs of 'y', and then average across the batch.
        self.y = tf.matmul(self.x, self.W) + self.b
        self.cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=self.y_, logits=self.y))
        self.train_step = tf.train.GradientDescentOptimizer(self.eta).minimize(self.cross_entropy)
        self.prediction = tf.argmax(self.y,1)

        self.sess = tf.InteractiveSession()
        tf.global_variables_initializer().run()
        self.saver = tf.train.Saver()

    def train(self, X, Y):
        # Train the model
        Xs = X
        Ys = Y
        batch_xs = Xs
        batch_xs = np.reshape(batch_xs, (-1, self.numInputs))
        batch_ys = Ys
        if(str(Ys) == "0"):
            batch_ys = np.array([[1,0]])
        else:
            batch_ys = np.array([[0,1]])
        self.sess.run(self.train_step, feed_dict={self.x: batch_xs, self.y_: batch_ys})

    def save(self):
        save_path = self.saver.save(self.sess, "/tmp/SeniorDesignModel.ckpt")
        print("Model saved in file: %s" % save_path)

    def load(self):
        self.saver.restore(self.sess, "/tmp/SeniorDesignModel.ckpt")

    def run(self, X):
        # Run trained model
        Xs = X
        test_xs = Xs
        test_xs = np.reshape(test_xs, (-1, self.numInputs))
        result = self.prediction.eval(feed_dict={self.x: test_xs}, session=self.sess)
        if(result == 1):
            return "A"
        else:
            return "None"