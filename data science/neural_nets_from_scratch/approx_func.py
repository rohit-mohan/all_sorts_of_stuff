"""
Approximating a function with a simple neural network
"""

from nn.actFunc import *
from nn.dense import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import imageio as im
import os


def create_gif(source, dest):
	filenames =  sorted([source+'/'+fn for fn in os.listdir(source) if fn.endswith('.png')])
	with im.get_writer(dest, mode='I', duration=0.5) as writer:
		for filename in filenames:
			image = im.imread(filename)
			writer.append_data(image)
	writer.close()


def build_dense_architecture(parameters):
	layers = []
	for param in parameters:
		layers.append(initDense(param))
	
	return layers	

def forward_pass(layers, sample):
	layerInput = sample
	for i in xrange(len(layers)):
		layers[i] = forwardDense(layers[i], layerInput)
		layerInput = layers[i]['output'][-1]
	return layerInput

def error_calc(label, prediction):
	return prediction - label

def backward_pass(layers, sample, error):
	e = error	
	updateDeltas = []
	#print range(len(layers))[::-1]
	for i in range(len(layers))[::-1][:-1] :
		ret = backwardDense(layers[i], e, layers[i-1]['output'][-1])
		e = ret['del_input']
		updateDeltas.append(ret)
	
	ret =  backwardDense(layers[0], e, sample)
	updateDeltas.append(ret)
	
	return updateDeltas[::-1]

def add_deltas(oldDeltas, newDeltas, num_per_epoch):
	if oldDeltas == None:
		return newDeltas
	
	for i in range(len(oldDeltas)):
		oldDeltas[i]['del_W'] += newDeltas[i]['del_W']/num_per_epoch
		oldDeltas[i]['del_b'] += newDeltas[i]['del_b']/num_per_epoch
	
	return oldDeltas

def update(layers, deltas, lr):
	for i in range(len(layers)):
		layers[i] = updateDense(layers[i], deltas[i], lr)
	
	return layers

def training(layers, x, y, num_epochs, num_per_epoch, lr, print_after, funcname):
	xtrain = np.array(list(x)[::2])
	ytrain = np.array(list(y)[::2])
	xtest = np.array(list(x)[1::2])
	ytest = np.array(list(y)[1::2]) 
	
	for i in xrange(num_epochs):
	
		deltas = None
		for j in xrange(num_per_epoch):
			index = np.random.randint(0, high = xtrain.shape[0])	
			sample = np.array([xtrain[index]])
			label = ytrain[index]
		
			prediction = forward_pass(layers, sample)
			error = error_calc(label, prediction)		
			updates = backward_pass(layers, sample, error)
			deltas = add_deltas(deltas, updates, num_per_epoch)
	
		update(layers, deltas, lr)
			
		# Validating
		if (i % print_after == print_after-1):
			print "Epoch : ", i+1
			predictions = testing(layers, xtest, ytest)
			
			plt.title('x vs. {}(x) - iter:{}, lr:{}, h_layers:{},h_units:{}'.format(funcname, i+1, lr, num_hidden, hidden_units))
			plt.plot(x, y, color='r')
			plt.plot(xtest,predictions, color='g', linewidth=5, alpha=0.5)
			plt.xlim(np.min(x), np.max(x))
			plt.ylim(np.min(y),np.max(y))
			plt.savefig(funcname + '-gifs/'+str(i/print_after).zfill(3)+'.png')
			plt.close()

def testing(layers, x, y):
	predictions = []
	for index in range(x.shape[0]):
		sample = np.array([x[index]])
		predictions.append(forward_pass(layers, sample))
	return predictions
##########################################################################################


num_samples = 10000
num_epochs = 10000
num_per_epoch = 10
lr = 0.1 
hidden_units = 15
num_hidden = 2
print_after = num_epochs / 20

# Creating dataset
#x = np.linspace(-1*np.pi, 1*np.pi, num_samples)
x = np.linspace(-np.pi, np.pi, num_samples)
y = np.sin(x)
funcname = 'sin'

#Create gif directory
if not(os.path.isdir(funcname + '-gifs')) : os.mkdir(funcname+'-gifs') 

print "func(x) = " + funcname + '(x)'

# Architecture Parameters
hiddenParam1 = {'num_units':hidden_units, 'input_size':1, 'actFunc':sigmoid}
hiddenParam2 = {'num_units':hidden_units, 'input_size':hidden_units, 'actFunc':sigmoid}
outputParam = {'num_units':1, 'input_size':hidden_units, 'actFunc':linear}
parameters = [hiddenParam1] + [hiddenParam2]*(num_hidden - 1) + [outputParam]
layers = build_dense_architecture(parameters)

# Training
print "Training has begun..."
training(layers, x, y, num_epochs, num_per_epoch, lr, print_after, funcname)

# Create GIF
source = funcname + '-gifs'
gifs = sorted([fn for fn in os.listdir(source) if fn.endswith('.gif')])
if gifs == []:
	dest = '001.gif'
else :
	dest = str(int(gifs[-1].split('.')[0]) + 1).zfill(3) + '.gif'
print "Creating GIF ( source : ", source, " destination : ", dest, " )..."
create_gif(source, source + '/' +dest)

# Create log of architecture and training specs in 'record.txt'
print "Making log entry..."
log_string = 'echo "dest : {}, num_epochs : {}, iter_per_epoch : {}, hidden_layers : {}, units_per_layer : {}, lr : {}" >> {}-record.txt'
os.system(log_string.format(dest, num_epochs, num_per_epoch, num_hidden, hidden_units, lr, source+'/'+funcname))

# Removing graphs
print "Removing temporary graphs..."
#os.system('rm -f {}/*.png'.format(source))

print "Exit."






