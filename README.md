# LP_Simplex
Simplex implementation in Python (using Numpy) for Linear Optimization class 2023.

## Lista de Problemas testados
### Arenale
- Exemplo 2.1
    A = np.array([[1,1,1,1,0],
                  [0,0,0,0,1],
                  [1,0,0,0,0]])
    c = np.array([0.56,0.81,0.46,0,0])
    b = np.array([0.3,0.5,1]) 
    <!-- 3 variáveis e 3 restrições -->

- Exemplo 2.3
    A = np.array([[1,1,1,0,0,0,1,0],
                  [0,0,0,1,1,1,0,1],
                  [1,0,0,1,0,0,0,0],
                  [0,1,0,0,1,0,0,0],
                  [0,0,1,0,0,1,0,0]])
    c = np.array([4,2,5,11,7,4,0,0])
    b = np.array([800,1000,500,400,900])
    <!-- 6 varáveis, 5 restrições -->

- Exemplo 2.4
    A = np.array([[1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0],
                  [0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0],
                  [0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,0],
                  [0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1],
                  [1,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0],
                  [0,1,0,0,1,0,0,1,0,0,1,0,0,0,0,0],
                  [0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,0]])
    c = np.array([30,13,21,12,40,26,27,15,35,37,25,19,0,0,0,0])
    b = np.array([433,215,782,300,697,421,612])
     <!-- 12 variáveis, 7 restrições -->

### Netlib.org/lp/data/
- afiro.mps
- adlittle.mps
- share2b.mps
- itest2.mps
- sc205.mps