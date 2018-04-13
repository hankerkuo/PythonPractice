import  numpy as np
import tensorflow as tf

y_data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
results = tf.reduce_sum(y_data)
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    print(sess.run(results))
