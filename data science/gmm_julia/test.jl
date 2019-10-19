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

using PyPlot

for i=1:size(X,1)
	scatter(X[i, 1], X[i, 2], s=5, c=)
end


