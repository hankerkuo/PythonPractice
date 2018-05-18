import numpy as np

class AlexNet(object):

    def __init__(self, x):
        self.X = x
        self.create()

    def create(self):
        self.fc8 = 123

print(AlexNet(10).fc8)