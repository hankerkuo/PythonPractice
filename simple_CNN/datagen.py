from threading import Thread, Lock
from os import listdir
from os.path import splitext, join, basename
from collections import deque
from random import shuffle

import re
import cv2
import numpy as np
import platform


# for class number = 2
class DataGenerator:

    def __init__(self, img_folder, batch_size, input_shape, class_num):
        self.img_folder = img_folder
        self.batch_size = batch_size
        self.input_shape = input_shape
        self.class_num = class_num
        self.x, self.y = self.create_buffer()
        self.imgs_paths = deque()

    def create_buffer(self):
        x_buffer = np.zeros(shape=(self.batch_size,) + self.input_shape)
        y_buffer = np.zeros(shape=(self.batch_size, self.class_num))

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
            return np.array([1., 0.])
        elif class_name in ['rear']:
            return np.array([0., 1.])

    def get_digit_class(self, file_name):
        class_name = int(basename(file_name)[0])
        one_hot = np.zeros((10,))
        one_hot[class_name] = 1
        return one_hot

    def load_data(self):
        for num in range(self.batch_size):
            if len(self.imgs_paths) == 0:
                self.renew_imgs_paths()
            now_handle = self.imgs_paths.pop()
            self.x[num] = np.sum(cv2.resize(cv2.imread(now_handle), self.input_shape[:2]), axis=2) / 765.
            # self.y[num] = self.get_img_class(now_handle)
            self.y[num] = self.get_digit_class(now_handle)
        # print('data loaded')
        return self.x, self.y


if __name__ == '__main__':
    if platform.system() == 'Windows':
        folder = 'C:/data/train_data'
    elif platform.system() == 'Linux':
        folder = '/home/shaoheng/Documents/PythonPractice/handwritedigit'
    data_generator = DataGenerator(folder, 1, (16, 16), 10)

    while 1:
        x, y = data_generator.load_data()
        print(x)