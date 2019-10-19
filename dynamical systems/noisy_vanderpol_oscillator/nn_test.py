import network
import cPickle as pkl

base_folder = "data/noise(0.1)/"

"""
ratio = 0.7
def slice_with_ratio(data, ratio):
	num3 = len(data)
	num1 = 0
	num2 = int(ratio * num3)

	return data[num1 : num2], data[num2 : num3]
"""


def get_data(num_class):
	test = []

	for i in range(1, num_class + 1):
		fname = "{}train-class{}.pkl".format(base_folder, i)
		print "\t",fname 
		f = open(fname, 'rb')
		data = pkl.load(f)
		test = test + data

	return test


num_class = 3

print "Getting network parameters"
fname = "{}network.pkl".format(base_folder)
f = open(fname,  'rb')
s, b, w = pkl.load(f)
f.close()
net = network.Network(s, b, w)

print "Getting test data"
test = get_data(num_class)
num_test = len(test)
print "test set size : ", num_test

print "Evaluating test dataset"
print "Accuracy on test dataset : ", float(net.evaluate(test))/num_test * 100, " %"
