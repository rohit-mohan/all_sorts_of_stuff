import matplotlib.pyplot as plt
import numpy as np 
import cPickle as pkl

###########Global Variables###################

# Simulation parameters
del_t = 0.1
n = 8000

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
eta_list = [-0.20 + i * 0.002 for i in range(150)]

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



def bifurcation(eta, x0, v0):
	time_series = [xinit]
	
	x = x0 + 1e-5
	v = v0 + 1e-5
	
	# Generating time-series 
	for i in range(n-1):
		x, v = update(x, v, eta)
		time_series.append(x)
	
	time_series = np.array(time_series)
	#ret = np.mean( np.abs(time_series) )
	#ret = np.max(time_series[:100])
	ret = np.sqrt(np.mean(np.square(time_series)))
	
	return ret, x, v

	
##############Main###########################
forward = []
backward = []
rev_eta_list = eta_list[::-1]

x0 = xinit
v0 = vinit
for eta in eta_list:
	print eta
	am, x0, v0 = bifurcation(eta, x0, v0)
	forward.append(am)

for eta in rev_eta_list:
	print eta
	am, x0, v0 = bifurcation(eta, x0, v0)
	backward.append(am)

plt.plot(eta_list, forward, color='r', linewidth=4)
plt.plot(rev_eta_list, backward, color='g', linewidth=4)
plt.title('Bifurcation Diagram')
plt.xlabel('Parameter eta')
plt.ylabel('RMS value of time-series of state, x')
plt.show()


