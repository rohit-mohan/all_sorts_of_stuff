import cPickle as pkl

class Output:
	def __init__(self):
		self.stat_file = None
		self.network_out = None
		self.output = None
		#print "Output object created."
		
	
	def setOutputDest(self, stat_file, network_out):
		self.stat_file = stat_file
		self.network_out = network_out
	
		#print "Output destination set."
	
	
	def saveStats(self, output):
		self.output = output
		assert (self.stat_file != None and self.stat_file != ''), "No output file specified."
		with open(self.stat_file, 'wb') as f:
			pkl.dump(output, f)
	
		print "Training stats saved to {}.".format(self.stat_file)
	
	def saveNetwork(self, output): 
		assert (self.network_out != None and self.network_out != ''), "No output file specified."
		with open(self.network_out, 'wb') as f:
			pkl.dump(output, f)
			
		print "Network data saved to {}.".format(self.network_out)
	
		
