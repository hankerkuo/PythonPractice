from datagen import DataGenerator
from model import MLP
from no_batch import MlpSingle
from MLP_batch import MlpBatch
import platform
import numpy as np

if __name__ == '__main__':
    if platform.system() == 'Windows':
        folder = 'C:/data/train_data'
    elif platform.system() == 'Linux':
        folder = '/home/shaoheng/Documents/PythonPractice/handwritedigit'

    batch = 5
    class_num = 10

    data_generator = DataGenerator(
        folder, batch, (16, 16), class_num=class_num)
    model = MlpBatch(input_nodes=16*16,
                     hidden_nodes=(12, class_num), batch_size=batch)

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
