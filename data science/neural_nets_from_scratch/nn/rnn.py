from actFunc import *
import numpy as np

"""
	modelParam.keys() = ['data_dim', 'num_cells', 'actFunc']
"""
def initRNN(modelParam, load_weights = None):
	num_cells = modelParam['num_cells']
	data_dim = modelParam['data_dim']
	actFunc = modelParam['actFunc']
	in_size = num_cells + data_dim
	
	modelRNN = {}
	modelRNN['actFunc'] = actFunc
	modelRNN['hidden'] = [np.zeros([num_cells, ])]
	if load_weights == None:
		modelRNN['H'] = 2 *  np.random.random(size=[num_cells, in_size]) - 1
		modelRNN['Hb'] = np.random.random(size=[num_cells, ])
	
	else :
		modelRNN['H'] = load_weights['H']
		modelRNN['Hb'] = load_weights['Hb']	
	
	return modelRNN

def forwardRNN(modelRNN, inputRNN):
	W = modelRNN['H']
	b = modelRNN['Hb']
	actFunc = modelRNN['actFunc']
	prev_hidden = modelRNN['hidden'][-1]
	cell_input = np.hstack([inputRNN, prev_hidden])
	
	#print W.shape, cell_input.shape, b.shape
	hidden = actFunc(np.dot(W, cell_input) + b)
	modelRNN['hidden'].append(hidden)
	
	return modelRNN
	

def backwardRNN(modelRNN, inputRNN, del_cur_hidden, del_passed_hidden):
	cur_hidden = modelRNN['hidden'][-1]
	prev_hidden = modelRNN['hidden'][-2]
	cell_input = np.hstack([inputRNN, prev_hidden])
	actFunc = modelRNN['actFunc']
	W = modelRNN['H']
	b = modelRNN['Hb']
	
	del_hidden = del_cur_hidden + del_passed_hidden
	del_z = del_hidden * actFunc(np.dot(W, cell_input) + b, derivative=True) 
	del_W = np.outer(del_z, cell_input)
	del_passed_hidden = np.dot( W[:, -cur_hidden.shape[0] : ].T, del_z)
	del_input = np.dot( W[:, : -cur_hidden.shape[0]].T, del_z)
	
	modelRNN['hidden'] = modelRNN['hidden'][:-1]
	
	ret = {	'model' : modelRNN,
			'del_H' : del_W,
			'del_Hb' : del_z,
			'del_passed_hidden' : del_passed_hidden,
			'del_input' : del_input}
	
	return ret
	

def updateRNN(modelRNN, deltas, lr):
	modelRNN['H'] -= lr * deltas['del_H']
	modelRNN['Hb'] -= lr * deltas['del_Hb']
	
	return modelRNN
	
def displayRNN(modelRNN, display_type): 
	if display_type == "RNN" :
		print "... RNN ..."
		print "\thidden = ", modelRNN['hidden'][-1]
		print "... END ..."
	
	elif display_type == "RNN_weights" : 
		print "... RNN weights ..."
		print "\tW = ", modelRNN['H']
		print "\tb = ", modelRNN['Hb']
		print "... END ..."
	
	elif display_type == "RNN_del" :
		print "... RNN deltas ..."
		print "\tdel_W = ", modelRNN['del_H']
		print "\tdel_b = ", modelRNN['del_Hb']
		print "... END ..."
		
	else : print "Unknown model type"	
