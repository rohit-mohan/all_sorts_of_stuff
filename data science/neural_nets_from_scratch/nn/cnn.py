from actFunc import *
import numpy as np

def output_size(matrix_size, filter_size, stride):
	return [(matrix_size[0] - filter_size[0]) / stride[0] + 1, 
			(matrix_size[1] - filter_size[1]) / stride[1] + 1]

def pad(M, filter_size, pad_type='center'):
	matrix_size = M.shape
	
	if pad_type == 'center':
		pad_row_size = [int(np.floor(filter_size[0]/2)), int(np.floor(filter_size[0]/2))]
		pad_col_size = [int(np.floor(filter_size[1]/2)), int(np.floor(filter_size[1]/2))] 

	elif pad_type == 'full' :
		pad_row_size = [filter_size[0]-1, filter_size[0]-1] 
		pad_col_size = [filter_size[1]-1, filter_size[1]-1] 		
	
	size = (pad_row_size, pad_col_size)
	
	if len(matrix_size) > 2:
		size.append( (0,0) )
	
	M = np.pad(M, size, mode='constant')
	return M

def fill_stride_gap(W, stride):
	size = W.shape
	new_size = [size[0] + size[0] * (stride[0]-1), size[1] + size[1] * (stride[1]-1) ]
	if new_size == size: return W
	new_W = np.zeros(new_size)
	
	for i_new, i in zip( range(0, new_size[0], stride[0]), range(size[0]) ) :
		for j_new, j in zip( range(0, new_size[1], stride[1]), range(size[1]) ):
			new_W[i_new, j_new] = W[i, j]
	
	return new_W

def convolution(M, W, stride, padding='valid'):
	
	if padding != 'valid':
		M = pad(M, W.shape, padding)	
	
	filter_size = W.shape
	matrix_size = M.shape
	
	
		
	out_size = output_size(matrix_size, filter_size, stride)
	
	out = []
	for i in range(0,matrix_size[0] - filter_size[0] + 1, stride[0]):
		for j in range(0, matrix_size[1] - filter_size[0] + 1, stride[1]):
			val = np.dot(M[i:i+filter_size[0], j:j+filter_size[1]].flatten(), W.flatten())
			out.append(val)
	
	out = np.array(out).reshape(out_size)
	#if out.shape == (2,2) : print "conv : ", out
	return out

def conv2dense(outputConv):
	return outputConv.flatten()

def dense2conv(outputDense, shape):
	return outputDense.reshape(shape)
		

"""
modelParam.keys() = [input_size, num_filters, filter_size, stride, actFunc, pad_input]
load_weights.keys() = [filters, biases, out_size, stride, actFunc]
"""
def initConv(modelParam, load_weights=None):
	modelConv = {}
	
	if load_weights != None:
		load_weights['output'] = []
		return load_weights
	
	input_size = modelParam['input_size']
	num_filters = modelParam['num_filters']
	filter_size = modelParam['filter_size']
	modelConv['stride'] = modelParam['stride']
	modelConv['actFunc'] = modelParam['actFunc']
	modelConv['pad_input'] = modelParam['pad_input']
	
	out_size = output_size(input_size,filter_size, modelConv['stride'])
	modelConv['out_size'] = out_size + [num_filters]
	W = []
	b = []
	for i in range(num_filters): 
		W.append( np.random.normal(size=filter_size, scale=1.0/filter_size[1]) )
		b.append( np.random.random(size=out_size) )
	
	modelConv['filters'] = W
	modelConv['biases'] = b
	modelConv['output'] = []
	
	return modelConv

def forwardConv(modelConv, inputConv):
	actFunc = modelConv['actFunc']
	out_size = modelConv['out_size']
	num_filters = len(modelConv['filters'])
	
	if modelConv['pad_input'] :
			inputConv = pad(inputConv, modelConv['filters'][0].shape, pad_type='center')
	
	out = np.zeros(out_size)
	for i in range(num_filters) : 
		z = convolution(inputConv, modelConv['filters'][i], modelConv['stride']) + modelConv['biases'][i]
		#print 'z : ', z
		out[:, :, i] = actFunc( z ) 
		#print 'conv out : ', out[:,:,i]
		
	modelConv['output'].append(out)
	
	return modelConv

def backwardConv(modelConv, inputConv, del_out) :
	actFunc = modelConv['actFunc']
	num_filters = len(modelConv['filters'])
	in_depth = inputConv.shape[2]
	
	if modelConv['pad_input'] :
		inputConv = pad(inputConv, modelConv['filters'][0].shape, pad_type='center')
	 
	stride = modelConv['stride']
	filters = modelConv['filters']
	biases = modelConv['biases']
	
	del_filters = []
	del_b = []
	del_input = np.zeros_like(inputConv)
	
	for i in xrange(num_filters):
		del_z = del_out[:,:,i] * actFunc( convolution(inputConv, filters[i], stride) + biases[i], derivative=True)
		
		stride_filled_del = fill_stride_gap(del_z, stride) 
		flipped_filter = np.rot90(filters[i], 2, (0,1))
		del_filter = np.zeros_like(filters[0])
		for j in xrange(in_depth):
			del_filter[:,:,j] = convolution(inputConv[:,:,j], stride_filled_del, [1,1])
			del_input[:,:,j] += convolution(stride_filled_del, flipped_filter[:,:,j], [1,1], padding='full')  
		
		del_filters.append(del_filter)
		del_b.append(del_z)
	
	if modelConv['pad_input']:
		crop_size = np.floor(np.array(modelConv['filters'][0].shape) / 2).astype(int)
		del_input = del_input[crop_size[0]:-crop_size[0], crop_size[1]:-crop_size[1]]
	
	modelConv['output'] = modelConv['output'][:-1]
	
	ret = {'model' : modelConv,
			'del_filters' : del_filters,
			'del_biases' : del_b,
			'del_input' : del_input}	
	
	return ret

def updateConv(modelConv, deltas, lr):
	num_filters = len(modelConv['filters'])
	for i in xrange(num_filters):
		modelConv['filters'][i] -= lr * deltas['del_filters'][i]
		modelConv['biases'][i] -= lr * deltas['del_biases'][i]
	
	return modelConv 
			
def displayDense(model, display_type) :	
	if display_type == "Conv" :
		print "... Convolution ..."
		print "\toutput = ", model['output'][-1]
		print "... END ..."
	
	elif display_type == "Conv_weights" : 
		print "... Conv weights ..."
		print "\tFilters = ", model['Filters']
		print "\tBiases = ", model['biases']
		print "... END ..."
	
	elif display_type == "Conv_del" :
		print "... Conv deltas ..."
		print "\tdel_filters = ", model['del_filters']
		print "\tdel_biases = ", model['del_biases']
		print "... END ..."
		
	else : print "Unknown model type"	
		


"""
modelParam.keys() = [input_size, window, stride, pool_type]
"""			
def initPool(modelParam):
	modelPool = {}
	input_size = modelParam['input_size']
	modelPool['window']  = modelParam['window']
	modelPool['stride'] = modelParam['stride']
	modelPool['pool_type'] = modelParam['pool_type']
	modelPool['indices'] = []
	modelPool['output'] = []
	modelPool['out_size'] = output_size(input_size, modelPool['window'], modelPool['stride']) + [input_size[2]]
	return modelPool

def forwardPool(modelPool, inputPool):
	stride = modelPool['stride']
	filter_size = modelPool['window']
	matrix_size = inputPool.shape[0:2]
	depth = inputPool.shape[2]
	
	out_size = modelPool['out_size']
	out = np.zeros(out_size)
	ind = np.zeros(out_size + [len(filter_size)])
	
	for d in xrange(depth):
		for i in range(0,matrix_size[0] - filter_size[0] + 1, stride[0]):
			for j in range(0, matrix_size[1] - filter_size[0] + 1, stride[1]):
				inp = inputPool[i:i+filter_size[0], j:j+filter_size[1], d]
				out[i,j,d] = inp.max()
				ind[i,j,d] = np.unravel_index(inp.argmax(), inp.shape)
	
	modelPool['output'].append(out)
	modelPool['indices'].append(ind)
	
	return modelPool		

def backwardPool(modelPool, inputPool, del_out):
	stride = modelPool['stride']
	filter_size = modelPool['window']
	matrix_size = inputPool.shape[0:2]
	depth = inputPool.shape[2]
	
	del_inp = np.zeros_like(inputPool)
	for d in xrange(depth):
		for i in range(0,matrix_size[0] - filter_size[0] + 1, stride[0]):
			for j in range(0, matrix_size[1] - filter_size[0] + 1, stride[1]):
				x, y = ind[i, j, d, 0], ind[i, j, d, 0]
				del_inp[i:i+filter_size[0], j:j+filter_size[1], d][x,y] += del_out[i,j,d]
	
	ret = {'del_inp' : del_inp}
	return ret

def updatePool(modelPool):
	return modelPool



		
		
		
	
	
	
	
	
	






















	
