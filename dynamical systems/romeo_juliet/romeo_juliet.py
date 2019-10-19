#! /usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
import random as rnd

def trace_function(x_init_list, y_init_list, num_iter, del_t, A):
	f_x_list = []
	f_y_list = []

	for i in range(len(x_init_list)) :
	#	print "Point number  : " + str(i)

		x = x_init_list[i]
		y = y_init_list[i]

		f_x_list.append(x)
		f_y_list.append(y)

		for j in range(num_iter) :
			xdot = A[0] * x + A[1] * y
			ydot = A[2] * x + A[3] * y 
			x = x + xdot * del_t
			y = y + ydot * del_t

			f_x_list.append(x)
			f_y_list.append(y)
	

	return f_x_list, f_y_list


# MAIN routine

x_init_arr, y_init_arr = np.mgrid[-10:10, -10:10]
num_points = x_init_arr.size

x_init_list = x_init_arr.reshape([num_points]).tolist()
y_init_list = y_init_arr.reshape([num_points]).tolist()

# number of iterations to be done for finding f(x) for given initial conditions
num_iter = 20
del_t = 0.005

# parameters A and B (for the case where A > B)
A = float(rnd.randint(1, 10))
B = float(rnd.randint(1, 10))
if A < B :
	A, B = B, A

# matrix parameters
m11 = 0.0 
m12 = 0.0
m21 = A
m22 = B
Mat = [m11, m12, m21, m22]

# Get the function's x, y values
f_x_list, f_y_list = trace_function(x_init_list, y_init_list, num_iter, del_t, Mat)

# Plot them
fig = plt.figure(1)
plt.title("A : " + str(A) + " B : " + str(B))
plt.scatter(f_x_list, f_y_list, s = 0.4, alpha = 0.6)
plt.xlim(min(f_x_list), max(f_x_list))
plt.ylim(min(f_y_list), max(f_y_list))


# parameters A and B (for the case where A < B)
A = float(rnd.randint(1, 10))
B = float(rnd.randint(1, 10))
if A > B :
	A, B = B, A

# matrix parameters remain the same

# Get the function's x, y values
f_x_list, f_y_list = trace_function(x_init_list, y_init_list, num_iter, del_t, Mat)

# Plot them
fig = plt.figure(2)
plt.title("A : " + str(A) + " B : " + str(B))
plt.scatter(f_x_list, f_y_list, s = 0.4, alpha = 0.6)
plt.xlim(min(f_x_list), max(f_x_list))
plt.ylim(min(f_y_list), max(f_y_list))

plt.show()


