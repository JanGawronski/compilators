A = eye(3);
B = ones(3);
C = A .+ B;
print C;

D = zeros(3, 4);
D[0, 0] = 42;
D[1:2, 2:3] = [[7, 7], [7, 7]];
print D;
print D[2, 2];
