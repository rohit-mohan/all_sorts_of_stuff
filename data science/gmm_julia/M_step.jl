function M_step(W, X)
	Nk = sum(W);
	Anew = Nk/sum(sum(W));

	num_classes = size(W,2);
	num_data = size(X,1);
	data_dim = size(X,2);

	Unew = zeros(data_dim, num_classes);

	for i=1:num_classes
		for j=1:num_data
            Unew[:, i] = Unew[:, i] + W[j, i] * X[j,:]';
		end
        Unew[:,i] = Unew[:,i] / Nk[i];
	end

	Snew = zeros(data_dim, data_dim, num_classes);

	for i=1:num_classes
		for j=1:num_data
            Snew[:,:, i] = Snew[:,:,i] + W[j, i] * (X[j, :]' - Unew[:, i]) * (X[j, :]' - Unew[:, i])'; 
		end
        Snew[:,:,i] = Snew[:,:,i] / Nk[i];
	end	
    
    return  [Unew, Snew, Anew]
end
