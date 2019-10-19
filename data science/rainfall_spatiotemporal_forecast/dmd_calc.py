import numpy as np
import matplotlib as mpl
from matplotlib import cm, patches
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import dot, multiply, diag, power, pi, real, imag, log
from numpy.linalg import inv, eig, pinv
from scipy.linalg import svd, svdvals
from cPickle import load, dump

######################### User Input Code ##########################

import sys

if len(sys.argv) < 6:
	print "python dmd_calc.py <lim1> <lim2> <rank> <plotflag> <transposeflag>"
	sys.exit()

lim1 = int(sys.argv[1])
lim2 = int(sys.argv[2])
rank = int(sys.argv[3])
plotflag = int(sys.argv[4])
transposeflag = int(sys.argv[5])
####################################################################





# Get data from the pickle file and format it
pFile = open('data/india_rainfall.pickle')

#####################################################################
if (transposeflag):
	data = load(pFile).T
	xname = "time"
	yname = "station"
else:
	data = load(pFile)
	xname = "station"
	yname = "time"
#####################################################################

D = data[:, lim1:lim2]
#D = data[700:, [23, 19, 9]]

print 'Size of data : ', D.shape

x = np.array(range(0, D.shape[0]))
print 'number of' , xname, x.shape
y = np.array(range(0, D.shape[1]))
print 'number of ', yname, y.shape
Xm, Ym = np.meshgrid(x, y)
print "Mesh size : ", Xm.shape, Ym.shape
dt = 1


# Plot the spatio-temporal rainfall data 
fig1 = plt.figure()
ax = fig1.gca(projection='3d')
ax.plot_surface(Xm, Ym, D.T, cmap=cm.rainbow, rstride=1, cstride=1)
plt.title('spatio-temporal rain data')
plt.xlabel(xname)
plt.ylabel(yname)

# create DMD input-output matrices
X = D[:,:-1]
print 'Size of DMD input matrix : ', X.shape
Y = D[:,1:]
print 'Size of DMD output matrix : ', Y.shape

# Calculate the SVD of DMD input matrix X
U2,Sig2,Vh2 = svd(X, False)
print 'Size of SVD components : ', U2.shape, Sig2.shape, Vh2.shape


# Plot singular values of X
if (plotflag):
	fig2 = plt.figure()
	plt.scatter( range(len(Sig2)), Sig2)
	plt.title('singular values of X (from AX = Y)')


# low-rank truncation of X using SVD
r = rank
U = U2[:,:r]
Sig = diag(Sig2)[:r,:r]
V = Vh2.conj().T[:,:r]
print 'Size of reduced SVD components : ', U.shape, Sig.shape, V.shape

# equally distributed color map
color_idx = np.linspace(0, 1, r)

# Calulate lower dimensional matrix Atil resembling A and get its eigenvalues and eigenvectors 
Atil = dot(dot(dot(U.conj().T, Y), V), inv(Sig))
print 'Size of reduced dimension matrix similar to A (Atil) : ', Atil.shape
mu,W = eig(Atil)
print 'no. of eigenvalues for Atil : ', len(mu)


# Plot the eigenvalues of Atil in the complex plane with unit circle as the reference
if (plotflag):
	fig3 = plt.figure()
	circle1 = plt.Circle((0, 0), 1, color='r', fill=False)
	ax = fig3.gca()
	ax.add_patch(circle1)

	colors = [cm.rainbow(i) for i in color_idx]
	plt.scatter(mu.real, mu.imag, color=colors, s=50)

	plt.xlim(min(min(mu.real), -1.5), max(max(mu.real), 1.5))
	plt.ylim(min(min(mu.imag), -1.5), max(max(mu.imag), 1.5))

	plt.title('complex plane plot of eigenvalues of A')


# Calculate the eigenvectors of A from the eigenvectors of the low dimensional approximation Atil
Phi = dot(dot(dot(Y, V), pinv(Sig)), W)
print 'Size of eigenvector matrix of A (Phi) : ', Phi.shape


# Plot the dominant modes of A
if (plotflag):
	fig4 = plt.figure()
	plt.title('{} dominant modes'.format(r))
	for ind,clr in enumerate(color_idx):
		plt.plot(Phi[:,ind].real, color=cm.rainbow(clr))
	#	plt.scatter(range(len(Phi[:,0])), Phi[:,ind].imag, color=cm.rainbow(clr), alpha=0.3)


# compute time evolution
b = dot(pinv(Phi), X[:,0])
Psi = np.zeros([r, len(y)], dtype='complex')

for i,_t in enumerate(y):
    Psi[:,i] = multiply(power(mu, _t/dt), b)
print 'size of Psi : ', Psi[:, 0].shape


# Plot the time evolution of the dominant modes
if (1 or plotflag):
	fig5 = plt.figure()
	plt.title('evolution of {} dominant modes'.format(r))

	for ind,clr in enumerate(color_idx):
		plt.plot(Psi[ind, :].real,  color=cm.rainbow(clr))
	#	plt.scatter(range(len(Psi[0, :])), Psi[0, :].imag, color='r', alpha=0.3)


# DMD reconstruction
D2 = dot(Phi, Psi)

fig6 = plt.figure()
ax = fig6.gca(projection='3d')
ax.plot_surface(Xm, Ym, D2.real.T, cmap=cm.rainbow, rstride=1, cstride=1)
plt.title('reconstructed spatio-temporal rain data')
plt.xlabel(xname)
plt.ylabel(yname)

plt.show()

