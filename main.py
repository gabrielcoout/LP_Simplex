# Arquivo contendo todos os testes feitos ao algoritmo simplex
# Basta descomentar o código para testar

from numpy import set_printoptions # -> Para melhorar a visibilidade dos outputs
from simplex import simplex
from converter import mps_to_numpy
import pulp as pl

# ---------------------------------------------------------------------------------------------------------------------------------


n = 5                              # quantidade de casas decimais que a solução mostra
set_printoptions(n,suppress=True)  

# ---------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":



    # Problemas do livro PESQUISA OPERACIONAL

    # Exemplo 2.1
    # A = np.array([[0.2,0.5,0.4,1,0],
    #               [0.6,0.4,0.4,0,1],
    #               [1,1,1,0,0]])
    # c = np.array([0.56,0.81,0.46,0,0])
    # b = np.array([0.3,0.5,1]) 

    # Exemplo 2.3
    # A = np.array([[1,1,1,0,0,0,1,0],
    #               [0,0,0,1,1,1,0,1],
    #               [1,0,0,1,0,0,0,0],
    #               [0,1,0,0,1,0,0,0],
    #               [0,0,1,0,0,1,0,0]])
    # c = np.array([4,2,5,11,7,4,0,0])
    # b = np.array([800,1000,500,400,900])

    # Exemplo 2.4
    # A = np.array([[1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0],
    #               [0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0],
    #               [0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,0],
    #               [0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1],
    #               [1,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0],
    #               [0,1,0,0,1,0,0,1,0,0,1,0,0,0,0,0],
    #               [0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,0]])
    # c = np.array([30,13,21,12,40,26,27,15,35,37,25,19,0,0,0,0])
    # b = np.array([433,215,782,300,697,421,612])



    # Problemas da base NETLIB
    file = 'test/afiro.mps'
    # file = 'test/adlittle.mps'
    # file = 'test/itest2.mps'
    # file = 'test/itest6.mps'
    # file = 'test/qual.mps'
    # file = 'test/sc205.mps'
    # file = 'test/scagr25.mps'
    # file = 'test/scagr7.mps'
    # file = 'test/share2b.mps'
    c, A, b = mps_to_numpy(file)

    # ALGORITMO SIMPLEX
    # colocar o argumento msg == True caso queira ver a solução ótima -> o x* ótimo
     
    simplex(c, A, b)

# ---------------------------------------------------------------------------------------------------------------------------------


    # GABARITO -> 

    # var, prob = pl.LpProblem.fromMPS(file)
    # solver = pl.get_solver(pl.list_solvers(onlyAvailable=True)[0])       # PuLP procura um solver (no caso, usou-se o GLPK, o primeiro da
    # prob.solve(solver)                                                   # lista dos disponíveis) e resolve o problema usando ele. 
                                                                           # O GLPK precisa estar baixado





