function E_step(X, U, S, A)
	data_dim = size(X,2);
	num_data = size(X,1);
	num_classes = size(U,2);
	Likelihood = zeros(num_data, num_classes);
	Normalized_L = zeros(num_data, num_classes);
	W = zeros(num_data, num_classes);
	
	for clas=1:num_classes
        den = (2*pi)^(1/data_dim) * sqrt(det(S[:,:,clas]))

		for data=1:num_data
            diff = (X[data,:]'- U[:,clas]);
            num = A[clas]*exp(-0.5.*diff'*pinv(S[:,:,clas])*diff);

	        Likelihood[data,clas] = num[1] / den; 
		end		
	end 
	
	for data=1:num_data
        Normalized_L[data, :] = Likelihood[data,:] / sum(Likelihood[data, :]); 
	end

	for i=1:num_data
        L = Normalized_L[i, :];
		maxval = maximum(L);
        W[i, :] = map(x->begin if x == maxval return 1.0 else return 0.0 end end, L);
	end
		
    return W;
end


function M_step(W, X)
	Nk = sum(W,1);
	Anew = Nk/sum(W);

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
    
    return  Unew, Snew, Anew
end




C1 = [1 2];
C2 = [10 2];
C3 = [10 4];

R1 = 1*rand(1, 100);
R2 = 1*rand(1, 100);
R3 = 1*rand(1, 100);

T1 = 2*pi*rand(1,100);
T2 = 2*pi*rand(1,100);
T3 = 2*pi*rand(1,100);

Y1 = C1[2]+R1.*sin(T1);
Y2 = C2[2]+R2.*sin(T2);
Y3 = C3[2]+R3.*sin(T3);

X1 = C1[1]+R1.*cos(T1);
X2 = C2[1]+R2.*cos(T2);
X3 = C3[1]+R3.*cos(T3);

X=[X1' Y1'; X2' Y2'; X3' Y3'];
num_data = size(X,1);
data_dim = size(X,2);

A = [0.3, 0.7];
U = [2 3; 10 2]';

num_classes = size(U,2);
S = zeros(data_dim,data_dim,num_classes);
S[:,:,1] = [1 0; 0 1];
S[:,:,2] = [1 0; 0 1];

W = Array{Float64, 2}


LLold = 0.0;
for clas=1:num_classes
	den = (2*pi)^(1/data_dim) * sqrt(det(S[:,:,clas]))
	for data=1:num_data
    	diff = (X[data,:]'- U[:,clas]);
        num = W[data,class] * log(A[clas]*exp(-0.5.*diff'*pinv(S[:,:,clas])*diff));
	    LLold[data,clas] = num[1] / den; 
	end		
end

LLnew = 1.0;

while (abs(LLold - LLnew)) > 0.0001
	W = E_step(X, U, S, A);
	(Unew, Snew, Anew) = M_step(W, X);
	S = Snew;
	U = Unew;
	A = Anew;

	println((Snew, Unew, Anew));
	
	LLnew = 0;
	for clas=1:num_classes
        den = (2*pi)^(1/data_dim) * sqrt(det(S[:,:,clas]))
		for data=1:num_data
            diff = (X[data,:]'- U[:,clas]);
            num = W[data,class] * log(A[clas]*exp(-0.5.*diff'*pinv(S[:,:,clas])*diff));
	        LLnew[data,clas] = num[1] / den; 
		end		
	end  
end


using PyPlot
for i=1:num_data
	if (W[i, 1] > W[i, 2])
		plot(X[i, 1], X[i, 2], "b");
	else
		plot(X[i, 1], X[i, 2], "g");	
end
end
