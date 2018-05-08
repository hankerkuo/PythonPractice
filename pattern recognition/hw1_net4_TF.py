import tensorflow as tf
from six.moves import cPickle as pickle
import numpy as np
from scipy import ndimage
# number 1 to 10 data


def compute_accuracy(v_xs, v_ys):
    global prediction
    y_pre = sess.run(prediction, feed_dict={xs: v_xs})
    correct_prediction = tf.equal(tf.argmax(y_pre, 1), tf.argmax(v_ys, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    result = sess.run(accuracy, feed_dict={xs: v_xs})
    return result


def weight_variable(shape):
    # truncated normal distribution
    # initial = tf.truncated_normal(shape, stddev=0.1)
    if np.shape(shape) == (4,):
        initial = tf.random_uniform(shape, minval=-2.4 / (shape[0] * shape[1]), maxval=2.4 / (shape[0] * shape[1]))
    elif np.shape(shape) == (2,):
        initial = tf.random_uniform(shape, minval=-2.4 / shape[0], maxval=2.4 / shape[0])
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.0, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W):
    # stride [Batch, Height, Width, Channel], in the computer's point if view, it sees just four dimensions
    # so we shouldn't pass through any of samples(batch) or channels
    # Must have strides[0] = strides[3] = 1
    return tf.nn.conv2d(x, W, strides=[1, 2, 2, 1], padding='SAME')


def max_pool_2x2(x):
    # stride [Batch, Height, Width, Channel]
    # ksize [Batch, Height, Width, Channel]
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


# define placeholder for inputs to network
with tf.name_scope('inputs'):
    xs = tf.placeholder(tf.float32, [None, 16, 16], name='x_input')   # 16*16
    ys = tf.placeholder(tf.float32, [None, 10], name='y_input')
x_image = tf.reshape(xs, [-1, 16, 16, 1], name='reshape')

## conv1 layer ##
with tf.name_scope('CNN_1'):
    with tf.name_scope('weight'):
        W_conv1 = weight_variable([3, 3, 1, 2])  # patch 3x3, in size 1, out size 32
    with tf.name_scope('bias'):
        b_conv1 = bias_variable([8, 8, 2])
    with tf.name_scope('Wx_plus_bias_activation'):
        # output size 8x8x2 (16x16x2 -> 8x8x2)
        h_conv1 = 1.7159 * tf.nn.tanh((2 / 3) * (conv2d(x_image, W_conv1) + b_conv1))

## conv2 layer ##
with tf.name_scope('CNN_2'):
    with tf.name_scope('weight'):
        W_conv2 = weight_variable([5, 5, 2, 1])  # patch 5x5, in size 2, out size 1
    with tf.name_scope('bias'):
        b_conv2 = bias_variable([4, 4, 1])
    with tf.name_scope('Wx_plus_bias_activation'):
        # output size 4x4x1 (8x8x2 -> 4x4x1)
        h_conv2 = 1.7159 * tf.nn.tanh((2 / 3) * (conv2d(h_conv1, W_conv2) + b_conv2))

## FC layer ##
with tf.name_scope('FC'):
    with tf.name_scope('weight'):
        W_fc1 = weight_variable([4*4*1, 10])
    with tf.name_scope('bias'):
        b_fc1 = bias_variable([10])
    # [n_samples, 4, 4, 1] ->> [n_samples, 4*4*1]
    with tf.name_scope('flat'):
        h_pool2_flat = tf.reshape(h_conv2, [-1, 4*4*1])
    with tf.name_scope('Wx_plus_bias'):
        h_FC = tf.matmul(h_pool2_flat, W_fc1) + b_fc1
with tf.name_scope('prediction'):
    prediction = tf.nn.softmax(h_FC)
    # prediction = 1.7159 * tf.nn.tanh((2 / 3) * (tf.matmul(h_pool2_flat, W_fc1) + b_fc1))

# the error between prediction and real data, two kinds of cost function
# cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys * tf.log(prediction), reduction_indices=[1]))
with tf.name_scope('loss'):
    mse = tf.reduce_mean(0.5 * tf.square(ys - prediction))
with tf.name_scope('train'):
    train_step = tf.train.AdamOptimizer(1e-4).minimize(mse)

sess = tf.Session()
writer = tf.summary.FileWriter('C:/data/tensorboard/net4/', sess.graph)
init = tf.global_variables_initializer()
sess.run(init)
# saver = tf.train.Saver()
# saver.restore(sess, "my_net/save_net.ckpt")

with open('./train_data/data.pickle', 'rb') as f:
    tr_dat = pickle.load(f)
with open('./train_data/label.pickle', 'rb') as f:
    tr_lab = pickle.load(f)
with open('./test_data/data.pickle', 'rb') as f:
    te_dat = pickle.load(f)
with open('./test_data/label.pickle', 'rb') as f:
    te_lab = pickle.load(f)

# building ndarrays for storing results after filters
tr_dat_after_sobel = np.ndarray(shape=(np.shape(tr_dat)), dtype=np.float32)
tr_dat_after_prewitt = np.ndarray(shape=(np.shape(tr_dat)), dtype=np.float32)
tr_dat_after_laplacian = np.ndarray(shape=(np.shape(tr_dat)), dtype=np.float32)
tr_dat_after_gaussian_laplace = np.ndarray(shape=(np.shape(tr_dat)), dtype=np.float32)

te_dat_after_sobel = np.ndarray(shape=(np.shape(te_dat)), dtype=np.float32)
te_dat_after_prewitt = np.ndarray(shape=(np.shape(te_dat)), dtype=np.float32)
te_dat_after_laplacian = np.ndarray(shape=(np.shape(te_dat)), dtype=np.float32)
te_dat_after_gaussian_laplace = np.ndarray(shape=(np.shape(te_dat)), dtype=np.float32)

# filter operations on training data
for _ in range(320):
    tr_dat_after_sobel[_, :, :] = ndimage.sobel(tr_dat[_, :, :], 0)
    tr_dat_after_prewitt[_, :, :] = ndimage.prewitt(tr_dat[_, :, :], 0)
    tr_dat_after_laplacian[_, :, :] = ndimage.laplace(tr_dat[_, :, :])
    tr_dat_after_gaussian_laplace[_, :, :] = ndimage.gaussian_laplace(tr_dat[_, :, :], sigma=1)

# filter operations on test data
for _ in range(160):
    te_dat_after_sobel[_, :, :] = ndimage.sobel(te_dat[_, :, :], 0)
    te_dat_after_prewitt[_, :, :] = ndimage.prewitt(te_dat[_, :, :], 0)
    te_dat_after_laplacian[_, :, :] = ndimage.laplace(te_dat[_, :, :])
    te_dat_after_gaussian_laplace[_, :, :] = ndimage.gaussian_laplace(te_dat[_, :, :], sigma=1)

### old version : training process starts ###
# to divide data set into how many pieces
# batch_number = 3
# for epoch in range(5000):       # epoch amount
#     for batch_index in range(batch_number):
#         start = int(batch_index * (np.shape(tr_dat)[0] / batch_number))
#         end = int(batch_index * (np.shape(tr_dat)[0] / batch_number) + (np.shape(tr_dat)[0] / batch_number))
#         batch_xs = tr_dat[start:end]
#         batch_ys = tr_lab[start:end]
#         sess.run(train_step, feed_dict={xs: batch_xs, ys: batch_ys})
#     if epoch % 100 == 0:
#         print(epoch, 'th', compute_accuracy(te_dat, te_lab))

# training process starts
batch_size = 32
for epoch in range(3000):       # epoch amount
    for batch in range(len(tr_dat) // batch_size):
        sess.run(train_step, feed_dict={xs: tr_dat[batch * batch_size: (batch + 1) * batch_size],
                                        ys: tr_lab[batch * batch_size: (batch + 1) * batch_size]})
    if epoch % 100 == 0:
        print(epoch, 'th', compute_accuracy(te_dat, te_lab))

writer.close()
sess.close()