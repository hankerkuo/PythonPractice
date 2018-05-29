import tensorflow as tf
from six.moves import cPickle as pickle
from filter_operators import *
import os
from variable_control import *
# number 1 to 10 data


def compute_accuracy(v_xs, v_ys):
    global prediction
    y_pre = sess.run(prediction, feed_dict={xs: v_xs})
    correct_prediction = tf.equal(tf.argmax(y_pre, 1), tf.argmax(v_ys, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    result = sess.run(accuracy, feed_dict={xs: v_xs, ys: v_ys})
    return result


def weight_variable(shape):
    # truncated normal distribution
    # initial = tf.truncated_normal(shape, stddev=0.1)
    if np.shape(shape) == (4,):
        initial = tf.random_uniform(shape, minval=-2.4 / (shape[0] * shape[1]), maxval=2.4 / (shape[0] * shape[1]))
    elif np.shape(shape) == (2,):
        initial = tf.random_uniform(shape, minval=-2.4 / shape [0], maxval=2.4 / shape[0])
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
with tf.name_scope('input'):
    xs = tf.placeholder(tf.float32, [None, 16, 16], name='x_input')   # 16*16
    ys = tf.placeholder(tf.float32, [None, 10], name='y_input')
    x_image = tf.reshape(xs, [-1, 16, 16, 1], name='x_reshape')

# define step
global_step = tf.Variable(0, dtype=tf.int32, trainable=False, name='global_step')

# conv1 layer
with tf.name_scope('convnet1'):
    W_conv1 = weight_variable([3, 3, 1, 2])  # patch 3x3, in size 1, out size 32
    b_conv1 = bias_variable([8, 8, 2])
    h_conv1 = 1.7159 * tf.nn.tanh((2 / 3) * (conv2d(x_image, W_conv1) + b_conv1))  # output size 8x8x2 (16x16x2 -> 8x8x2)
    # h_after_filter = tf.py_func(sobel_operator_nd, [h_conv1], tf.float32)

# conv2 layer
with tf.name_scope('convnet2'):
    W_conv2 = weight_variable([5, 5, 2, 4])  # patch 5x5, in size 2, out size 4
    b_conv2 = bias_variable([4, 4, 4])
    h_conv2 = 1.7159 * tf.nn.tanh((2 / 3) * (conv2d(h_conv1, W_conv2) + b_conv2))  # output size 4x4x1 (8x8x2 -> 4x4x4)

# fc1 layer
with tf.name_scope('fc_layer'):
    W_fc1 = weight_variable([4*4*4, 10])
    b_fc1 = bias_variable([10])
    # [n_samples, 4, 4, 4] ->> [n_samples, 4*4*4]
    h_pool2_flat = tf.reshape(h_conv2, [-1, 4*4*4])

prediction = tf.nn.softmax(tf.matmul(h_pool2_flat, W_fc1) + b_fc1, name='prediction_softmax')
# prediction = 1.7159 * tf.nn.tanh((2 / 3) * (tf.matmul(h_pool2_flat, W_fc1) + b_fc1))


# the error between prediction and real data, two kinds of cost function
with tf.name_scope('loss'):
    cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys * tf.log(prediction),
                                                  reduction_indices=[1]))       # loss
    mse = tf.reduce_mean(0.5 * tf.square(ys - prediction))

with tf.name_scope('training_process'):
    train_step = tf.train.AdamOptimizer(1e-4).minimize(mse, name='optimizer',  global_step=global_step)

with tf.name_scope('saver'):
    saver = tf.train.Saver()

# define the accuracy estimating tensor
with tf.name_scope('accuracy'):
    same_or_not = tf.equal(tf.argmax(prediction, 1), tf.argmax(ys, 1))
    accuracy = tf.reduce_mean(tf.cast(same_or_not, tf.float32))

# summary
with tf.name_scope("summaries"):
    tf.summary.scalar("loss", mse)
    tf.summary.scalar("accuracy", accuracy)
    tf.summary.histogram("histogram loss", mse)
    summary_op = tf.summary.merge_all()

# data loading and preprocessing
with open('./train_data/data.pickle', 'rb') as f:
    tr_dat = pickle.load(f)
with open('./train_data/label.pickle', 'rb') as f:
    tr_lab = pickle.load(f)
with open('./test_data/data.pickle', 'rb') as f:
    te_dat = pickle.load(f)
with open('./test_data/label.pickle', 'rb') as f:
    te_lab = pickle.load(f)


# activate the whole process
with tf.Session() as sess:
    init = tf.global_variables_initializer()
    sess.run(init)

    ckpt = tf.train.get_checkpoint_state(os.path.dirname('./checkpoint/net5/save_net.ckpt'))
    if ckpt and ckpt.model_checkpoint_path:
        saver.restore(sess, ckpt.model_checkpoint_path)

    # write log files using a FileWriter
    # access the tensorboard, -> tensorboard --logdir=C:\data\tensorboard\net4 , in this tf version no '' for logdir!!
    writer_train = tf.summary.FileWriter('C:/data/tensorboard/net5/no_batch/train/', sess.graph)
    writer_test = tf.summary.FileWriter('C:/data/tensorboard/net5/no_batch/test/', sess.graph)

    # input data filter operation
    # tr_dat = prewitt_operator(tr_dat, threshold=0, axis=1)
    # te_dat = prewitt_operator(te_dat, threshold=0, axis=1)

    # training process starts
    batch_size = 1
    for epoch in range(3000):  # epoch amount
        for batch in range(len(tr_dat) // batch_size):
            train_op, loss = sess.run([train_step, mse], feed_dict={
                xs: tr_dat[batch * batch_size: (batch + 1) * batch_size],
                ys: tr_lab[batch * batch_size: (batch + 1) * batch_size]})
            # incremental average (refresh average loss after every epoch)
            try:
                average_loss += 1 / (batch + 1) * (loss - average_loss)
            except:
                average_loss = 0
        if (epoch + 1) % 100 == 0:
            print((epoch + 1), 'th test accuracy = %.3f' % compute_accuracy(te_dat, te_lab), end=' ')
            print('train accuracy = %.3f' % compute_accuracy(tr_dat, tr_lab), end=' ')
            print('(loss = %.4f)' % average_loss)
            summary_test = sess.run(summary_op, feed_dict={xs: te_dat, ys: te_lab})
            summary_train = sess.run(summary_op, feed_dict={xs: tr_dat, ys: tr_lab})
            # save check point (named by the number of mini batch which has already fed into the NN)
            # saver.save(sess, './checkpoint/net5/save_net.ckpt', global_step=(epoch + 1) * (len(tr_dat) // batch_size))
            writer_test.add_summary(summary_test, global_step=(epoch + 1) * (len(tr_dat) // batch_size))
            writer_train.add_summary(summary_train, global_step=(epoch + 1) * (len(tr_dat) // batch_size))
        average_loss = 0

    writer_test.close()
    writer_train.close()




