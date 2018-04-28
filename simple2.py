import numpy as np
import os
import imageio
import matplotlib.pyplot as plt
import pickle
import shutil


# a = pickle.load(open('C:/OneDrive/文件/NRLab/python project/PythonPractice/pattern recognition/test_data/0.pickle', 'rb'))
# plt.imshow(a[9], cmap='gray')
# plt.show()
# a = os.listdir('C:/data/digits/0/')
# b = np.random.choice(a, 36, replace=False)
# c = np.setdiff1d(a, b)
# print(len(b))
# print(b)
# print(c)

def random_take_data(mother_folder, train_num):
    for kid_folder in os.listdir(mother_folder):
        for image in os.listdir(mother_folder + kid_folder):
            print(image)
# for image in os.listdir('C:/data/digits_all/'):
#     print(image)
#     shutil.copy('C:/data/digits_all/' + image, 'C:/data/')

random_take_data('C:/data/digits/', 10)
