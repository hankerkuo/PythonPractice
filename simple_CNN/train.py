from simple_CNN.datagen import DataGenerator
from simple_CNN.model import MLP
from simple_CNN.no_batch import MlpSingle
from simple_CNN.MLP_batch import MlpBatch
import platform
import numpy as np

if __name__ == '__main__':
    if platform.system() == 'Windows':
        folder = 'C:/data/train_data'
    elif platform.system() == 'Linux':
        folder = '/home/shaoheng/Documents/Thesis_KSH/training_data/old_data/CCPD_FR_for_classfifcation'

    batch = 5
    data_generator = DataGenerator(folder, batch, (16, 16), class_num=10)
    model = MlpBatch(input_nodes=16*16, hidden_nodes=(20, 12, 10), batch_size=batch)

    right = 0
    for i in range(1000000):
        if (i + 1) % 100 == 0:
            print('acc=%.2f' % (right / (i * batch) * 100), '%')

        x, y = data_generator.load_data()
        out = model.forward_prop(x)
        model.back_prop(x, y)

        for b in range(batch):
            if np.argmax(y[b]) == np.argmax(out[b]):
                right += 1
