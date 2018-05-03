from __future__ import print_function
import imageio
import numpy as np
import os
from six.moves import cPickle as pickle

image_size = 16  # Pixel width and height.
pixel_depth = 255.0  # Number of levels per pixel.

def make_data_train_test(folder, train_num):        # folder is the folder path of the dataset, train_num is the desired train data amount
    """Load the data for a single letter label."""
    image_files = os.listdir(folder)                                            # os.listdir shows all of the files and folder under one folder
    train_set = np.ndarray(shape=(train_num, image_size, image_size),           # len(image_files) means the total amount of data, dataset is
                         dtype=np.float32)                                      # a nparray used to store the image data
    test_set = np.ndarray(shape=(len(image_files) - train_num, image_size, image_size),
                         dtype=np.float32)
    image_files_train = np.random.choice(image_files, train_num, replace=False)     # randomly choose the train data
    image_files_test = np.setdiff1d(image_files, image_files_train)                 # the rest data will become test data
    num_images_train = 0
    num_images_test = 0

    for image in image_files_train:
        image_file = os.path.join(folder, image)    # image_file now points to the path of a single image file
        try:
            image_data = (np.sum(imageio.imread(image_file).astype(float), axis=2) / 3 -    # normalize the data, because the image is RGB
                          pixel_depth / 2) / pixel_depth
            if image_data.shape != (image_size, image_size):                                # error prevention
                raise Exception('Unexpected image shape: %s' % str(image_data.shape))
            train_set[num_images_train, :, :] = image_data      # stack single image data into the array
            num_images_train = num_images_train + 1             # prepare to store next data, only operate when exception doesn't come out
        except (IOError, ValueError) as e:
            print('Could not read:', image_file, ':', e, '- it\'s ok, skipping.')

    for image in image_files_test:
        image_file = os.path.join(folder, image)    # image_file now points to the path of a single image file
        try:
            image_data = (np.sum(imageio.imread(image_file).astype(float), axis=2) / 3 -    # normalize the data, because the image is RGB
                          pixel_depth / 2) / pixel_depth
            if image_data.shape != (image_size, image_size):                                # error prevention
                raise Exception('Unexpected image shape: %s' % str(image_data.shape))
            test_set[num_images_test, :, :] = image_data      # stack single image data into the array
            num_images_test = num_images_test + 1             # prepare to store next data, only operate when exception doesn't come out
        except (IOError, ValueError) as e:
            print('Could not read:', image_file, ':', e, '- it\'s ok, skipping.')

    print('Full train_dataset tensor:', train_set.shape)
    print('Full test_dataset tensor:', test_set.shape)
    print('Mean:', np.mean(train_set))
    print('Standard deviation:', np.std(train_set))
    return train_set, test_set

# old version function
def load_letter(folder, min_num_images):        # folder is the folder path of the dataset, min_num_images is the minimum amount of data(hyper)
    """Load the data for a single letter label."""
    image_files = os.listdir(folder)            # os.listdir shows all of the files and folder under one folder
    train_set = np.ndarray(shape=(len(image_files), image_size, image_size),  # len(image_files) means the total amount of data, dataset is
                         dtype=np.float32)                                    # a nparray used to store the image data
    test_set = np.ndarray(shape=(len(image_files), image_size, image_size),
                         dtype=np.float32)
    print(folder)

    random_seed = np.ceil(np.random.rand() * 4)     # to make 1/4 of the digit data be test data
    num_images_train = 0
    num_images_test = 0

    for image in image_files:
        image_file = os.path.join(folder, image)    # image_file now points to the path of a single image file
        try:
            image_data = (np.sum(imageio.imread(image_file).astype(float), axis=2) / 3 -    # normalize the data, because the image is RGB
                          pixel_depth / 2) / pixel_depth
            if image_data.shape != (image_size, image_size):                                # error prevention
                raise Exception('Unexpected image shape: %s' % str(image_data.shape))
            if random_seed % 4 == 0:
                test_set[num_images_test, :, :] = image_data
                num_images_test = num_images_test + 1
            elif random_seed % 4 != 0:
                train_set[num_images_train, :, :] = image_data  # stack single image data into the array
                num_images_train = num_images_train + 1             # prepare to store next data, only operate when exception doesn't come out
        except (IOError, ValueError) as e:
            print('Could not read:', image_file, ':', e, '- it\'s ok, skipping.')
        random_seed += 1

    train_set = train_set[0:num_images_train, :, :]           # just remain the image being read successfully
    test_set = test_set[0:num_images_test, :, :]           # just remain the image being read successfully
    if num_images_train < min_num_images:
        raise Exception('Many fewer images than expected: %d < %d' %
                        (num_images_train, min_num_images))

    print('Full dataset tensor:', train_set.shape)
    print('Mean:', np.mean(train_set))
    print('Standard deviation:', np.std(train_set))
    return train_set, test_set


def make_pickle(data_folders, train_num):      # data_folders is a outer folder which contains folder A ~ J
    dataset_names = []
    if not os.path.exists('./train_data'):
        os.makedirs('./train_data')
    if not os.path.exists('./test_data'):
        os.makedirs('./test_data')
    for folder in os.listdir(data_folders):                     # correction for the mistake on website "os.listdir(data_folders)"
        train_set_filename = './train_data/' + folder + '.pickle'        # stored to the local folder
        test_set_filename = './test_data/' + folder + '.pickle'
        dataset_names.append(folder)
        folder = data_folders + folder         # repoint the folder path to the place we stored them
        print('Pickling from source folder %s' % folder, 'to %s.' % train_set_filename)
        train_set, test_set = make_data_train_test(folder, train_num)
        try:
            with open(train_set_filename, 'wb') as f:
                pickle.dump(train_set, f, pickle.HIGHEST_PROTOCOL)
            with open(test_set_filename, 'wb') as f:
                pickle.dump(test_set, f, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print('Unable to save data to', train_set_filename, ':', e)

    return dataset_names

source_folder = 'C:/data/digits/'
train_datasets = make_pickle(source_folder, 36)