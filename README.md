# LP_Simplex
Simplex implementation in Python (using Numpy) for Linear Optimization class 2023.


Arenale
Exemplo 2.1
Exemplo 2.3
Exemplo 2.4
A = np.array([[1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0],
                  [0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0],
                  [0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,0],
                  [0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1],
                  [1,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0],
                  [0,1,0,0,1,0,0,1,0,0,1,0,0,0,0,0],
                  [0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,0]])
    c = np.array([30,13,21,12,40,26,27,15,35,37,25,19,0,0,0,0])
    b = np.array([433,215,782,300,697,421,612])