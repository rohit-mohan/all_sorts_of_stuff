import numpy as np
import random

class Network:
	def __init__(self):
		self.num_clusters = 0
		self.data_dim = 0
		self.mean_list = None
		
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
	
		def extract_mean_var(time_series):
			time_series = np.abs(time_series)
			m = np.mean(time_series)
			v = np.var(time_series)
	
			return np.array((m, v))
		
		data = []
		for d in dataset :
			sample = extract_mean_var(d[0])
			real_label = np.argmax(d[1])
			data.append({'sample' : sample, 'real_label' : real_label, 'pred_label' : 0})

		return data	
	
	
	def formatInputNetwork(self, network):
		return network

	
	def formatOutputData(self, output):
		return output

	
	def formatOutputNetwork(self):
		network = {'num_clusters' : self.num_clusters, 'data_dim' : self.data_dim, 'mean_list': self.mean_list}
		return network
	
	def newModel(self, model):
		self.num_clusters = model['NUMBER_CLUSTERS']
		self.data_dim = model['DATA_DIMENSION']
		self.mean_list = np.zeros([self.num_clusters, self.data_dim])
	
	def loadModel(saved) :
		self.num_clusters = saved['num_clusters']
		self.data_dim = saved['data_dim']
		self.mean_list = saved['mean_list']
	
	def continueModel():
		return
	
	
	def train(self, trainOpt, inObj, outObj):
		
		def init_means(data):
			random.shuffle(data)
			index = 0
			for d in data:
				sample = d['sample']
				label = d['real_label']
				
				if index == self.num_clusters:
					break
				if label == index:
					self.mean_list[index, :] = sample
					index += 1
		
		def obj_func(data):
			cluster_sum = np.zeros([self.num_clusters,])
	
			for d in data:
				sample = d['sample']
				label = d['pred_label']
				cluster_sum[label] += np.linalg.norm(sample - self.mean_list[label])**2

			return np.sum(cluster_sum)
		
		
		def update_cluster(data):
			for i in xrange(len(data)):
				sample = data[i]['sample']
				data[i]['pred_label'] =  np.argmin(np.sum( (sample - self.mean_list) ** 2, 1))
		
		
		def update_mean(data):
			new_mean_list = np.zeros_like(self.mean_list)
			num_members = [0] * self.num_clusters
	
			for d in data:
				s = d['sample']
				l = d['pred_label']
				num_members[l] += 1
				new_mean_list[l] += s
	
			for i in xrange(self.num_clusters):
				new_mean_list[i] = new_mean_list[i] / float(num_members[i])

			return new_mean_list
		
		
		num_iter = trainOpt['NUMBER_ITER']
		cutoff = trainOpt['CUTOFF']
		evaluate_train = trainOpt['EVALUATE_TEST_SET']
		evaluate_test = trainOpt['EVALUATE_TRAIN_SET']
		evaluate_conf_mat_train = True
		evaluate_conf_mat_test = True
		save_stats = trainOpt['SAVE_STATS']
		save_network = trainOpt['SAVE_NETWORK']
		
		
		inObj.loadTrainingData()
		train_data = self.formatInputData(inObj.data)
		
		output = {'epoch_list': [],
				 'cost_list': [], 
				 'train_accuracy_list': [], 
				 'test_accuracy_list' : [], 
				 'conf_mat_test' : None, 
				 'conf_mat_train' : None}
		
		init_means(train_data)
		
		for j in xrange(num_iter):
			update_cluster(train_data) 
			new_mean_list = update_mean(train_data)
			
			cost = obj_func(train_data)
			output['epoch_list'].append(j+1)
			output['cost_list'].append(cost)
			print "Iter : ", j+1," Cost : ", cost,
			
			if evaluate_train:
				acc = self.test(inObj, use_train_data = True)
				output['train_accuracy_list'].append(acc)
				print " Training Accuracy : ", acc,
			
			if evaluate_test:
				acc = self.test(inObj)
				output['test_accuracy_list'].append(acc)
				print " Testing Accuracy : ", acc,
			
			print ""
			
			if (np.linalg.norm(new_mean_list - self.mean_list) < cutoff):
				print "\tConverged below ", cutoff
				break
			
			self.mean_list = new_mean_list
		
		if evaluate_conf_mat_train : 
			output['conf_mat_train'] = self.test(inObj, use_train_data = True, calc_conf_mat = True)
		
		if evaluate_conf_mat_test : 	
			output['conf_mat_test'] = self.test(inObj, calc_conf_mat = True)
			
		if save_stats :
			outObj.saveStats(self.formatOutputData(output))
		
		if save_network :
			outObj.saveNetwork(self.formatOutputNetwork())
	
		
	def test(self, inObj, use_train_data = False, calc_conf_mat=False):
	
		if use_train_data:
			inObj.loadTrainingData()
		else :
			inObj.loadTestingData()
		
		data = self.formatInputData(inObj.data)
		total_data = len(data)
		correct = 0
		conf_mat = np.zeros([self.num_clusters, self.num_clusters])
		
		for d in data:
			pred = np.argmin(np.sum( (d['sample'] - self.mean_list) ** 2, 1))
			conf_mat[d['real_label']][pred] += 1
			if pred == d['real_label'] : correct += 1
		
		if calc_conf_mat : return conf_mat
		else : return float(correct)/total_data * 100






















		
	
