import tensorflow as tf

with tf.Session() as session:
    c = tf.constant(1.0)
    x = tf.placeholder(tf.float32, [1], name='x')
    y = tf.placeholder(tf.float32, [1], name='y')
    y = x * c
    x_in = [100]
    y_output = session.run(y, {x:x_in})
    print(y_output)