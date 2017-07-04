import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data

from data_handling.mnist_data_set import MnistDataSet

dataset = MnistDataSet(validation_sample_count=5000)
dataset.load_dataset()
total_samples_seen = 0
while True:
    samples, labels, indices = dataset.get_next_batch(batch_size=1000)
    total_samples_seen += 1000
    if dataset.isNewEpoch:
        break

print("X")



# mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
#
#
#
# W1_shape = [5, 5, 1, 32]
# b1_shape = [32]
#
# x = tf.placeholder(tf.float32)
# initial_W1 = tf.truncated_normal(shape=W1_shape, stddev=0.1)
# W1 = tf.Variable(initial_W1)
# initial_b1 = tf.constant(0.1, shape=b1_shape)
# b1 = tf.Variable(initial_b1)
# conv1 = tf.nn.conv2d(x, W1, strides=[1, 1, 1, 1], padding='SAME')
#
# sess = tf.Session()
#
# # Run init ops
# init = tf.global_variables_initializer()
# sess.run(init)

#

