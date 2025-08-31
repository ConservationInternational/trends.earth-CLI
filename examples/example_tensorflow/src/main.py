"""Custom Script"""

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data


def model(x):
    """"""
    W = tf.Variable(tf.zeros([784, 10]))
    b = tf.Variable(tf.zeros([10]))
    return tf.matmul(x, W) + b


def run(params, logger):
    # Import data
    mnist = input_data.read_data_sets("/tmp/tensorflow/mnist/input_data", one_hot=True)
    learning_rate = 0.5

    # Create the model
    x = tf.placeholder(tf.float32, [None, 784])
    y = model(x)
    y_ = tf.placeholder(tf.float32, [None, 10])

    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y)
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(cross_entropy)

    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()

    # Train
    for _ in range(1000):
        batch_xs, batch_ys = mnist.train.next_batch(100)
        sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

    # Test trained model
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
    return "Done"
