import warnings
from copy import deepcopy

class Config:
	def __init__(
				self,
				display_condition=True,
				):
		
		self.display_condition = display_condition 		
		self.default_param = {
						'BEHAVIOUR' : {'TRAIN/TEST' : '0',
										'LOAD/CONTINUE' : '0', 
										'NEW' : '1'},
						
						'FILES' : {'TRAIN_DATA' : './train.pkl', 
									'TEST_DATA' : './test.pkl', 
									'NETWORK_INPUT' : './net_in.pkl', 
									'NETWORK_OUTPUT' : './net_out.pkl', 
									'TRAIN_STATS' : './output.pkl'}, 
						
						'MODEL' : {'ARCHITECTURE' : [100, 10],
									'ACTIVATION' : 'sigmoid'}, 
						
						'TRAINING_OPTIONS' : {'LEARNING_RATE' : 0.01,
												'EPOCHS' : 100,
												'BATCH_SIZE' : 50,
												'KEEP_PROB' : 1.0,
												'EPOCHS_BETWEEN_TEST' : 1,
												'EVALUATE_TEST_SET' : True,
												'EVALUATE_TRAIN_SET' : True,
												'SAVE_STATS' : True,
												'SAVE_NETWORK' : True}
						}
		
		self.print_order = (
							('BEHAVIOUR', ('TRAIN/TEST', 'LOAD/CONTINUE', 'NEW')), 
							('FILES', ('TRAIN_DATA', 'TEST_DATA', 'NETWORK_INPUT', 'NETWORK_OUTPUT', 'TRAIN_STATS')),
							('MODEL', ('ARCHITECTURE', 'ACTIVATION')),
							('TRAINING_OPTIONS', ('LEARNING_RATE', 'EPOCHS', 'BATCH_SIZE', 'KEEP_PROB', 'EPOCHS_BETWEEN_TEST', 'EVALUATE_TEST_SET', 'EVALUATE_TRAIN_SET'))
						)
		self.configs = []
		
		#print "Config object created."
		
	@staticmethod
	def sepKeyVal(s):
		
		lst = s.split('=')
		key = lst[0].strip()
		value = lst[1].strip()
			
		return key, value

	
	def setType(self, section, key, valstr):
		ty = type(self.default_param[section][key])
		
		if ty == bool:
			return True if valstr=='True' else False
		
		elif ty == list or ty == tuple:
			
			ty2 = type(self.default_param[section][key][0])
			value = [ty2(num) for num in valstr.strip('{}[]()').split(',')]
			return value	
		
		else:
			return ty(valstr)
		
	
	def getConfig(self, config_file):
		self.configs = []
		temp_config = deepcopy(self.default_param)
		
		with open(config_file, 'rb') as f:
			cur_section = None
			
			for line in f:
				line = line.strip()
				
				if line== '' or line[0] == '#' :
					continue
				
				elif line[0] == '[':
					section_temp = line.strip().strip('[]')
					assert (section_temp in self.default_param), "Unknown section header : {}.".format(section_temp)
					cur_section = section_temp
				
				elif line == 'END':
					new_entry = deepcopy(temp_config)
					self.configs.append(new_entry)
					cur_section = None
								
				else:
					assert (cur_section != None), 'Section header missing.'
					
					keyVal = self.sepKeyVal(line)
					assert keyVal[0] in self.default_param[cur_section], "Unknown keyword or parameter : {}.".format(keyVal[0])
					
					value = self.setType(cur_section, keyVal[0], keyVal[1])
					temp_config[cur_section][keyVal[0]] = value
		
		#print "Configurations retreived from config file."
	
	
	
	def displayConfig(self, config):
		if self.display_condition :
			print "\nStart Config\n"
			
			for elem in self.print_order:
				section = elem[0]
				print '[ ' , section, ' ]'
				for param in elem[1]:
					if param in config[section] :
						print '\t{:30}=\t\t{}'.format(param, config[section][param])
			
			print "\nEnd Config\n"
				
	def displayAllConfigs(self):
		for config_temp in self.configs:
			self.displayConfig(config_temp)
	





