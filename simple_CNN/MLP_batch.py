import numpy as np


class MlpBatch:

    # hidden nodes can be a tuple, including the output layer
    def __init__(self, input_nodes, hidden_nodes, batch_size):
        self.inputnodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.layers = len(hidden_nodes)
        self.batch_size = batch_size
        self.w, self.b, self.z, self.a = [], [], [], []
        self.w_b_z_s_container()

    def w_b_z_s_container(self):
        for i in range(self.layers):
            if i == 0:
                self.w.append(np.random.rand(self.inputnodes, self.hidden_nodes[i]) - 0.5)
            else:
                self.w.append(np.random.rand(self.hidden_nodes[i - 1], self.hidden_nodes[i]) - 0.5)
            self.b.append(np.zeros((1, self.hidden_nodes[i])))
            self.z.append(np.zeros((self.batch_size, self.hidden_nodes[i])))
            self.a.append(np.zeros((self.batch_size, self.hidden_nodes[i])))

    def sigmoid(self, x):
        return 1. / (1. + np.exp(-x))

    def sigmoid_derivative(self, x):
        return self.sigmoid(x) * (1. - self.sigmoid(x))

    def softmax(self, x):
        exps = np.exp(x - np.max(x))
        return exps / np.sum(exps, axis=1, keepdims=True)

    def forward_prop(self, x):
        x = np.reshape(x, (self.batch_size, self.inputnodes))
        for num in range(self.layers):
            self.z[num] = np.dot(x, self.w[num]) + self.b[num]
            if num == self.layers - 1:
                self.a[num] = self.softmax(self.z[num])
            else:
                self.a[num] = self.sigmoid(self.z[num])
            x = self.a[num]
        return x

    def back_prop(self, x, y):
        x = np.reshape(x, (self.batch_size, self.inputnodes))
        y = np.reshape(y, (self.batch_size, self.hidden_nodes[-1]))
        lr = 0.01

        for num in range(self.layers - 1, -1, -1):
            if num == self.layers - 1:
                # delta = (self.a[num] - y) * self.sig_deri(self.z[num])
                delta = self.z[num] - y
            else:
                delta = np.dot(delta, self.w[num + 1].T) * self.sigmoid_derivative(self.z[num])

            if num == 0:
                a = x
            else:
                a = self.a[num - 1]

            w_deri = np.dot(a.T, delta) / self.batch_size
            b_deri = np.average(delta, axis=0)

            self.w[num] -= lr * w_deri
            self.b[num] -= lr * b_deri

        return self.w, self.b, self.z, self.a
