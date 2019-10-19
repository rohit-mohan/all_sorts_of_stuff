import os.path
import warnings

class Run:
	def __init__(self, netObj, confObj, inObj, outObj = None):
		self.netObj = netObj
		self.confObj = confObj
		self.inObj = inObj
		self.outObj = outObj
	
	def getConfig(self, config_file):
		self.confObj.getConfig(config_file)
	
	
	def runConfig(self):
		
		#netObj = self.netObj
		#confObj = self.confObj
		#inObj = self.inObj
		#outObj = self.outObj
		
		
		for config in self.confObj.configs :
			
			self.confObj.displayConfig(config)
			
			behaviour = config['BEHAVIOUR']
			files = config['FILES']
			model = config['MODEL']
			train_opt = config['TRAINING_OPTIONS']
			
			self.inObj.setInputSource(files['TRAIN_DATA'], files['TEST_DATA'], files['NETWORK_INPUT'])
			self.outObj.setOutputDest(files['TRAIN_STATS'], files['NETWORK_OUTPUT'])
			
			
			if behaviour['NEW'] == '1':
				if not os.path.isfile(files['TRAIN_DATA']) :
					warnings.warn('Could not find training data. Skipping current configuration')
					continue
				
				self.netObj.trainNew(model, train_opt, self.inObj, self.outObj)
			
			elif behaviour['NEW'] == '0':
				if behaviour['LOAD/CONTINUE'] == '0':
					if not os.path.isfile(files['NETWORK_INPUT']) :
						warnings.warn('Could not find network input file. Skipping current configuration')
						continue
				
					if behaviour['TRAIN/TEST'] == '0':
						if not os.path.isfile(files['TRAIN_DATA']) :
							warnings.warn('Could not find training data. Skipping current configuration')
							continue
					
						self.netObj.loadAndTrain(train_opt, self.inObj, self.outObj)						

					elif behaviour['TRAIN/TEST'] == '1':
						if not os.path.isfile(files['TEST_DATA']) :
							warnings.warn('Could not find testing data. Skipping current configuration')
							continue
					
						self.netObj.loadAndTest(self.inObj, self.outObj)
				
					else :
						warnings.warn('Unknown configuration. TRAIN/TEST not 0 or 1. Skipping current configuration')
						continue
				
				elif behaviour['LOAD/CONTINUE'] == '1':				
					if behaviour['TRAIN/TEST'] == '0':
						if not os.path.isfile(files['TRAIN_DATA']) :
							warnings.warn('Could not find training data. Skipping current configuration')
							continue
					
						self.netObj.continueToTrain(train_opt, self.inObj, self.outObj)						

					elif behaviour['TRAIN/TEST'] == '1':
						if not os.path.isfile(files['TEST_DATA']) :
							warnings.warn('Could not find testing data. Skipping current configuration')
							continue
					
						self.netObj.continueToTest(self.inObj, self.outObj)
				
					else :
						warnings.warn('Unknown configuration. TRAIN/TEST not 0 or 1. Skipping current configuration')
						continue
				
				else :
					warnings.warn('Unknown configuration. LOAD/CONTINUE not 0 or 1. Skipping current configuration')
					continue
			
			else:
				warnings.warn('Unknown configuration. NETWORK not 0 or 1. Skipping current configuration')
			
				























				
