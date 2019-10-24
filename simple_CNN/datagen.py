from threading import Thread, Lock
from os import listdir
from os.path import splitext, join
from collections import deque
from random import shuffle

import re
import cv2
import numpy as np


# for class number = 2
class DataGenerator:

    def __init__(self, img_folder, batch_size, input_shape):
        self.img_folder = img_folder
        self.batch_size = batch_size
        self.input_shape = input_shape
        self.x, self.y = self.create_buffer()
        self.imgs_paths = deque()

    def create_buffer(self):
        x_buffer = np.zeros(shape=(self.batch_size,) + self.input_shape)
        y_buffer = np.zeros(shape=(self.batch_size, 2))

        return x_buffer, y_buffer

    def renew_imgs_paths(self):
        imgs_paths = []
        for img_file in listdir(self.img_folder):
            if splitext(img_file)[1] in ['.jpg', '.JPG', '.png', '.PNG']:
                imgs_paths.append(join(self.img_folder, img_file))
        shuffle(imgs_paths)
        self.imgs_paths = deque(imgs_paths)

    def get_img_class(self, file_name):
        class_name = re.match(r'.*_(.*)\.', file_name).group(1)
        if class_name in ['front']:
            return np.array([1, 0])
        elif class_name in ['rear']:
            return np.array([0, 1])

    def load_data(self):
        for num in range(self.batch_size):
            if len(self.imgs_paths) == 0:
                self.renew_imgs_paths()
            now_handle = self.imgs_paths.pop()
            self.x[num] = cv2.resize(cv2.imread(now_handle), self.input_shape[:2]) / 255.
            self.y[num] = self.get_img_class(now_handle)
        print('data loaded')
        return self.x, self.y


if __name__ == '__main__':
    folder = '/home/shaoheng/Documents/Thesis_KSH/training_data/old_data/CCPD_FR_for_classfifcation'
    data_generator = DataGenerator(folder, 32, (100, 100, 3))

    while 1:
        x, y = data_generator.load_data()
        print(y)