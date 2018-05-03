from PIL import Image
import numpy as np
import tensorflow as tf

####################################################################################################


def compute_accuracy(v_xs, v_ys):
    global predict
    y_pre = sess.run(predict, feed_dict={x: v_xs})
    correct_prediction = tf.equal(y_pre, tf.argmax(v_ys, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    result = sess.run(accuracy, feed_dict={x: v_xs})
    return result


def get_digit_data():

    fileName = np.array([])
    digits = [i for i in range(10)]

    labels = np.array([])

    for digit in digits:
        fileName = np.append(fileName, [str(digit) + '_' + str(i + 1) + '.png' for i in range(48)])

    np.random.shuffle(fileName)

    datasets = np.array([])

    for name in fileName:
        filePath = "./HandWriteDigit/" + name
        labels = np.append(labels, name[0])
        im = Image.open(filePath).convert("L")
        image = np.array(im)
        datasets = np.append(datasets, image).reshape(-1, 256)

    trainX = np.array(datasets[:320])
    testX = np.array(datasets[320:])

    labels = labels.astype(int)

    trainY = np.zeros((320, 10))
    trainY[np.arange(320),labels[:320]] = 1
    testY = np.zeros((160,10))
    testY[np.arange(160),labels[320:]] = 1

    return (trainX / 255), trainY, (testX / 255), testY

####################################################################################################

def init_weights(shape):
    weights = tf.random_uniform(shape, minval=-2.4 / 256, maxval=2.4 / 256)
    return tf.Variable(weights, name='weight')

def squashing_function(x):
    return tf.multiply(1.7159, tf.tanh(x * (2/3)), name='squashing_function')

### Net-1 : A Single Layer Network


trainX, trainY, testX, testY = get_digit_data()
with tf.name_scope('input'):
    x = tf.placeholder("float", shape=[None, 256], name='x_input')
    y = tf.placeholder(tf.float32, [None, 10], name='y_input')

with tf.name_scope('layer1'):
    w = init_weights((256, 10))
    b = tf.Variable(tf.zeros([10]), name='bias')
    h = tf.add(tf.matmul(x, w), b, name='x_multiply_W_plus_b')

with tf.name_scope('activation'):
    z = squashing_function(h)
    predict = tf.argmax(z, axis=1)

with tf.name_scope('train'):
    cost = tf.reduce_sum((1/2) * tf.pow(tf.subtract(y, z), 2), name='cost')
    updates = tf.train.AdamOptimizer(1e-4).minimize(cost, name='optimizer')

sess = tf.Session()
writer = tf.summary.FileWriter('C:/data/tensorboard/abc/', sess.graph)
init = tf.global_variables_initializer()
sess.run(init)

# for i in range(10):

for epoch in range(300):
    avg_cost = 0.0
    for i in range(len(trainX)):
        o, c = sess.run([updates, cost], feed_dict={x: trainX[i:i+1], y: trainY[i:i+1]})
        avg_cost += c / len(trainX)
    # train_accuracy = np.mean(np.argmax(trainY, axis=1) ==
    #                           sess.run(predict, feed_dict={x: trainX}))
    # test_accuracy = np.mean(np.argmax(testY, axis=1) ==
    #                         sess.run(predict, feed_dict={x: testX}))
    # print("Epoch = %d, train accuracy = %.2f%%, test accuracy = %.2f%%, cost = %.2f"
    #       % (epoch + 1, 100. * train_accuracy, 100. * test_accuracy, avg_cost))
    print(compute_accuracy(testX, testY))

sess.close()
writer.close()
