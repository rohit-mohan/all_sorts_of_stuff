from KMeans.KMeansConfig import Config
import numpy as np
import cPickle as pkl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from os.path import dirname, basename, exists, splitext

def meanVarPlots(confObj) :
	patch_1 = mpatches.Patch(color=[0,0,1], label='Class 1')
	patch_2 = mpatches.Patch(color=[0,1,0], label='Class 2')
	patch_3 = mpatches.Patch(color=[1,0,0], label='Class 3')
	plt.legend(handles=[patch_1, patch_2, patch_3])

	plt.title("Mean vs. Variance Plot of Absolute Magnitude of Signal")
	plt.xlabel("Mean")
	plt.ylabel("Variance")

	inFiles = [conf['FILES']['TEST_DATA'] for conf in confObj.configs]
	outFiles = [conf['FILES']['NETWORK_OUTPUT'] for conf in confObj.configs]

	for fin, fout in zip(inFiles, outFiles):
		print "Data File : ", fin
		with open(fin, 'rb') as f:
			data = pkl.load(f)
	
		for d in data:
			d_abs = np.abs(d[0])
			mean = np.mean(d_abs)
			var = np.var(d_abs)
		
			plt.scatter(mean, var, c=d[1], s=10)
		
		with open(fout, 'rb') as f:
			data = pkl.load(f)
			
		mean_list = data['mean_list']
		num_clusters = data['num_clusters']	
		
		for i in xrange(num_clusters):
			plt.scatter(mean_list[i, 0], mean_list[i, 1], c = 'y', s = 100, alpha=0.3)
		
		plt.savefig(dirname(fout) + '/mean_var.png', dpi=800)
		plt.close()
		del mean_list
		del num_clusters


