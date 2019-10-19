import numpy as np
import cPickle as pkl

def slice_with_ratio(data, ratio):
	num3 = len(data)
	num1 = 0
	num2 = int(ratio * num3)

	return data[num1 : num2], data[num2 : num3]

num = 1000
base_folder = 'data/noise(0.1)/'
classes = ['eta(-0.2)', 'eta(-0.075)', 'eta(0.2)']
class_labels = [[0,0,1], [0,1,0], [1,0,0]]
ratio = 0.7

class_count = 1
for c, l in zip(classes, class_labels):
	dataset = []
	folder = base_folder + c
	print "Folder : ", folder, " label : ", l
	
	for i in range(1, num + 1):
		fname = "{}/{}.pkl".format(folder,i)
		print "\t", fname
		f = open(fname, 'rb')
		timeseries = pkl.load(f)
				
		dataset.append( ( np.array(timeseries).reshape(len(timeseries), 1), np.array(l).reshape(len(l), 1) ) )

		f.close()
	
	
	dataset_train, dataset_test = slice_with_ratio(dataset, 0.7)
	
	f = open("test-class{}.pkl".format(c), 'wb')
	pkl.dump(dataset_test, f)
	f.close()

	f = open("train-class{}.pkl".format(c), 'wb')
	pkl.dump(dataset_train, f)
	f.close()	
	
	


print "Dataset created."
