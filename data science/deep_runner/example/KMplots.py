from FFN.FFNConfig import Config
import cPickle as pkl
import numpy as np
import matplotlib as mpl
#mpl.rcParams['agg.path.chunksize'] = 500000
import matplotlib.pyplot as plt
from os.path import dirname, basename, exists, splitext
from os import mkdir
from shutil import copyfile

def makePlots(confObj, basename=''):
	
	#copyfile(config_file, directory + 'config.cfg')
	
	for config in confObj.configs:
		outFile = config['FILES']['TRAIN_STATS']
		#base_name = splitext(basename(outFile))[0]
		directory = dirname(outFile)
	
		print "Output file : ", outFile
	
		outData = []
		with open(outFile, 'rb') as f:
			outData = pkl.load(f)
	
	
		if type(outData['cost_list']) == list:
			print "\tCost vs. Epochs (final cost = {})".format(outData['cost_list'][-1])
			fig = plt.figure()
			plt.title('Cost vs. Epochs ')
			plt.xlabel('Number of Epochs')
			plt.ylabel('Cost')
			plt.xlim( (outData['epoch_list'][0], outData['epoch_list'][-1]) )
			plt.ylim( (min(outData['cost_list']), max(outData['cost_list'])) )
			plt.scatter(outData['epoch_list'], outData['cost_list'], color='r', s=1)
		
			plotFile = directory + '/' + basename + 'cost.png'
		
			fig.tight_layout()
			fig.savefig(plotFile, dpi=800)
			plt.close(fig)

		if type(outData['train_accuracy_list']) == list:
			print "\tTraining_Accuracy vs. Epochs (final training accuracy = {})".format(outData['train_accuracy_list'][-1])
			fig = plt.figure()
			plt.title('Training Accuracy vs. Epochs')
			plt.xlabel('Number of Epochs')
			plt.ylabel('Training Accuracy')
			plt.xlim( (outData['epoch_list'][0], outData['epoch_list'][-1]) )
			plt.ylim( (0.0, 100.0) )
			plt.plot(outData['epoch_list'], outData['train_accuracy_list'], 'b')
		
			plotFile = directory + '/' +  basename + 'train_acc.png'
		
			fig.tight_layout()
			fig.savefig(plotFile, dpi=800)			
			plt.close(fig)
	
		if type(outData['test_accuracy_list']) == list:
			print "\tTesting_Accuracy vs. Epochs (final testing accuracy = {})".format(outData['test_accuracy_list'][-1])
			fig = plt.figure()
			plt.title('Testing_Accuracy vs. Epochs')
			plt.xlabel('Number of Epochs')
			plt.ylabel('Testing Accuracy')
			plt.xlim( (outData['epoch_list'][0], outData['epoch_list'][-1]) )
			plt.ylim( (0.0, 100.0) )
			plt.plot(outData['epoch_list'], outData['test_accuracy_list'], 'g')
		
			plotFile = directory + '/' + basename + 'test_acc.png'
		
			fig.tight_layout()
			fig.savefig(plotFile, dpi=800)			
			plt.close(fig)


		if type(outData['conf_mat_test']) == np.ndarray:
			print "\tTest Confusion Matirx : ", outData['conf_mat_test']
			
			plt.matshow(outData['conf_mat_test'], cmap='Greens')
			plt.colorbar()
			plt.xlabel('predicted class')
			plt.ylabel('actual class')
			
			fig = plt.gcf()
			plotFile = directory + '/' + basename + 'confusion_test.png'
			fig.savefig(plotFile, dpi=800)			
			plt.close(fig)
"""

		if type(outData['conf_mat_train']) == np.ndarray:
			print "\tTrain Confusion Matrix : ", outData['conf_mat_train']
		

			fig = plt.figure()
			plt.xlabel('predicted class')
			plt.ylabel('actual class')
			plt.matshow(outData['conf_mat_train'], cmap='Blues')
			plt.colorbar()
		
			plotFile = directory + '/' + 'confusion_train.png'
		
			fig.tight_layout()
			fig.savefig(plotFile, dpi=800)			
			plt.close(fig)

"""
