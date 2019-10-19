import numpy as np

def sigmoid(x, derivative = False) :
	val = 1 / (1 + np.exp(-x))
	if derivative: return val * (1 - val)
	else : return val 

def tanh(x, derivative = False) :
	val = np.tanh(x)
	if derivative : return 1 - val ** 2
	else : return val

def linear(x, derivative=False):
	if derivative:
		if type(x) == int or type(x) == float:
			return 1.0
		else:
			return np.ones_like(x)
	
	else : return x 

def relu(x, derivative= False):
	val = np.maximum(x, 0)
	
	if derivative : 
		val[val > 0] = 1
		
	return val
