import tensorflow as tf
import numpy as np
from six.moves import cPickle as pickle


def test_accuracy(data, label):
    global a
    equal_or_not = tf.equal(tf.argmax(a, axis=1), tf.argmax(label, axis=1))
    to_float = tf.cast(equal_or_not, tf.float32)
    accuracy = tf.reduce_mean(to_float)
    result = sess.run(accuracy, feed_dict={x: data})
    return result


x = tf.placeholder(dtype=tf.float32, shape=[None, 16, 16])
y = tf.placeholder(dtype=tf.float32, shape=[None, 10])
x_reshape = tf.reshape(x, [-1, 256])

# layer 1
w = tf.Variable(tf.random_uniform([16*16, 10], minval=-0.05, maxval=0.05))
b = tf.Variable(tf.zeros([10]) * 0.1)
z = tf.matmul(x_reshape, w) + b
a = tf.nn.softmax(z)

loss = tf.reduce_mean(0.5 * tf.square(a - y))
train = tf.train.AdamOptimizer(0.0001).minimize(loss)

with open('./train_data/data.pickle', 'rb') as f:
    tr_dat = pickle.load(f)
with open('./train_data/label.pickle', 'rb') as f:
    tr_lab = pickle.load(f)
with open('./test_data/data.pickle', 'rb') as f:
    te_dat = pickle.load(f)
with open('./test_data/label.pickle', 'rb') as f:
    te_lab = pickle.load(f)

batch_size = 1
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for _ in range(30):
        for batch in range(len(tr_dat) // batch_size):
            sess.run(train, feed_dict={x: tr_dat[batch * batch_size: (batch + 1) * batch_size],
                                       y: tr_lab[batch * batch_size: (batch + 1) * batch_size]})
        # print(sess.run(loss, feed_dict={x: tr_dat, y: tr_lab}))
        # print(sess.run(tf.reduce_mean(tf.cast(tf.equal(tf.argmax(a, axis=1), tf.argmax(te_lab, axis=1)), tf.float32)), feed_dict={x: te_dat}))
    print(test_accuracy(te_dat, te_lab))