import numpy as np
import random
from functools import reduce
import operator

class Network:


	def __init__(self):
		self.num_mixtures = 0
		self.data_dim = 0
		self.mean_list = None
		self.var_list = None
		self.weights = None
		
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
	
	def formatInputData(self, dataset):
		return dataset	
	
	
	def formatInputNetwork(self, network):
		return network

	
	def formatOutputData(self, output):
		return output

	
	def formatOutputNetwork(self):
		network = {'num_mixtures' : self.num_mixtures, 
			'data_dim' : self.data_dim, 
			'mean_list': self.mean_list,
			'variance_list' : self.var_list}
	
		return network
	
	def newModel(self, model):
		self.num_mixtures = model['NUMBER_MIXTURES']
		self.data_dim = model['DATA_DIMENSION']
		self.mean_list = np.random.random([self.num_mixtures, self.data_dim]) 
		self.var_list = np.zeros([self.num_mixtures, self.data_dim, self.data_dim])
		for i in range(self.num_mixtures): self.var_list[i, :, :] = np.eye(self.data_dim)
		self.weights = np.random.random([self.num_mixtures]) 
		self.weights /= np.sum(self.weights) 
	
	def loadModel(saved) :
		self.num_mixtures = saved['num_mixtures']
		self.data_dim = saved['data_dim']
		self.mean_list = saved['mean_list']
		self.var_list = saved['variance_list']
	
	def continueModel():
		return
	
	
	def train(self, trainOpt, inObj, outObj):
		num_iter = trainOpt['NUMBER_ITER']
		cutoff = trainOpt['CUTOFF']
		save_network = trainOpt['SAVE_NETWORK']

		inObj.loadTrainingData()
		data = self.formatInputData(inObj.data)
		T = data.shape[0]

		def e_step():
			likelihood = np.zeros([T,self.num_mixtures])
	
			for n in xrange(self.num_mixtures):
				denominator = (2 * np.pi)**(self.data_dim/2) * np.sqrt(np.linalg.det(self.var_list[n, :, :]))
				for i in xrange(T):
					var1 = (data[i] - self.mean_list[n, :])
					var2 = np.linalg.pinv(self.var_list[n, :, :])
					numerator = np.exp(-0.5 * np.dot( np.dot(var1, var2), var1.T))  + 1e-10
					likelihood[i, n] = numerator / denominator
		
			for i in xrange(T):
				likelihood[i, :] /= np.sum(likelihood[i, :])
	
			return likelihood
	

		def m_step(likelihood):
			nk = np.sum(likelihood, axis=0)
	
			self.weights = nk / np.sum(nk)
	
			self.mean_list = np.zeros_like(self.mean_list)
			for n in xrange(self.num_mixtures):
				for d in xrange(self.data_dim):
					self.mean_list[n, d] = np.sum(likelihood[:,n] * data[:,d])
				self.mean_list[n, :] *= 1/nk[n]
	
			self.var_list = np.zeros_like(self.var_list)
			for n in xrange(self.num_mixtures):
				diff_like = np.zeros_like(data)
				
				for d in xrange(self.data_dim):
					diff_like[:, d] = (data[:, d] - self.mean_list[n,d]) * likelihood[:,n]
				
				self.var_list[n, :, :] = np.dot((data - self.mean_list[n, :]).T, diff_like) / nk[n]


		def calc_cost(likelihood):
			cost = 0
			for n in xrange(self.num_mixtures):
				denominator = (2 * np.pi)**(self.data_dim/2) * np.sqrt(np.linalg.det(self.var_list[n, :, :]))		
				for i in xrange(T):
					var1 = (data[i] - self.mean_list[n, :])
					var2 = np.linalg.pinv(self.var_list[n, :, :])
					numerator = self.weights[n] * np.exp(-0.5 * np.dot( np.dot(var1, var2), var1.T))
					numerator = likelihood[i, n] * np.log(numerator)
					cost += numerator/denominator
	
			return cost


		prev_cost = 0
		for i in xrange(num_iter):
			print "Iteration : ", i,
			likelihood = e_step()
			m_step(likelihood)
			cost = calc_cost(likelihood)
			print " Cost : ", cost
			
			if abs(prev_cost - cost) <= cutoff:
				print "Cost converged."
				break
			else : prev_cost = cost

		if save_network : outObj.saveNetwork(self.formatOutputNetwork())
	  	
  
  
	def test(self, inObj):
		print "Test module not defined."
		return






















		
	
