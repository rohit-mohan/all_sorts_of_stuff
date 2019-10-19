f = open('trial_folders.txt', 'rb')

learning_rate = [0.001, 0.003, 0.005, 0.008,
                     0.01, 0.03, 0.05, 0.08,
                     0.1, 0.3, 0.5, 0.8]

batch_size = [30, 50, 100, 200, 500]
count = 0
for directory in f:
	for lr in learning_rate:
		for bs in batch_size:
			count = count + 1
			print '# Config Number : ',  count
			print '[TRAINING_OPTIONS]'
			print 'LEARNING_RATE = {}'.format(lr)
			print 'BATCH_SIZE = {}'.format(bs)
			print '[FILES]'
			print 'TRAIN_STATS = {}'.format(directory.strip() + '/l{}_b{}.pkl'.format(lr, bs))
			print 'END'
			print 

