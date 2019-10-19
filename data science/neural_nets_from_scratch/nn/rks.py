import numpy as np

def initRKS(modelParam, load_weights = None):
	outDim = modelParam['out_dim'] / 2
	inDim = modelParam['in_dim']
	sigma = modelParam['sigma']
	
	if load_weights == None : 
		W = np.random.normal(size=[outDim, inDim], scale = sigma)
			
	else : 
		W = load_weights['W']
		
	modelRKS = {'W' : W,'output' : []}
	
	return modelRKS


def forwardRKS(modelRKS, inputRKS):
	W = modelRKS['W']
	outMul = np.dot(W, inputRKS)
	output = np.vstack([np.cos(outMul), np.sin(outMul)])
	modelRKS['output'].append(output)
	
	return modelRKS


def backwardRKS(modelRKS):
	modelRKS['output'] = modelRKS['output'][:-1]
	
	return modelRKS
