import cPickle as pkl
import os.path

class Input:
	
	def __init__(self):
	
		
	
		self.test_file = None
		self.train_file = None
		self.network_in = None
		
		self.train = None
		self.test = None
		
		self.load_train = False
		self.load_test = False	
	
		self.data = self.train
		
		#print "Input object created."
		
		
	
	def setInputSource(self, train_file = None, test_file = None, network_in = None):
		
		if test_file == self.test_file :
			self.load_test = False
		else:
			self.test_file = test_file
			self.load_test =True

		if train_file == self.train_file :
			self.load_train = False
		else:
			self.train_file = train_file
			self.load_train =True
		
		self.network_in = network_in
		
		#print "Input source set."
	
	def loadTrainingData(self):
		assert (self.train_file != None), "Training data not specified."
	
		if self.load_train:
			self.load_train = False
			print "Loading training data."
			data = self.getDataFromFile(self.train_file)
			self.train =  data
			
		self.data = self.train

		


	def loadTestingData(self):
		assert (self.test_file != None), "Testing data not specified."
		
		if self.load_test:
			self.load_test = False
			print "Loading testing data."
			data = self.getDataFromFile(self.test_file)
			self.test =  data
		
		self.data = self.test
		
		
	
	def getNetworkModel(self, f):
		assert (self.network_in != None), "Network model not specified."
		
		print "Retreiving network data."
		
		return self.getDataFromFile(self.network_in)
	

	
	@staticmethod
	def getDataFromFile(filename):
		assert (os.path.isfile(filename)), "Could not find file to be opened."
		data = []
		with open(filename, 'rb') as f:
			data = pkl.load(f)
		return data
	




