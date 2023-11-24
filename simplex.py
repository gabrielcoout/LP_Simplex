import numpy as np
from numpy import concatenate, dot, identity
from numpy.linalg import inv
import time



def pivot(Matrix,i,j):
    B = np.ones(Matrix.shape)
    for k in range(Matrix.shape[0]):
            if k != i:
                B[k,:] = Matrix[k,:] + (-Matrix[k,j]/Matrix[i,j])*Matrix[i,:]
            else:
                continue
    B[i,:] = Matrix[i,:]/Matrix[i,j]
    return B

def r_bland(v):

    pass


def criar_tableau(custo_atual,custo_reduzido,b,B_1A):
    
    m = len(b)
    
    tableau = concatenate((                             # Criação do tableau
    np.insert(b,0,custo_atual).reshape(m+1,1),          # Coluna 0 ->                   -cbxb / B_1b        
    concatenate((custo_reduzido,B_1A),axis=0)),         # Demais colunas do Tableau ->  c - cbB_1A | B_1A 
    axis=1)

    return tableau


def simplex_iteration(tableau, B, i, p):
    
    while np.any(np.round(tableau[0,1:], p)<0):
        
        index_j = np.where(tableau[0,1:]<0)[0][0]
        # print(tableau[0,index_j+1])
        # print(tableau[0,1:])

        denominador = tableau[1:,index_j+1].copy()
        denominador[denominador<=0] = np.nan
        dummy = tableau[1:,0]/denominador
        index_i = np.nanargmin(dummy) 
        

        
        # print(B[index_i],'<-',index_j)
        B[index_i] = index_j
        
        
        tableau = pivot(tableau,index_i+1,index_j+1)
        # print(tableau)
    
    
        i+=1
        # time.sleep(0.1)
        
    return tableau, B, i


# Achar uma solução inicial -> achar uma base inicial que seja LI -> gerar uma base LI adicionando uma identidade no final da matrix dos coeficientes
# Resolver o probelma auxiliar

def simplex(c, A, b, p):
        
    # Input do problema

        # c -> Matrix dos custos
        # A -> Matrix dos coenficientes das restriçõees
        # b -> Matrix das restrições

    if A.shape[0]!=len(b) or A.shape[1]!=len(c):                                    
        print("O problema fornecido contém matrizes de tamanhos incompatíveis.")
        return None 
    
    ##########################################################################################################################
    ##########################################################################################################################

    # Problema Auxiliar | Simplex Fase 1

    i=0 # contador das iterações (do simplex)

    m,n = A.shape[0], A.shape[1]

    A_aux = concatenate((A,identity(m)),axis=1)     # Criando m variáveis artificiais -> Uma Identidade mxm na matrix dos coeficientes
    n_aux = A_aux.shape[1]                          # Númeoro de colunas da matrix dos coeficientes com as variáveis auxiliares

    custo_aux = concatenate((np.zeros(n_aux-m),np.ones(m)),axis=0)                  # custo auxiliar
    Base_aux = [n for n in range(n,n_aux)]                                          # base auxiliar
    custo_atual_aux = -dot(custo_aux[Base_aux],b)                                   # custo atual do problema auxiliar
    custo_reduzido_aux = custo_aux -  dot(custo_aux[Base_aux].reshape(1,m), A_aux)  # custo reduzido do problema auxiliar
    tableau_aux = criar_tableau(custo_atual_aux, custo_reduzido_aux, b, A_aux)      # criação do tableau


    sol_inicial, B, i = simplex_iteration(tableau_aux, Base_aux, i, p)                 # aplicação do tableau no problema auxiliar
    print('---------------------------------Solução Auxiliar encontrada---------------------------------')
    if round(sol_inicial[0,0],p)>0:
        print('O problema original não tem solução.')
    
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
                        # print(f'{B[l]}<-{index}')
                        B[l] = index
                        break
    # print(sol_inicial)

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

    # print(B,'\n',tableau)
    resultado, base_final, i = simplex_iteration(tableau, B, i, p)


    # Solução

    x_final = np.zeros(len(c))
    x_final[base_final] = resultado[1:,0]
    # custo_otimo = dot(c,x)
    custo_otimo = -resultado[0,0]

    print(f"\nCusto ótimo : {custo_otimo}\nSolução ótima : {x_final}\nNúmero de iterações : {i}")



if __name__ == '__main__':
    np.set_printoptions(suppress=True)
    A = np.array([[1,1,1,0,0,0,1,0],
                  [0,0,0,1,1,1,0,1],
                  [1,0,0,1,0,0,0,0],
                  [0,1,0,0,1,0,0,0],
                  [0,0,1,0,0,1,0,0]])
    c = np.array([4,2,5,11,7,4,0,0])
    b = np.array([800,1000,500,400,900])
    # print(len(b),len(c))
    import time
    start_time = time.time()
    simplex(c,A,b,14)
    print(f"--- {time.time() - start_time:.4f} seconds ---")

