import numpy as np
from pulp import LpProblem

""" Cria um objeto que recebe um problema de programação linear no formato MPS e o representa na forma padrão, com a matriz dos 
    coeficientes, o vetor custo e o vetor RHS como atributos para serem subsequentemente usados como argumentos para a função simplex. """


class LP:
    
    def __init__(self, file):
        self.var, prob = LpProblem.fromMPS(file)                                # converte o problema da forma mps para 
        self.prob = prob.toDict()                                               # um dicionário self.prob contendo as variáveis, 
        self.var_index = {value:index for index,value in enumerate(self.var)}   # as restrições, a função objetivo etc

         # sense –> LpConstraintEQ, LpConstraintGE, LpConstraintLE (0, 1, -1 respectivamente)

        cons = {1.0:0, 0.0:0, -1.0:0}                                            
        count = np.zeros(len(self.prob['constraints']))                          # conta e armazena quantas restrições são de
        for index, row in enumerate(self.prob['constraints']):                   # igualdade (0), maior igual (1.0) ou menor igual (-1.0).
            count[index] = row['sense']
        unique, counts = np.unique(count, return_counts=True)
        for val,cou in zip(unique,counts):
            cons[val] = cou
        self.cons = cons


        # Matriz do custo
        c = np.zeros(len(self.var)+cons[-1.0]+cons[1.0])                                # cria um vetor dos custos já na forma padrão
        c_coefficients = self.prob['objective']['coefficients']                         # (acrescida das variáveis de folga)
        value = {variable['name']:variable['value'] for variable in c_coefficients}
        for index, variable in enumerate(self.var.keys()):
            if variable in value.keys():
                c[index] = value[variable]
            else:
                c[index] = 0
        self.c = c


        # RHS matrix                                                                   # cria o vetor b dos valores no lado direito
        b = np.zeros(len(self.prob['constraints']))                                    # das restrições (right hand side)
        for index, row in enumerate(self.prob['constraints']):
            b[index] =  - row['constant'] if row['constant']!=0 else 0
        self.b = b
    

        # Matriz dos coeficientes
        A = np.zeros((len(self.prob['constraints']),len(c)))                           # cria a matriz dos coeficientes na forma padrão
        i = len(self.var)                                                              # com as variáveis de folga acrescidas (caso 
        for index, row in enumerate(self.prob['constraints']):                         
            for column in row['coefficients']:
                A[index, self.var_index[column['name']]] = column['value']
            if row['sense'] == 1.0:
                A[index,i] = -1
                i+=1
            if row['sense'] == -1.0:
                A[index,i] = 1
                i+=1
        
        self.A = A

