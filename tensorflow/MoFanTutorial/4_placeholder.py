import tensorflow as tf

input1 = tf.placeholder(tf.float32)
input2 = tf.placeholder(tf.float32)

output = tf.multiply(input1, input2)

with tf.Session() as sess:
    # the timing that values need to be supervised into the code is sess.run
    print(sess.run(output, feed_dict={input1: [8.], input2: [10.]}))