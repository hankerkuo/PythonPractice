from datagen import DataGenerator
from model import MLP

if __name__ == '__main__':
    folder = '/home/shaoheng/Documents/Thesis_KSH/training_data/old_data/CCPD_FR_for_classfifcation'
    data_generator = DataGenerator(folder, 10, (10, 10, 3))
    model = MLP((10 * 10 * 3, 100, 100, 20, 10, 2))

    while 1:
        x, y = data_generator.load_data()
        output = model.forward_prop(x)
        model.back_prop(output, y)
        print(output)