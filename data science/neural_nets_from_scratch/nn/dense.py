from actFunc import *
import numpy as np
"""
	modelParam.keys() = ['num_units', 'input_size', 'actFunc']
	load_weights.keys() = ['W', 'b']
"""
def initDense(modelParam, load_weights = None):
	activation = modelParam['actFunc']
	 
	if load_weights == None : 
		num_units = modelParam['num_units']
		input_size = modelParam['input_size']	
		W = np.random.normal(size=[num_units, input_size], scale=1.0/input_size)
		b = np.random.normal(size=[num_units,])
		
	else : 
		W = load_weights['W']
		b = load_weights['b']
	
	modelDense = {'W' : W, 'b': b, 'actFunc' : activation, 'output' : []}
	
	return modelDense

def forwardDense(modelDense, inputDense):
	W = modelDense['W']
	b = modelDense['b']
	actFunc = modelDense['actFunc']
	output = actFunc(np.dot(W, inputDense) + b)
	modelDense['output'].append(output)

	return modelDense

def backwardDense(modelDense, del_out, inputDense):
	W = modelDense['W']
	actFunc = modelDense['actFunc']
	
	del_z = del_out * actFunc(np.dot(W, inputDense), derivative=True)
	del_W =  np.outer(del_z, inputDense)
	del_input = np.dot(W.T, del_z)
	
	modelDense['output'] = modelDense['output'][:-1]
	
	ret = {'model' : modelDense,
			'del_W' : del_W,
			'del_b' : del_z,
			'del_input' : del_input}
	
	return ret

def updateDense(modelDense, deltas, lr):
	modelDense['W'] -= (lr * deltas['del_W'])
	modelDense['b'] -= (lr * deltas['del_b'])
	
	return modelDense

def displayDense(model, display_type) :
	
	if display_type == "Dense_output" :
		print "... Dense ..."
		print "\toutput = ", model['output'][-1]
		print "... END ..."
	
	elif display_type == "Dense_weights" : 
		print "... Dense weights ..."
		print "\tW = ", model['W']
		print "\tb = ", model['b']
		print "... END ..."
	
	elif display_type == "Dense_del" :
		print "... Dense deltas ..."
		print "\tdel_W = ", model['del_W']
		print "\tdel_b = ", model['del_b']
		print "... END ..."
		
	else : print "Unknown model type"	
