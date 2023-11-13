import codecs, json
import numpy as np

from pulp import LpProblem

def mps_to_numpy(file):
    
    var, prob = LpProblem.fromMPS(file)

    lp_prob = prob.toDict()

    var_index = {value:index for index,value in enumerate(var)}


    cons = {1.0:0, 0.0:0, -1.0:0} # sense –> one of LpConstraintEQ, LpConstraintGE, LpConstraintLE (0, 1, -1 respectively)
    count = np.zeros(len(lp_prob['constraints']))
    for index, row in enumerate(lp_prob['constraints']):
        count[index] = row['sense']
    unique, counts = np.unique(count, return_counts=True)
    for val,cou in zip(unique,counts):
        cons[val] = cou

    # Matriz do custo
    c = np.zeros(len(var)+cons[-1.0]+cons[1.0])
    c_coefficients = lp_prob['objective']['coefficients']
    value = {variable['name']:variable['value'] for variable in c_coefficients}
    for index, variable in enumerate(var.keys()):
        if variable in value.keys():
            c[index] = value[variable]
        else:
            c[index] = 0

    # RHS matrix
    b = np.zeros(len(lp_prob['constraints']))
    for index, row in enumerate(lp_prob['constraints']):
        b[index] = row['constant']

    
    # Matriz dos coeficientes
    A = np.zeros((len(lp_prob['constraints']),len(c)))

    i = len(var)
    for index, row in enumerate(lp_prob['constraints']):
        for column in row['coefficients']:
            A[index, var_index[column['name']]] = column['value']
        if row['sense'] == 1.0:
            A[index,i] = -1
            i+=1
        if row['sense'] == -1.0:
            A[index,i] = 1
            i+=1
    return c, A, b

if __name__ == '__main__':
    c, A, b = mps_to_numpy("LP_Simplex/share2b.mps")
    