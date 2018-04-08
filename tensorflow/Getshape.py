import tensorflow as tf
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
arr = tf.constant(arr)
with tf.Session() as session:
    print(arr.get_shape())
    print(session.run(arr))
