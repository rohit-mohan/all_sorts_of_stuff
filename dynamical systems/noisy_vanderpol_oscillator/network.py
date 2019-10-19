import random
import numpy as np
import cPickle as pkl

class Network(object):
	
	def __init__(self, sizes, biases=None, weights=None):
		self.sizes = sizes
		self.num_layers = len(sizes)
		if biases == None:
			self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
		else:
			self.biases = biases
		
		if weights == None:
			self.weights = [np.random.randn(y, x) for x,y in zip(sizes[:-1], sizes[1:])]
		else:
			self.weights = weights
		
		"""
		print "Number of layers : ", self.num_layers
		print "Shape of weights  :"
		for w in self.weights:
			print w.shape
		"""
		
	def feedforward(self, a):
		for b, w in zip(self.biases, self.weights):
			a = sigmoid(np.dot(w, a) + b)
			
		return a
	
	"""
	def SGD(self, training_data, epoches, minibatch_size, eta, testing_data=None):
		n = len(training_data)
		
		for j in xrange(epoches):
			random.shuffle(training_data)
			minibatches = [training_data[k:min(k+minibatch_size, n)] for k in xrange(0, n, minibatch_size)]
			
			count = 0
			for minibatch in minibatches:
				count = count + 1
				print "\tMinibatch number : ", count
				self.update_minibatch(minibatch, eta)
			
			print "Epoch {} complete".format(j+1)
	"""
	
	def SGD(self, training_data, epoches=1, minibatch_size=100, eta=1.0, testing_data=None, del_accuracy=0.5, eval_per_epoch=10):
		n = len(training_data)
		accuracies = [0.0]
		epoch = 0
		
		test_flag = (testing_data != None)
		
		if test_flag:
			print "Accuracy check enabled."
		
		while test_flag or (epoch < epoches):
			random.shuffle(training_data)
			minibatches = [training_data[k:min(k+minibatch_size, n)] for k in xrange(0, n, minibatch_size)]
			
			count = 0
			for minibatch in minibatches:
				count = count + 1
				print "\tMinibatch number : ", count
				self.update_minibatch(minibatch, eta)
			
			epoch = epoch + 1
			print "Epoch {} complete".format(epoch)
			
			if test_flag and (epoch % eval_per_epoch == 0):
				accuracy = float(self.evaluate(testing_data)) / len(testing_data) * 100
				print "Accuracy after {} epoches : {}".format(epoch, accuracy)
				accuracies.append(accuracy)
				if (accuracies[-1] - accuracies[-2]) < del_accuracy:
					break			
	
		print "Total epoches : ", epoch
		print "Accuracy list : "
		for a in accuracies[1:] :
			print a	


	
	def update_minibatch(self, minibatch, eta):
		nabla_b = [np.zeros(b.shape) for b in self.biases]
		nabla_w = [np.zeros(w.shape) for w in self.weights]
		
		for x, y in minibatch:
			del_nebla_b, del_nebla_w = self.backprop(x, y)
			nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, del_nebla_b)]
			nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, del_nebla_w)]
		
		self.biases = [b - (eta/len(minibatch))*nb for b, nb in zip(self.biases, nabla_b)]	
		self.weights = [w - (eta/len(minibatch))*nw for w, nw in zip(self.weights, nabla_w)]	
		
	def backprop(self, x, y):
		
		nabla_b = [np.zeros(b.shape) for b in self.biases]
		nabla_w = [np.zeros(w.shape) for w in self.weights]
		# feedforward
		activation = x
		activations = [activation] # list to store all the activations, layer by layer
		zs = [] # list to store all the z vectors, layer by layer
		for b, w in zip(self.biases, self.weights):
			#print "Backpropogation => a : ", activation.shape, " w : ", w.shape
			z = np.dot(w, activation)+b
			zs.append(z)
			activation = sigmoid(z)
			activations.append(activation)
		
		#print "backpropogation => activation size = ", activation.shape
		# backward pass
		#print "backprop => y : ", len(y), " activation : ", activations[-1].shape
		delta = self.cost_derivative(activations[-1], y) * \
			sigmoid_prime(zs[-1])
		nabla_b[-1] = delta
		nabla_w[-1] = np.dot(delta, activations[-2].transpose())

		for l in xrange(2, self.num_layers):
			z = zs[-l]
			sp = sigmoid_prime(z)
			delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
			nabla_b[-l] = delta
			nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
		return (nabla_b, nabla_w)	
        
	def evaluate(self, test_data):
		test_results = [(np.argmax(self.feedforward(x)), np.argmax(y)) for (x, y) in test_data]
		return sum(int(x == y) for (x, y) in test_results) 

	def cost_derivative(self, output_activations, y):
		return (output_activations-y)

	def save_network_as_pickle(self, filename):
		obj = (self.sizes, self.biases, self.weights)
		f = open(filename, 'wb')
		pkl.dump(obj, f)
		f.close()
		
#### Miscellaneous functions
def sigmoid(z):
	return 1.0/(1.0+np.exp(-z))

def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
    return sigmoid(z)*(1-sigmoid(z))	



"""
import mnist_loader
training_data, validation_data, test_data = mnist_loader.load_data_wrapper()

import network
net = network.Network([784, 30 ,10])
net.SGD(training_data, 30, 10, 3.0)

"""



			





