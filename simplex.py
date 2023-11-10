import numpy as np
from numpy import concatenate, dot, identity
from numpy.linalg import inv


def pivot(Matrix,i,j):
    B = np.ones(Matrix.shape)
    for k in range(Matrix.shape[0]):
            if k != i:
                B[k,:] = Matrix[k,:] + (-Matrix[k,j]/Matrix[i,j])*Matrix[i,:]
            else:
                continue
    B[i,:] = Matrix[i,:]/Matrix[i,j]
    return B

def criar_tableau(custo_atual,custo_reduzido,b,B_1A):
    
    m = len(b)
    
    tableau = concatenate((                             # Criação do tableau
    np.insert(b,0,custo_atual).reshape(m+1,1),          # Coluna 0 ->                   -cbxb / B_1b        
    concatenate((custo_reduzido,B_1A),axis=0)),         # Demais colunas do Tableau ->  c - cbB_1A | B_1A 
    axis=1)

    return tableau

def simplex_iteration(tableau, B, i):
    while np.any(np.round(tableau[0,1:],10)<0):
        print(B)
        index_j = np.where(tableau[0,1:]<0)[0][0]
        
        denominador = tableau[1:,index_j+1].copy()
        denominador[denominador<=0] = np.nan
        dummy = tableau[1:,0]/denominador
        index_i = np.nanargmin(dummy) 
        
        print(B[index_i],'<-',index_j)
        B[index_i] = index_j
        
        
        tableau = np.round(pivot(tableau,index_i+1,index_j+1),10)
        print(tableau)
        i+=1
        
    return tableau, B, i

# Achar uma solução inicial -> achar uma base inicial que seja LI -> gerar uma base LI adicionando uma identidade no final da matrix dos coeficientes
# Resolver o probelma auxiliar


def simplex(c, A, b):
        
    # Input do problema

    # c -> Matrix dos custos
    # A -> Matrix dos coenficientes das restriçõees
    # b -> Matrix das restrições

    if A.shape[0]!=len(b) or A.shape[1]!=len(c):
        print("O problema fornecido contém matrizes de tamanhos incompatíveis.")
    
    else:

        # Achar uma solução inicial -> achar uma base inicial que seja LI -> gerar uma base LI adicionando uma identidade no final da matrix dos coeficientes
        # Resolver o probelma auxiliar

        # Problema Auxiliar | Simplex fase 1

        i=0

        m,n = A.shape[0], A.shape[1]

        A_aux = concatenate((A,identity(m)),axis=1) # Criando m variáveis artificiais -> Uma Identidade mxm na matrix dos coeficientes
        n_aux = A_aux.shape[1] # n+m colunas

        custo_aux = concatenate((np.zeros(n_aux-m),np.ones(m)),axis=0)
        Base_aux = [n for n in range(n,n_aux)] 
        print(Base_aux)
        custo_atual_aux = -dot(custo_aux[Base_aux],b)
        custo_reduzido_aux = custo_aux -  dot(custo_aux[Base_aux].reshape(1,m), A_aux)

        tableau_aux = criar_tableau(custo_atual_aux, custo_reduzido_aux, b, A_aux) 

        print(tableau_aux)
        sol_inicial, B, i = simplex_iteration(tableau_aux, Base_aux, i)
        print('Solução Auxiliar encontrada')
        print(B)
        if sol_inicial[0,0]>0:
            print('The original LP has no feasible solution.')
        
        artificial_var = np.where(np.array(B)>n)[0]

        # exit()
        if len(artificial_var) > 0:
            for l in artificial_var:
                if np.all(sol_inicial[l+1,:n+1]==0): # Checar restricão redundante 
                    sol_inicial = sol_inicial[[n for n in range(m+1) if n!=l+1]] # Descarta a linha LD redundante
                else:
                    for index, l_i in enumerate(sol_inicial[l+1,1:n+1]):
                        # print(index, '-', l_i,end=', ')
                        if l_i==0:
                            continue
                        else:
                            sol_inicial = pivot(sol_inicial,l+1,index+1)
                            print(f'{B[l]}<-{index}')
                            B[l] = index
                            break
        print(sol_inicial)

        x_ = np.zeros(A_aux.shape[1])
        x_[B] = sol_inicial[1:,0]
        x = x_[:-m]

        # Problema Principal | Simplex Fase 2
        var_basicas = sol_inicial[1:,0]
        custo_atual = -dot(c[B],x[B])
        inv_base = inv(A[:,B])                                                          # Inverso da base B: B_1
        table_A = np.round(dot(inv_base,A),10)
        custo_reduzido = c - dot(c[B].reshape(1,m),table_A)

        tableau = criar_tableau(custo_atual, custo_reduzido, var_basicas, table_A)

        print(B,'\n',tableau)
        resultado, base_final, i = simplex_iteration(tableau, B, i)


        # Solução

        x_final = np.zeros(len(c))
        x_final[base_final] = resultado[1:,0]
        custo_otimo = -resultado[0,0]

        print(f"\nCusto ótimo : {custo_otimo}\nSolução ótima : {x_final}\nNúmero de iterações : {i}")



if __name__ == '__main__':
    np.set_printoptions(suppress=True)
    A = np.array([[0.2,0.5,0.4,1,0],
                  [0.6,0.4,0.4,0,1],
                  [1,1,1,0,0]])
    c = np.array([0.56,0.81,0.46,0,0])
    b = np.array([0.3,0.5,1])
    # print(len(b),len(c))
    simplex(c,A,b)
