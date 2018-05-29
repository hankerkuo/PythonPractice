from six.moves import cPickle as pickle

with open('ptb.pkl', 'rb') as f:
    te_lab = pickle.load(f, encoding='latin1')