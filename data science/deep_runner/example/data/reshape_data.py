import cPickle as pkl
import numpy as np

folders = ['beta=0/D=0.001/epsilon_set_1/',
			'beta=0/D=0.001/epsilon_set_2/',
			'beta=0/D=0.001/epsilon_set_3/',
			'beta=0/D=0.002/epsilon_set_1/',
			'beta=0/D=0.002/epsilon_set_2/',
			'beta=0/D=0.002/epsilon_set_3/']

filenames = ['test.pkl', 'train.pkl']

for folder in folders:
	print "Folder : ", folder
	
	for filename in filenames:
		data = []
		with open(folder + filename, 'rb') as f:
			data = pkl.load(f)
		
		sample_size = data[0][0].shape[0]
		label_size = data[0][1].shape[0]
		for i in xrange(len(data)):
			a = data[i][0].reshape([sample_size])
			b = data[i][1].reshape([label_size])
			data[i] = (a,b)
		
		with open(folder + filename, 'wb') as f:
			pkl.dump(data, f)
		
		print "\tFilename : ", filename, " Number of samples : ", len(data), "Sample size : ", data[0][0].shape, " Label size : ", data[0][1].shape

		
		
