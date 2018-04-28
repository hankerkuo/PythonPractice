from __future__ import print_function
import imageio
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import tarfile
from IPython.display import display, Image
from sklearn.linear_model import LogisticRegression
from six.moves.urllib.request import urlretrieve
from six.moves import cPickle as pickle

image_size = 28  # Pixel width and height.
pixel_depth = 255.0  # Number of levels per pixel.


def load_letter(folder, min_num_images):        # folder is the folder path of the dataset, min_num_images is the minimum amount of data(hyper)
    """Load the data for a single letter label."""
    image_files = os.listdir(folder)            # os.listdir shows all of the files and folder under one folder
    dataset = np.ndarray(shape=(len(image_files), image_size, image_size),  # len(image_files) means the total amount of data, dataset is
                         dtype=np.float32)                                  # a nparray used to store the image data
    print(folder)
    num_images = 0
    for image in image_files:
        image_file = os.path.join(folder, image)    # image_file now points to the path of a single image file
        try:
            image_data = (imageio.imread(image_file).astype(float) -    #normalize the data
                          pixel_depth / 2) / pixel_depth
            if image_data.shape != (image_size, image_size):
                raise Exception('Unexpected image shape: %s' % str(image_data.shape))
            dataset[num_images, :, :] = image_data  # stack single image data into the array
            num_images = num_images + 1             # prepare to store next data, only operate when exception doesn't come out
        except (IOError, ValueError) as e:
            print('Could not read:', image_file, ':', e, '- it\'s ok, skipping.')

    dataset = dataset[0:num_images, :, :]           # just remain the image being read successfully
    if num_images < min_num_images:
        raise Exception('Many fewer images than expected: %d < %d' %
                        (num_images, min_num_images))

    print('Full dataset tensor:', dataset.shape)
    print('Mean:', np.mean(dataset))
    print('Standard deviation:', np.std(dataset))
    return dataset


def maybe_pickle(data_folders, min_num_images_per_class, force=False):      # data_folders is a outer folder which contains folder A ~ J
    dataset_names = []
    for folder in os.listdir(data_folders):                     # correction for the mistake on website "os.listdir(data_folders)"
        set_filename = folder + '.pickle'
        dataset_names.append(set_filename)
        if os.path.exists(set_filename) and not force:          # if the set_filename already exists, then skip making data
            # You may override by setting force=True.
            print('%s already present - Skipping pickling.' % set_filename)
        else:
            print('Pickling %s.' % set_filename)
            folder = data_folders + folder         # repoint the folder path to the place we stored them
            dataset = load_letter(folder, min_num_images_per_class)
            try:
                with open(set_filename, 'wb') as f:
                    pickle.dump(dataset, f, pickle.HIGHEST_PROTOCOL)
            except Exception as e:
                print('Unable to save data to', set_filename, ':', e)

    return dataset_names

train_folders = 'C:/data/notMNIST_large/'
test_folders = 'C:/data/notMNIST_small/'
train_datasets = maybe_pickle(train_folders, 45000)
test_datasets = maybe_pickle(test_folders, 1800)