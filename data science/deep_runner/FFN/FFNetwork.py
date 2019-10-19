import tensorflow as tf
import numpy as np
import random
import os

class Network:
	"""
	This class deals with the actual machine learning algorithm.
	"""
	def __init__(self, displayCondition=True):
		self.displayCondition = displayCondition
		self.activation_dict = {'relu':tf.nn.relu, 'tanh':tf.tanh, 'sigmoid' : tf.sigmoid}
		self.arch = []						
		self.activation = None
		self.layers = []
		self.sess = tf.Session()
	
	def newModel(self, model):
		
		arch = model['ARCHITECTURE']
		activation = model['ACTIVATION']
		self.arch = arch
		self.activation = self.activation_dict[activation]
		self.layers = []
		for i, j in zip(arch[:-1], arch[1:]):	
			l = { 'weights' : tf.Variable(tf.random_normal([ i, j ], stddev= 0.0001, dtype=tf.float32),name = 'weight-{}'.format(j)), 
				'biases' : tf.Variable(tf.random_normal([1, j], dtype=tf.float32),name = 'bias-{}'.format(j)) }
			self.layers.append(l)		
		
		#print "New network created."

	
	def loadModel(self, model):
		arch = model['Architecture']
		activation = model['Activation']
		layers = model['Layers']
		self.arch = arch
		self.activation = self.activation_dict[activation]
		self.layers = []
		for j in xrange(len(self.arch)-1):
			l = { 'weights' : tf.cast(tf.Variable(layers[j]['weights'], name = 'weight-{}'.format(j)), tf.float32), 
				'biases' : tf.cast(tf.Variable(layers[j]['biases'], name = 'bias-{}'.format(j)), tf.float32) }
			self.layers.append(l)	
		
		#print "Network loaded."
	
	def continueModel(self):
		layers = []
		for j in xrange(len(self.arch) - 1):
			weights = self.sess.run(self.layers[j]['weights'])
			biases = self.sess.run(self.layers[j]['biases'])
			l = {'weights' : tf.Variable(weights, name = 'weight-{}'.format(j)),
				'biases': tf.Variable(biases, name = 'bias-{}'.format(j))}
			layers.append(l)
		
		self.layers = layers
	
	def forward(self, x, prob):		
		layer_output = [x]
		for l in self.layers : 
			layer_output.append( self.activation( tf.nn.dropout( tf.add( tf.matmul(layer_output[-1], l['weights']), l['biases'] ), prob) ) )
		
		return layer_output[-1]

	def train(
				self,
				trainOpt, 
				inObj,
				outObj
				):
		
		assert(self.layers != [] and self.arch != [] and self.activation != None), 'No network initialized.'
		
		#print "Starting training."
		
		num_epochs = trainOpt['EPOCHS']
		batch_size  = trainOpt['BATCH_SIZE']
		learning_rate  = trainOpt['LEARNING_RATE']
		keep_prob = trainOpt['KEEP_PROB']
		
		epochs_between_test = trainOpt['EPOCHS_BETWEEN_TEST']
		evaluate_test_set  = trainOpt['EVALUATE_TEST_SET']
		evaluate_train_set = trainOpt['EVALUATE_TRAIN_SET']
		evaluate_confusion_train = True
		evaluate_confusion_test = True
		save_stats = trainOpt['SAVE_STATS']
		save_network = trainOpt['SAVE_NETWORK']

		epoch_list = []
		cost_list = []
		
		if evaluate_test_set:
			test_accuracy_list = []
		
		if evaluate_train_set: 
			train_accuracy_list = []
		
		x = tf.placeholder('float32', [None, self.arch[0]], name='x')
		y = tf.placeholder('float32', [None, self.arch[-1]], name='y')
		p = tf.placeholder(tf.float32)
		
		prediction = self.forward(x, p)
		cost = tf.reduce_mean(tf.square(tf.subtract(prediction, y)))
		optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
		max_val_y = tf.argmax(y, 1)
		max_val_pred = tf.argmax(prediction, 1)	
		correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
		accuracy = tf.reduce_mean(tf.cast(correct, 'float')) * 100		
			
		sess = self.sess
		sess.run(tf.global_variables_initializer())
		
		
		for epoch in xrange(1, num_epochs+1):
			batches = self.getTrainingBatches(inObj, batch_size)
		
			for batch in batches:
				_, c = sess.run([optimizer, cost], feed_dict={x: batch['data'], y: batch['label'], p: keep_prob})
			

			if epoch % epochs_between_test == 0:
				epoch_list.append(epoch)
				cost_list.append(c)
				
				
				if evaluate_test_set :
					
					inObj.loadTestingData()
					data = self.formatInputData(inObj.data)
					test_acc = sess.run(accuracy, {x: data['data'], y: data['label'], p: 1.0}) 
					
					
					#test_acc = self.test(inObj)
					test_accuracy_list.append(test_acc)
				
				if evaluate_train_set:
					
					inObj.loadTrainingData()
					data = self.formatInputData(inObj.data)
					train_acc = sess.run(accuracy, {x: data['data'], y: data['label'], p: 1.0})
					
					
					#train_acc = self.test(inObj, use_train_data=True)
					train_accuracy_list.append(train_acc)
				
				
				if self.displayCondition :			       
					print 'Epoch', epoch, ' / ',num_epochs,' => cost: ', c, 
					
					if evaluate_train_set:
						print ' training accuracy: ', train_acc, #, train_acc_1 
					if evaluate_test_set:
						print ' testing accuracy: ', test_acc, #, test_acc_1
					
					print
		
		os.system("echo 'Cost : {}' >> result.txt".format(cost_list[-1]))
		
		output = {'epoch_list' : epoch_list,
				'cost_list' : cost_list, 
				'train_accuracy_list' : None,
				'test_accuracy_list' : None,
				'conf_mat_test' : None,
				'conf_mat_train' : None
				}
		
		if evaluate_train_set:
			output['train_accuracy_list'] = train_accuracy_list
			os.system("echo 'Train acc : {}' >> result.txt".format(train_accuracy_list[-1]))
		
		if evaluate_test_set :
			output['test_accuracy_list'] = test_accuracy_list
			os.system("echo 'Test acc : {}' >> result.txt".format(test_accuracy_list[-1]))
		
		if evaluate_confusion_train:
			inObj.loadTrainingData()
			data = self.formatInputData(inObj.data)
			y_max = sess.run(max_val_y, {y: data['label']})
			pred_max = sess.run(max_val_pred, {x: data['data'], y: data['label'], p: 1.0})
			
			num_train = self.arch[-1]
			conf_mat_train = np.zeros([num_train, num_train])
			for i, j in zip(y_max, pred_max):
				conf_mat_train[i, j] = conf_mat_train[i, j] + 1
			
			output['conf_mat_train'] = conf_mat_train
		
		if evaluate_confusion_test:
			inObj.loadTestingData()
			data = self.formatInputData(inObj.data)
			y_max = sess.run(max_val_y, {y: data['label']})
			pred_max = sess.run(max_val_pred, {x: data['data'], y: data['label'], p: 1.0})
			
			num_test = self.arch[-1]
			conf_mat_test = np.zeros([num_test, num_test])
			for i, j in zip(y_max, pred_max):
				conf_mat_test[i, j] = conf_mat_test[i, j] + 1
			
			output['conf_mat_test'] = conf_mat_test
		
		if save_stats :
			outObj.saveStats( self.formatOutputData(output) )
		if save_network :
			outObj.saveNetwork( self.formatOutputNetwork() )

	
	def test(self, inObj, use_train_data = False):
	
		#print "Starting test."
	
		if use_train_data:
			inObj.loadTrainingData()
		else :
			inObj.loadTestingData()
		
		data = self.formatInputData(inObj.data)
		
		sess = self.sess
		
		prediction = self.forward(x)	
		correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
		accuracy = tf.reduce_mean(tf.cast(correct, 'float')) * 100	
				
		acc = sess.run(accuracy, {x: data['data'], y: data['label'], p: 1.0})
		
		return acc


	
	def getTrainingBatches(self, inObj, batch_size):
		assert (batch_size > 0), "Batchsize should be a positive integer"
		
		inObj.loadTrainingData()
		training_data = self.formatInputData(inObj.data)
		num_samples = len(training_data['data'])
		
		
		combined = zip(training_data['data'], training_data['label'])
		random.shuffle(combined)
		data, label = zip(*combined)
		
		batches = [{'data': data[i : min(i+batch_size, num_samples)], 'label': label[i : min(i+batch_size, num_samples)]} for i in xrange(0, num_samples, batch_size)]
		
		return batches	

	
	def formatInputData(self, dataset):
		
		assert (type(dataset) == list and dataset != [] and ( type(dataset[0]) == list or type(dataset[0]) == tuple ) and len(dataset[0]) == 2), "Incompatible dataset"
		
		d = []
		l = []
		for ds in dataset :
			d.append(ds[0])
			l.append(ds[1])
		
		return {'data' : d,'label' : l}

	
	def formatInputNetwork(self, network):
		return network

	
	def formatOutputData(self, output):
		return output

	
	def formatOutputNetwork(self):
		l = []
		with tf.Session() as sess:
			sess.run(tf.initialize_all_variables())
			for layer in self.layers:
				w, b = sess.run([layer['weights'], layer['biases']])
				l.append({'weights' : w, 'biases' : b})
		
		act = [i for i in self.activation_dict if self.activation_dict[i] == self.activation][0]
		
		network = {'Architecture': self.arch, 'Activation': act, 'Layers': l}
		
		return network

	
	def trainNew(self, model, trainOpt, inObj, outObj):
		print "Training new model."
		self.newModel(model)
		self.train(trainOpt, inObj, outObj)
	
	def loadAndTrain(self, trainOpt, inObj, outObj):
		print "Loading a model and training."
		self.loadModel(inObj.getNetworkModel(self.formatInputNetwork))
		self.train(trainOpt, inObj, outObj)
		
	def continueToTrain(self, trainOpt, inObj, outObj):
		print "Continuing the training."
		self.continueModel()
		self.train(trainOpt, inObj, outObj)		
		
	def loadAndTest(self, inObj):
		print "Loading a model and testing."
		self.loadModel( self.formatInputNetwork( inObj.getNetworkModel() ) )
		return self.test(inObj)
		
	def continueToTest(self, inObj):
		print "Testing the current model."
		self.continueModel()
		return self.test(inObj)		



