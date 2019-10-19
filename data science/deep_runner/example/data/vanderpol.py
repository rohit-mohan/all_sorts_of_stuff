import matplotlib.pyplot as plt
import numpy as np 
import cPickle as pkl

###########Global Variables###################

# Simulation parameters
del_t = 0.1
n = 10000

# Model parameters
eta0 = -0.075
beta = 0
D = 0.0

# Initial conditions
xinit = 0.2
vinit = 0.2

# dataset parameters
num_low = 0
num_high = data_per_class = 1
eta_list = [-0.23, -0.135, 0.23]
				
"""
for D=0.001 => [-0.5, -0.13, 0.5], [-0.25, -0.125, 0.25], [-0.20, -0.135, 0.20]
for D=0.002 => [-0.5, -0.13, 0.5], [-0.25, -0.125, 0.25], [-0.23, -0.135, 0.23]
"""

#options
plot_mean_var = 0
plot_ts = 0
save_file = 1
############Common Functions##################
def acceleration(x, v, eta=eta0):
	"""
	Function to compute acceleration
	"""
	return ((eta + x**2 - x**4) * v) - x - (beta * x**3)

def update(x0, v0, eta=eta0):
	"""
	Fourth Order Runge-Kutta for Second Order ODE (with noise added during velocity updation)
	"""
	
	k1 = acceleration(x0, v0, eta)
	
	v1 = v0 + k1 * del_t/2
	x1 = x0 + v0 * del_t/2
	
	k2 = acceleration(x1, v1, eta)
	
	v2 = v0 + k2 * del_t/2
	x2 = x0 + v1 * del_t/2
	
	k3 = acceleration(x2, v2, eta)
	
	v3 = v0 + k3 * del_t
	x3 = x0 + v2 * del_t
	
	k4 = acceleration(x3, v3, eta)
	
	v_new = v0 + del_t * (k1 + 2*k2 + 2*k3 + k4) / 6 + (np.sqrt(2*D) * np.sqrt(del_t) * np.random.normal(0, 1, 1)[0])
	x_new = x0 + del_t * (v0 + 2*v1 + 2*v2 + v3) / 6
	
	return (x_new, v_new)





def get_label(eta=eta0):
	"""
	Label to identify to which class the time-series belongs to
	"""
	
	if eta == eta_list[0]:
		return (0, 0, 1)
	elif eta == eta_list[1]:
		return (0, 1, 0)
	else:
		return (1, 0, 0)




def single_eta_ts(snum = 0, eta=eta0):
	
	label = get_label(eta)
	print label
			 
	time_list = [del_t * i for i in range(n)]
	time_series = [xinit]
	
	x = xinit
	v = vinit
	
	# Generating time-series 
	for i in range(n-1):
		x, v = update(x, v, eta)
		time_series.append(x)
	
	if plot_mean_var :
		# Mean and variance plot
		abs_ts = np.abs(time_series)
		plt.scatter(np.mean(abs_ts), np.var(abs_ts), color=label)


	if save_file : 	
		# Save file

		pickleFile = open("{}.pkl".format(snum), 'wb')
		pkl.dump((time_series, label), pickleFile)
		pickleFile.close()

	
	if plot_ts : 
		# Plot and save figure
		fig = plt.figure()
		plt.title("Time Series for init- ({}, {}), noise - {}, eta - {}".format(xinit, vinit, D, eta))
		plt.xlabel("time (s)")
		plt.ylabel("value")
		plt.xlim(0, time_list[len(time_series) - 1])
		plt.ylim(-4, 4)
		plt.plot(time_list[:len(time_series)] ,time_series, linewidth=0.25)
		fig.tight_layout()
		plt.savefig("{}.png".format(snum), dpi=600)
		#plt.show()
		plt.close(fig)

	
##############Main###########################

for eta in eta_list:
	for i in range(num_low, num_high):
		print "run number : ", i+1
		single_eta_ts(i+1, eta)
		
	num_low = num_high
	num_high = num_high + data_per_class

if plot_mean_var :
	plt.show()



