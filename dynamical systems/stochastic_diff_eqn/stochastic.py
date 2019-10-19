import matplotlib.pyplot as plt
import numpy as np 

#########Common values#######################
del_t = 0.01
epsilon = 1e-20
sigma = 2e-1
n = 10000
a0 = 2e-0
#######################Common Functions########################
def euler(f, a0, mu, del_t):
	return a0 + f(a0, mu) * del_t 


def custom_fn(a0, mu):
	return mu * a0 + a0**3 - a0**5 + sigma * np.random.normal(0, np.sqrt(del_t), 1)[0]

###############################################################
def individual_ts():
	time_series = [a0]
	mu = -0.1
	a_old = a0
	a_new = euler(custom_fn, a_old, mu, del_t)
	time_list = [del_t * i for i in range(n)]
	
	for i in range(1, n) :
		time_series.append(a_new)
		a_old = a_new
		a_new = euler(custom_fn, a_old, mu, del_t)
		print "", a_old

	plt.title("Time Series for mu- {}  with noise amplitude - {} (iter- {}, del_t- {})".format(mu, sigma, n, del_t))
	plt.xlabel("time (s)")
	plt.ylabel("value")
	plt.xlim(0, time_list[len(time_series) - 1])
	plt.ylim(-1.5, 1.5)
	plt.plot( [del_t * i for i in range(n)] ,time_series)
	plt.show()
##############################################################
def multimu_ts():
	time_series = [a0]

	mu_high = 0.0
	mu_low = -0.25
	mu_num = 100
	mu_del = (mu_high - mu_low) / mu_num
	mu_list = [mu_low + i*mu_del  for i in range(0, mu_num)]
	
	time_list = [del_t * i for i in range(2*mu_num*n + 1)]
	
	a_ts = a0
	
	for mu in mu_list:
		
		a_old = a_ts #+ 1e-40
				
		for i in range(n) :	
			a_new = euler(custom_fn, a_old, mu, del_t)
			time_series.append(a_new)						
			a_old = a_new	
		
		a_ts = a_new
		
		print "parameter : ", mu, "last value : ", a_ts

	"""	
	for mu in reversed(mu_list):
		
		a_old = a_ts #+ 1e-40
				
		for i in range(n) :	
			a_new = euler(custom_fn, a_old, mu, del_t)
			time_series.append(a_new)						
			a_old = a_new	
		
		a_ts = a_new
		
		print "parameter : ", mu, "last value : ", a_ts
	"""
	
	plt.title("Time Series for mu- {} to {} with noise amplitude - {} (iter- {}, del_t- {})".format(mu_low, mu_high, sigma, n, del_t))
	plt.xlabel("time (s)")
	plt.ylabel("value")
	plt.xlim(0, time_list[len(time_series) - 1])
	plt.ylim(-1.5, 1.5)
	plt.plot(time_list[:len(time_series)], time_series)
	plt.show()
	
	
##############################################################
def hysterisis():

	mu_high = 0.4
	mu_low = -0.4
	mu_num = 30
	mu_del = (mu_high - mu_low) / mu_num
	mu_list = [mu_low + i*mu_del  for i in range(0, mu_num)]
	
	a_hyst = a0
	
	
	bg_color = 'black'
	fg_color = 'white'

	fig = plt.figure(facecolor=bg_color, edgecolor=fg_color)
	axes = plt.axes(axisbg=bg_color)
	axes.xaxis.set_tick_params(color=fg_color, labelcolor=fg_color)
	axes.yaxis.set_tick_params(color=fg_color, labelcolor=fg_color)
	for spine in axes.spines.values():
		spine.set_color(fg_color)
	
	for mu in mu_list:

		a_old = a_hyst #+ 1e-40
				
		for i in range(1, n) :
	
			a_new = euler(custom_fn, a_old, mu, del_t)
			a_old = a_new
			
		print "Initial value : ", a_hyst, " parameter value : ", mu, " final value : ", a_new		
		
		plt.scatter(mu, a_new, color = 'yellow', alpha=0.5)
		
		a_hyst = a_new
	
	print "##############reverse################"	
	
	for mu in reversed(mu_list) :

		a_old = a_hyst 
				
		for i in range(1, n) :

			a_new = euler(custom_fn, a_old, mu, del_t)
			a_old = a_new
			
		print "Initial value : ", a_hyst, " parameter value : ", mu, " final value : ", a_new		
		
		plt.scatter(mu, a_new, color = 'red', alpha=0.5)
		
		a_hyst = a_new		
	
	
	plt.title("Hysterisis Plot iter- {}, del_t- {}".format(n, del_t), color=fg_color)
	plt.xlabel("parameter", color=fg_color)
	plt.ylabel("peaks", color=fg_color)
	plt.xlim(mu_low, mu_high)
	plt.show()
	
option = input('Option : ')
if option == 1:
	individual_ts()
elif option == 2:
	multimu_ts()	
else:
	hysterisis()
	
