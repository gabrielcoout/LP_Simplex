import numpy as np
from pulp import LpProblem

""" Recebe um problema de programação linear em formato MPS e retorna um problema equivalente na forma padrão, com a matriz dos 
    coeficientes, o vetor custo e o vetor RHS como atributos para serem subsequentemente usados como argumentos para a função simplex. """
import numpy as np

from pulp import LpProblem

def mps_to_numpy(file):                                                                 # converte o problema da forma mps para 
    var, prob = LpProblem.fromMPS(file)                                                 # a forma padrão em numpy arrays  

    lp_prob = prob.toDict()

    var_index = {value:index for index,value in enumerate(var)}


    cons = {1.0:0, 0.0:0, -1.0:0} 
    count = np.zeros(len(lp_prob['constraints']))                                       # conta e armazena quantas restrições são de
    for index, row in enumerate(lp_prob['constraints']):                                # igualdade (0), maior igual (1.0) ou menor igual (-1.0).
        count[index] = row['sense']
    unique, counts = np.unique(count, return_counts=True)
    for val,cou in zip(unique,counts):
        cons[val] = cou

    # Matriz do custo
    c = np.zeros(len(var)+cons[-1.0]+cons[1.0])                                         # cria um vetor dos custos já na forma padrão
    c_coefficients = lp_prob['objective']['coefficients']                               # (acrescido das variáveis de folga)                       
    value = {variable['name']:variable['value'] for variable in c_coefficients}
    for index, variable in enumerate(var.keys()):
        if variable in value.keys():
            c[index] = value[variable]
        else:
            c[index] = 0

    # RHS matrix
    b = np.zeros(len(lp_prob['constraints']))                                           # # cria o vetor b dos valores no lado direito
    for index, row in enumerate(lp_prob['constraints']):                                # das restrições (right hand side)
        b[index] =  - row['constant'] if row['constant']!=0 else 0

    
    # Matriz dos coeficientes
    A = np.zeros((len(lp_prob['constraints']),len(c)))                                  # cria a matriz dos coeficientes na forma padrão
    i = len(var)                                                                        # com as variáveis de folga acrescidas (para
    for index, row in enumerate(lp_prob['constraints']):                                # cada restrição seja desigualdade, é coadunado 
        for column in row['coefficients']:                                              # uma coluna da identidade ou o seu oposto)
            A[index, var_index[column['name']]] = column['value']
        if row['sense'] == 1.0:
            A[index,i] = -1
            i+=1
        if row['sense'] == -1.0:
            A[index,i] = 1
            i+=1
    return c, A, b


# if __name__ == '__main__':
#     c, A, b = mps_to_numpy("LP_Simplex/afiro.mps")
#     print(A.shape)
