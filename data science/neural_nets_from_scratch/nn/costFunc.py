def rmsError(pred, target, derivative = False) :
	if derivative : return (pred - target)
	else : return 0.5 * np.norm( target - pred )**2 
