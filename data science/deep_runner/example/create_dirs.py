import sys
from os import mkdir
from os.path import exists

base_dir = './' + sys.argv[1]

print "Creating following folders : "

if not exists(base_dir):
	print base_dir
	mkdir(base_dir)

b_list = ['beta_0', 'beta_0.1']
d_list = ['D_0.001','D_0.002']
e_list = ['epsilon_set_1', 'epsilon_set_2', 'epsilon_set_3']

for b in b_list:
	b_folder = base_dir + '/' + b
	if not exists(b_folder):
		print b_folder
		mkdir(b_folder)
	
	b_trial = base_dir + '/' + 'trial'
	if not exists(b_trial):
		print b_trial
		mkdir(b_trial)
	
	for d in d_list :
		d_folder = b_folder + '/' + d	
		if not exists(d_folder):
			print d_folder
			mkdir(d_folder)
		
		d_trial = b_folder + '/' + 'trial'
		if not exists(d_trial):
			print d_trial
			mkdir(d_trial)
		
		
		for e in e_list:
			e_folder = d_folder + '/' + e
			if not exists(e_folder):
				print e_folder
				mkdir(e_folder)
			
			e_trial = d_folder + '/' + 'trial'
			if not exists(e_trial):
				print e_trial
				mkdir(e_trial)
			
			if not exists(e_folder + '/' + 'trial'):
				print e_folder + '/' + 'trial'
				mkdir(e_folder + '/' + 'trial')
			
