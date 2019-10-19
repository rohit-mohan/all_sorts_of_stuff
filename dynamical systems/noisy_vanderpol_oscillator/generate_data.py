import matplotlib.pyplot as plt
import numpy as np 

###########Global Variables###################
del_t = 0.01
#D = 0.05
#n = 1000

beta = 0
#xinit = 0.4
#vinit = 0.4
############Common Functions##################
def acceleration(x0, v0, eta):
	return (eta + x0**2 - x0**4) * v0 - x0 - beta * x0**3

def v_update(x0, v0, eta, D):
	
	k1 = acceleration(x0, v0, eta) * del_t
	k2 = acceleration(x0 + del_t * (v0 + k1/2), v0 + k1/2, eta) * del_t
	k3 = acceleration(x0 + del_t * (v0 + k2/2), v0 + k2/2, eta) * del_t
	k4 = acceleration(x0 + del_t * (v0 + k3), v0 + k3, eta) * del_t
	
	return v0 + k2 + D * np.random.normal(0, np.sqrt(del_t), 1)[0]
	
def x_update(x0, v0):
	return x0 + del_t * v0

##############################################

def var_eta_ts(eta_low, eta_high, eta_num, iter_per_eta, xinit, vinit, D):

	del_eta = (eta_high - eta_low) / eta_num
	eta_list = [eta_low + i * del_eta for i in range(eta_num)]
	

	time_series = [xinit]
	time = [0.0]

	x = xinit
	v = vinit
	t = 0
	
	for eta in eta_list:
		for i in range(iter_per_eta):
			t = t + del_t
			v = v_update(x, v, eta, D)
			x = x_update(x, v)
			time_series.append(x)
			time.append(t)
	
	
	return time_series, time
	
###################################################


eta_high = 0.25
eta_low = -0.25
eta_num = 10
iter_per_eta = 10000
xinit = 0.4
vinit = 0.4
D = 0.1

del_eta = (eta_high - eta_low) / eta_num
bist_low = int(-(eta_low + 0.125) / del_eta) * iter_per_eta
bist_high = int(-eta_low / del_eta) * iter_per_eta

plt.title("Time Series for eta- {} to {} , init- ({}, {}), noise- {}, para- (beta- {},iter- {}, del_t- {})".format(eta_low, eta_high, xinit, vinit, D, beta, iter_per_eta, del_t))
plt.xlabel("time (s)")
plt.ylabel("value")

for i in range(100):

	print "run : ", i
	time_series, time = var_eta_ts(eta_low, eta_high, eta_num, iter_per_eta, xinit, vinit, D)

	fig = plt.figure()
	plt.xlim(0, time[len(time_series) - 1])
	plt.ylim(min(time_series) - 1, max(time_series) + 1)
	plt.plot(time[0:bist_low - 1] ,time_series[0:bist_low - 1], 'b')
	plt.plot(time[bist_low:bist_high] ,time_series[bist_low:bist_high], 'r')
	plt.plot(time[bist_high:] ,time_series[bist_high:], 'b')
	fig.tight_layout()
	plt.savefig("plots/{}.png".format(i), dpi=600)
	
	
	
	
	
	
	
