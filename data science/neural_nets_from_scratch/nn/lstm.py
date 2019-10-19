from actFunc import *
import numpy as np

"""
modelParam.keys() = ["data_dim",
					"num_cells",
					"outFunc",
					"inFunc",
					"gateFunc"]
					
					
load_weights.keys() = ["I", "Ib", "G", "Gb", "F", "Fb", "O", "Ob"]
"""
def initLSTM(modelParam, load_weights = None):
	data_dim = modelParam['data_dim']
	num_cells = modelParam['num_cells']	
	
	modelLSTM = {} 
	modelLSTM['state'] = [np.zeros([num_cells,])]
	modelLSTM['hidden'] = [np.zeros([num_cells,])]
	modelLSTM['i_hat'] = []
	modelLSTM['g_hat'] = []
	modelLSTM['f_hat'] = []
	modelLSTM['o_hat'] = []
	
	if load_weights == None :
		in_size = data_dim + num_cells
		modelLSTM['I'] = np.random.normal(size=[num_cells, in_size], scale=1/float(in_size))
		modelLSTM['Ib'] = np.random.normal(size=[num_cells,])
		modelLSTM['G'] = np.random.normal(size=[num_cells, in_size], scale=1/float(in_size))
		modelLSTM['Gb'] = np.random.normal(size=[num_cells,])
		modelLSTM['F'] = np.random.normal(size=[num_cells, in_size], scale=1/float(in_size))
		modelLSTM['Fb'] = np.random.normal(size=[num_cells,])
		modelLSTM['O'] = np.random.normal(size=[num_cells, in_size], scale=1/float(in_size))
		modelLSTM['Ob'] = np.random.normal(size=[num_cells,])
	
	else :
		modelLSTM['I'] = load_weights['I']
		modelLSTM['Ib'] = load_weights['Ib']
		modelLSTM['G'] = load_weights['G']
		modelLSTM['Gb'] = load_weights['Gb']
		modelLSTM['F'] = load_weights['F']
		modelLSTM['Fb'] = load_weights['Fb']
		modelLSTM['O'] = load_weights['O']
		modelLSTM['Ob'] = load_weights['Ob']
	
	modelLSTM['outFunc'] = modelParam['outFunc']
	modelLSTM['inFunc'] = modelParam['inFunc']
	modelLSTM['gateFunc'] = modelParam['gateFunc']
	
	return modelLSTM


""" 					
 modelLSTM.keys() = ["state", 
 				"hidden",
 				"i_hat", 
 				"g_hat", 
 				"f_hat", 
 				"o_hat",
 				"I",
 				"Ib",
 				"G",
 				"Gb",
 				"F",
 				"Fb",
 				"O", 
 				"Ob",
 				"outFunc", 
 				"inFunc",
 				"gateFunc"] 
"""
def forwardLSTM(modelLSTM, inputLSTM):
	cellInput = np.hstack( ( inputLSTM,  modelLSTM['hidden'][-1] ) )
	
	I = modelLSTM['I']
	Ib = modelLSTM['Ib']
	G = modelLSTM['G']
	Gb = modelLSTM['Gb']
	F = modelLSTM['F']
	Fb = modelLSTM['Fb']
	O = modelLSTM['O']
	Ob = modelLSTM['Ob']
	outFunc = modelLSTM['outFunc']
	inFunc = modelLSTM['inFunc']
	gateFunc = modelLSTM['gateFunc']
	
	i_hat = np.dot(I, cellInput) + Ib
	i = inFunc(i_hat)
	modelLSTM['i_hat'].append(i_hat)
	
	g_hat = np.dot(G, cellInput) + Gb
	g = gateFunc(g_hat)
	modelLSTM['g_hat'].append(g_hat)
	
	f_hat = np.dot(F, cellInput) + Fb
	f = gateFunc(f_hat)
	modelLSTM['f_hat'].append(f_hat)
	
	o_hat = np.dot(O, cellInput) + Ob
	o = gateFunc(o_hat)
	modelLSTM['o_hat'].append(o_hat)
	
	prev_state = modelLSTM['state'][-1]
	state = (i * g) + (f * prev_state)
	modelLSTM['state'].append(state)
	
	hidden = o * outFunc(state)
	modelLSTM['hidden'].append(hidden)
	
	return modelLSTM


def backwardLSTM(modelLSTM, inputLSTM, del_cur_hidden, del_passed_hidden, del_passed_state):
	
	outFunc = modelLSTM['outFunc']
	inFunc = modelLSTM['inFunc']
	gateFunc = modelLSTM['gateFunc']
	cur_state = modelLSTM['state'][-1]
	prev_state = modelLSTM['state'][-2]
	cur_hidden = modelLSTM['hidden'][-1]
	prev_hidden = modelLSTM['hidden'][-2]
	cell_input = np.hstack((inputLSTM, cur_hidden))
	i_hat = modelLSTM['i_hat'][-1]
	i = inFunc(i_hat)
	g_hat = modelLSTM['g_hat'][-1]
	g = gateFunc(g_hat)
	f_hat = modelLSTM['f_hat'][-1]
	f = gateFunc(f_hat)
	o_hat = modelLSTM['o_hat'][-1]
	o = gateFunc(o_hat)
	
	del_cur_hidden += del_passed_hidden
	
	del_cur_state = del_cur_hidden * o * outFunc(cur_state, derivative=True) + del_passed_state
	del_passed_state = del_cur_state * f
	
	del_o_hat = del_cur_hidden * outFunc(cur_state) * gateFunc(o_hat, derivative=True)
	del_f_hat = del_cur_state * prev_state * gateFunc(f_hat, derivative=True)
	del_g_hat = del_cur_state * i * gateFunc(g_hat, derivative=True)
	del_i_hat = del_cur_state * g * inFunc(i_hat, derivative=True)
	
	del_I = np.outer( del_i_hat, cell_input)
	del_F = np.outer( del_f_hat, cell_input)
	del_G = np.outer( del_g_hat, cell_input)
	del_O = np.outer( del_o_hat, cell_input)
	
	
	del_passed_hidden = np.dot( modelLSTM['I'][:, -del_i_hat.shape[0] : ].T, del_i_hat) +  \
						np.dot( modelLSTM['G'][:, -del_g_hat.shape[0] : ].T, del_g_hat) +  \
						np.dot( modelLSTM['F'][:, -del_f_hat.shape[0] : ].T, del_f_hat) +  \
						np.dot( modelLSTM['O'][:, -del_o_hat.shape[0] : ].T, del_o_hat)
	
	del_input = np.dot( modelLSTM['I'][:, : -del_i_hat.shape[0]].T, del_i_hat) +  \
				np.dot( modelLSTM['G'][:, : -del_g_hat.shape[0]].T, del_g_hat) +  \
				np.dot( modelLSTM['F'][:, : -del_f_hat.shape[0]].T, del_f_hat) +  \
				np.dot( modelLSTM['O'][:, : -del_o_hat.shape[0]].T, del_o_hat)
	
	modelLSTM['state'] = modelLSTM['state'][:-1]
	modelLSTM['hidden'] = modelLSTM['hidden'][:-1]
	modelLSTM['i_hat'] = modelLSTM['i_hat'][:-1]
	modelLSTM['g_hat'] = modelLSTM['g_hat'][:-1]
	modelLSTM['f_hat'] = modelLSTM['f_hat'][:-1]
	modelLSTM['o_hat'] = modelLSTM['o_hat'][:-1]
	
	ret =  {'model' : modelLSTM,
			'del_I' : del_I,
			'del_Ib': del_i_hat,
			'del_F' : del_F,
			'del_Fb': del_f_hat,
			'del_G' : del_G,
			'del_Gb': del_g_hat,
			'del_O' : del_O,
			'del_Ob': del_o_hat,
			'del_passed_hidden' : del_passed_hidden,
			'del_passed_state' : del_passed_state,
			'del_input' : del_input}

	return ret

def updateLSTM(modelLSTM, deltas, lr):
	modelLSTM['I'] = modelLSTM['I'] - lr * deltas['del_I']
	modelLSTM['Ib'] = modelLSTM['Ib'] - lr * deltas['del_Ib']
	modelLSTM['G'] = modelLSTM['G'] - lr * deltas['del_G']
	modelLSTM['Gb'] = modelLSTM['Gb'] - lr * deltas['del_Gb']
	modelLSTM['F'] = modelLSTM['F'] - lr * deltas['del_F']
	modelLSTM['Fb'] = modelLSTM['Fb'] - lr * deltas['del_Fb']
	modelLSTM['O'] = modelLSTM['O'] - lr * deltas['del_O']
	modelLSTM['Ob'] = modelLSTM['Ob'] - lr * deltas['del_Ob']

	return modelLSTM




def displayLSTM(model, display_type):
	if display_type == "LSTM" :
		print "... LSTM Cell ..."
		print "\tstate = ", model['state'][-1]
		print "\thidden = ", model['hidden'][-1]
		print "\ti = ", model['inFunc'](model['i_hat'][-1])
		print "\tg = ", model['gateFunc'](model['g_hat'][-1])
		print "\tf = ", model['gateFunc'](model['f_hat'][-1])
		print "\to = ", model['gateFunc'](model['o_hat'][-1])
		print "... END ..."
	
	elif display_type == "LSTM_weights" : 
		print "... LSTM Weights ..."
		print "\tI = ", model['I']
		print "\tIb = ", model['Ib']
		print "\tG = ", model['G']
		print "\tGb = ", model['Gb']
		print "\tF = ", model['F']
		print "\tFb = ", model['Fb']
		print "\tO = ", model['O']
		print "\tOb = ", model['Ob']
		print "... END ..."
	
	elif display_type == "LSTM_del" :
		print "... LSTM deltas ..."
		print "\tdel_I = ", model['del_I']
		print "\tdel_Ib = ", model['del_Ib']
		print "\tdel_G = ", model['del_G']
		print "\tdel_Gb = ", model['del_Gb']
		print "\tdel_F = ", model['del_F']
		print "\tdel_Fb = ", model['del_Fb']
		print "\tdel_O = ", model['del_O']
		print "\tdel_Ob = ", model['del_Ob']
		print "\tdel_passed_ hidden = ", model['del_passed_hidden']
		print "\tdel_passed_state = ", model['del_passed_state']
		print "\tdel_input = ", model['del_input']
		print "... END .."	
	
	else :
		print "Unknown model type."








