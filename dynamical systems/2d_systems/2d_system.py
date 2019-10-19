#! /usr/bin/python
import matplotlib.pyplot as plt
import numpy as np

x_init_arr, y_init_arr = np.mgrid[-10:10, -10:10]

num_points = x_init_arr.size
#print "Total number of points : " + str(num_points)

x_init_list = x_init_arr.reshape([num_points]).tolist()
y_init_list = y_init_arr.reshape([num_points]).tolist()
#print max(x_init_list), min(x_init_list)

# matrix parameters
a11 = 4.0 
a12 = 1.0
a21 = 8.0
a22 = 2.0

# number of iterations to be done for finding f(x) for given initial conditions
num_iter = 40
del_t = 0.01

f_x_list = []
f_y_list = []

for i in range(num_points) :
#	print "Point number  : " + str(i)

	x = x_init_list[i]
	y = y_init_list[i]

	f_x_list.append(x)
	f_y_list.append(y)

	for j in range(num_iter) :
		xdot = a11 * x + a12 * y
		ydot = a21 * x + a22 * y 
		x = x + xdot * del_t
		y = y + ydot * del_t

		f_x_list.append(x)
		f_y_list.append(y)
		
plt.scatter(f_x_list, f_y_list, s = 0.4, alpha = 0.8)
plt.xlim(min(f_x_list), max(f_x_list))
plt.ylim(min(f_y_list), max(f_y_list))
plt.show()


