function E_step(X, U, S, A)
	data_dim = size(X,2);
	num_data = size(X,1);
	num_classes = size(U,2);
	Likelihood = zeros(num_data, num_classes);
	W = zeros(num_data, num_classes);
	
	for clas=1:num_classes
        den = (2*pi)^(1/data_dim) * sqrt(det(S[:,:,clas]));
		for data=1:num_data
            diff = (X[data,:]'- U[:,clas]);
            num = A[clas]*exp(-0.5.*diff'*pinv(S[:,:,clas])*diff);
            Likelihood[data,clas] = num/den; 
		end		
	end 
	
	for data=1:num_data
        Normalized_L[data, :] = Likelihood[data,:] / sum(Likelihood[data, :]); 
	end

	for i=1:num_data
        L = Normalized_L[i, :];
		maxval = max(L);
        W[i, :] = map(x->begin if x == 4 return 1 else return 0 end end, a);
	end
		
    return W;
end
