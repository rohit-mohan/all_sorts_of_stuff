import numpy as np
import cPickle as pkl

def slice_with_ratio(data, ratio):
	num3 = len(data)
	num1 = 0
	num2 = int(ratio * num3)

	return data[num1 : num2], data[num2 : num3]

num = 1000
classes = ['1', '2', '3']
ratio = 0.7

dataset_train = []
dataset_test = []

for c in classes:
	dataset = []
	print "Folder : ", c
	
	for i in range((int(c)-1) * num + 1, int(c) * num + 1):
		fname = "{}/{}.pkl".format(c,i)
		print "\t", fname
		f = open(fname, 'rb')
		timeseries, l = pkl.load(f)
				
		dataset.append( ( np.array(timeseries), np.array(l) ) )

		f.close()
	
	
	train, test = slice_with_ratio(dataset, 0.7)
	
	dataset_train = dataset_train + train
	dataset_test = dataset_test + test
	

f = open("test.pkl", 'wb')
pkl.dump(dataset_test, f)
f.close()

f = open("train.pkl", 'wb')
pkl.dump(dataset_train, f)
f.close()	

print "Dataset created."
