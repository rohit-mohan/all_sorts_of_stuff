import matplotlib.pyplot as plt
import numpy as np 
import cPickle as pkl

###########Global Variables###################
del_t = 0.01
D0 = 0.1
n = 100000

beta = 0
xinit = 0.2
vinit = 0.2
############Common Functions##################
def acceleration(x0, v0, eta):
	return (eta + x0**2 - x0**4) * v0 - x0 - beta * x0**3

def v_update(x0, v0, eta, D=D0):
	
	k1 = acceleration(x0, v0, eta) * del_t
	v1 = v0 + k1
	k2 = acceleration(x0 + del_t * v1, v1, eta) * del_t
	#k3 = acceleration(x0 + del_t * (v0 + k2/2), v0 + k2/2, eta) * del_t
	#k4 = acceleration(x0 + del_t * (v0 + k3), v0 + k3, eta) * del_t
	
	return v0 + (k1+k2)/2 + D * np.random.normal(0, np.sqrt(del_t), 1)[0]
	
def x_update(x0, v0):
	return x0 + del_t * v0

##############################################
def single_eta_ts(snum = 0):
	eta = 0.2		 
	time_list = [del_t * i for i in range(n)]
	time_series = [xinit]
	
	x = xinit
	v = vinit
	 
	for i in range(n-1):
		v = v_update(x, v, eta)	
		x = x_update(x, v)
	
		#print x	
		time_series.append(x)

	pickleFile = open("{}.pkl".format(snum), 'wb')
	pkl.dump(time_series, pickleFile)
	pickleFile.close()

	fig = plt.figure()
	plt.title("Time Series for init- ({}, {}), beta- {}, iter- {}, del_t- {}".format(xinit, vinit, beta, n, del_t))
	plt.xlabel("time (s)")
	plt.ylabel("value")
	plt.xlim(0, time_list[len(time_series) - 1])
	plt.ylim(min(time_series) - 1, max(time_series) + 1)
	plt.plot(time_list[:len(time_series)] ,time_series, linewidth=0.25)
	fig.tight_layout()
	plt.savefig("{}.png".format(snum), dpi=1200)
	plt.close(fig)

data_num = 1
for i in range(data_num):
	print "run number : ", i+1
	single_eta_ts(i+1)
