import tensorflow as tf

matrix1 = tf.constant([[3, 3]])
matrix2 = tf.constant([[2], [2]])

product = tf.matmul(matrix1, matrix2)  # equal to np.dot

# method 1
sess = tf.Session()
results = sess.run(product)
print(results)
sess.close()

# method 2
with tf.Session() as sess:
    results2 = sess.run(product)
    print(results2)                 # method 2 doesn't need sess.close()