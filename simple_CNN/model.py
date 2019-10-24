import numpy as np


class MLP:

    # the 'unit_amounts' augment is a tuple in the format (layer_0 units, layer_1 units...., layer_L units)
    # layer_0 units -> SAME the input size
    # layer_L units -> SAME the class number
    def __init__(self, units):
        self.units = units
        self.last_layer = len(units) - 1
        self.ws, self.bs, self.zs = self.initaization()

    def initaization(self):
        w_container = [0]
        b_container = [0]
        z_container = [0]
        for l, unit in enumerate(self.units):
            if l + 1 > self.last_layer:
                break
            w = np.random.randn(self.units[l], self.units[l + 1]) * 0.01
            b = np.zeros(self.units[l + 1])
            z = np.zeros(self.units[l + 1])
            w_container.append(w)
            b_container.append(b)
            z_container.append(z)
        return w_container, b_container, z_container

    # all the activation functions are in a batch-manner
    def relu(self, z):
        return (z > 0) * z

    def relu_prime(self, z):
        return (z > 0) * np.ones(z.shape)

    def soft_max(self, z):
        exps = np.exp(z - np.max(z))
        exps_sum = np.sum(exps, axis=1, keepdims=True)
        return exps / exps_sum

    def soft_max_prime(self, z):
        return self.soft_max(z) * (1 - self.soft_max(z))

    def cross_entropy(self, a, batch_y):
        return np.sum(-np.log(a) * batch_y)

    def cross_entropy_prime(self, a, batch_y, eps=10e-10):
        return batch_y * -(1. / (a + eps))

    def forward_prop(self, batch_x):
        a = batch_x.reshape((batch_x.shape[0], self.units[0]))
        self.zs[0] = a

        for l, unit in enumerate(self.units):

            if l + 1 > self.last_layer:
                break

            if l + 1 == self.last_layer:
                activation = self.soft_max
            else:
                activation = self.relu

            w = self.ws[l + 1]
            b = self.bs[l + 1]
            z = np.dot(a, w) + b
            self.zs[l + 1] = z
            a = activation(z)

        return a

    def back_prop(self, output, batch_y):
        lr = 0.01
        for l in range(self.last_layer, 0, -1):

            if l == 1:
                activation = lambda x: x
            else:
                activation = self.relu

            w_grad = 0
            if l == self.last_layer:
                # deltas = self.cross_entropy_prime(output, batch_y) * self.soft_max_prime(self.zs[l])
                deltas = batch_y - self.soft_max(self.zs[l])
                print('deltas', deltas.shape)
                for i, delta in enumerate(deltas):
                    # print('zs[l-1]', self.zs[l - 1].shape)
                    w_grad += np.dot(activation(np.expand_dims(self.zs[l - 1][i], axis=1)),
                                                np.expand_dims(delta, axis=0))

            else:
                deltas = np.dot(deltas, self.ws[l + 1].T) * self.relu_prime(self.zs[l])
                print('deltas', deltas.shape)
                for i, delta in enumerate(deltas):
                    w_grad += np.dot(activation(np.expand_dims(self.zs[l - 1][i], axis=1)),
                                                np.expand_dims(delta, axis=0))

            w_grad = np.average(w_grad, axis=0)
            self.ws[l] -= lr * w_grad
            self.bs[l] -= lr * np.sum(deltas, axis=0) / batch_y.shape[0]



