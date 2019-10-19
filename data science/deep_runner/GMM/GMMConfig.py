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
									'TEST_DATA' : 'test.pkl', 
									'NETWORK_INPUT' : './net_in.pkl',
									'TRAIN_STATS' : './train_stats.pkl',
									'NETWORK_OUTPUT' : './net_out.pkl', 
									}, 
						
						'MODEL' : {'NUMBER_MIXTURES' : 2,
									'DATA_DIMENSION': 2}, 
						
						'TRAINING_OPTIONS' : {'CUTOFF' : 0.0001,
												'NUMBER_ITER' : 100,
												'SAVE_NETWORK' : True}
						}
		
		self.print_order = (
							('BEHAVIOUR', ('TRAIN/TEST', 'LOAD/CONTINUE', 'NEW')), 
							('FILES', ('TRAIN_DATA', 'TEST_DATA', 'NETWORK_INPUT', 'TRAIN_STATS', 'NETWORK_OUTPUT')),
							('MODEL', ('NUMBER_MIXTURES', 'DATA_DIMENSION')),
							('TRAINING_OPTIONS', ('CUTOFF', 'NUMBER_ITER', 'SAVE_NETWORK'))
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
	





