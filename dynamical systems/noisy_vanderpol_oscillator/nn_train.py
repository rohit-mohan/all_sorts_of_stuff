import network
import numpy as np
import random
import cPickle as pkl
import time

update_weights = 0
base_folder = "data/noise(0.1)/"


def get_data(num_class, test_train):
	train = []
	for i in range(1, num_class + 1):
		fname = "{}{}{}.pkl".format(base_folder, test_train, i)
		print "\t",fname 
		f = open(fname, 'rb')
		data = pkl.load(f)
		f.close()
		train = train + data
		
	return train


num_class = 3
dim = 100000

print "Defining Network"


s = [dim,100, 50, num_class]
b = None
w = None

if update_weights == 1:
	print "Updating weights"
	fname = "{}network.pkl".format(base_folder)
	f = open(fname,  'rb')
	s, b, w = pkl.load(f)
	f.close()

net = network.Network(s, b, w)

print "Getting training data."
tt = "train-class"
train = get_data(num_class, tt)
print "train data size : ", len(train)

print "Getting testing data."
tt = "test-class"
test = get_data(num_class, tt)
print "test data size : ", len(test)

print "Training network"
start = time.time()
net.SGD(training_data=train, epoches=100, minibatch_size=100, eta=5.0, testing_data=None, del_accuracy=0.2, eval_per_epoch=2)
end = time.time()
print "Time taken for training : ", end - start

net.save_network_as_pickle("{}network.pkl".format(base_folder))
print "Network saved."





