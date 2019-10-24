import numpy as np


# this class make a MLP with nodes number 10
class MlpSingle:

    # layers is a integer
    # layer number is not including the input layer
    def __init__(self, layers, input_nodes, output_nodes):
        pass
        self.inputnodes = input_nodes
        self.outputnodes = output_nodes
        self.layers = layers
        self.w, self.b, self.z, self.a = [], [], [], []
        self.w_b_z_s_contain()

    def w_b_z_s_contain(self):
        for i in range(self.layers):
            if i == 0:
                self.w.append(np.random.rand(self.inputnodes, 12) - 0.5)
                self.b.append(np.zeros((1, 12)))
                self.z.append(np.zeros((1, 12)))
                self.a.append(np.zeros((1, 12)))
            elif i == self.layers - 1:
                self.w.append(np.random.rand(12, self.outputnodes) - 0.5)
                self.b.append(np.zeros((1, self.outputnodes)))
                self.z.append(np.zeros((1, self.outputnodes)))
                self.a.append(np.zeros((1, self.outputnodes)))
            else:
                self.w.append(np.random.rand(12, 12) - 0.5)
                self.b.append(np.zeros((1, 12)))
                self.z.append(np.zeros((1, 12)))
                self.a.append(np.zeros((1, 12)))

    def sigmoid(self, x):
        return 1. / (1. + np.exp(-x))

    def sig_deri(self, x):
        return self.sigmoid(x) * (1. - self.sigmoid(x))

    def softmax(self, x):
        exps = np.exp(x - np.max(x))
        return exps / np.sum(exps)

    def forward_prop(self, x):
        x = np.reshape(x, (1, self.inputnodes))
        for num in range(self.layers):
            self.z[num] = np.dot(x, self.w[num]) + self.b[num]
            if num == self.layers - 1:
                self.a[num] = self.softmax(self.z[num])
            else:
                self.a[num] = self.sigmoid(self.z[num])
            x = self.a[num]
        return x

    def back_prop(self, x, y):
        x = np.reshape(x, (1, self.inputnodes))
        y = np.reshape(y, (1, self.outputnodes))
        lr = 0.1

        for num in range(self.layers - 1, -1, -1):
            if num == self.layers - 1:
                # delta = (self.a[num] - y) * self.sig_deri(self.z[num])
                delta = self.z[num] - y
            else:
                delta = np.dot(delta, self.w[num + 1].T) * self.sig_deri(self.z[num])

            if num == 0:
                a = x
            else:
                a = self.a[num - 1]

            w_deri = np.dot(a.T, delta)
            b_deri = delta

            self.w[num] -= lr * w_deri
            self.b[num] -= lr * b_deri

        return self.w
