import numpy as np
from numpy import concatenate, dot, identity, nan, nanargmin, where
from numpy.linalg import inv
from time import time

# ---------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------

def pivot(Matrix,i,j):  
    """ Retorna uma matrix (array) obtida a partir de operações de soma e multiplicação por escalar das linhas
        de modo que o elemento da i-ésima linha e j-ésima coluna (pivô) seja 1 e os demais elementos da j-ésima
        coluna sejam nulos. """

    A = np.ones(Matrix.shape)
    for k in range(Matrix.shape[0]):
            if k != i:
                A[k,:] = Matrix[k,:] + (-Matrix[k,j]/Matrix[i,j])*Matrix[i,:]
            else:
                continue
    A[i,:] = Matrix[i,:]/Matrix[i,j]
    
    return A

# ---------------------------------------------------------------------------------------------------------------------------------

def criar_tableau(custo_atual,custo_reduzido,b,B_1A):
    """ Cria a matrix correspondente ao tableau completo a partir do custo atual e do vetor dos custos reduzidos, 
        dos custos (b) e do produto da inversa da base (B) pela matrix dos coeficientes (A)"""
    
    m = len(b)                                          
    
    tableau = concatenate((                             
    np.insert(b,0,custo_atual).reshape(m+1,1),                  
    concatenate((custo_reduzido,B_1A),axis=0)),          
    axis=1)

    return tableau

# ---------------------------------------------------------------------------------------------------------------------------------

def iteração_simplex(tableau, B, i, p):
    
    while np.any(np.round(tableau[0,1:], p)<0):
        
        index_j = where(tableau[0,1:]<0)[0][0]       # guarda o índice da primeira variável menor que zero (Regra de Bland)
                                                        # nos custos reduzidos -> índice que vai entrar na base 
    

        denominador = tableau[1:,index_j+1].copy()      # cria uma cópia da coluna referente no tableau à variável que entra na base
        denominador[denominador<=0] = nan            # torna todas os elementos não negativos da coluna no tipo nan (a ser desprezado) 
        dummy = tableau[1:,0]/denominador               # 
        index_i = nanargmin(dummy) 
        

        
        # print(B[index_i],'<-',index_j)
        B[index_i] = index_j
        
        
        tableau = pivot(tableau,index_i+1,index_j+1)
    
        i+=1
        
    return tableau, B, i

    # ---------------------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------------------------


def simplex(c, A, b, p=10):
    start_time = time()
    # Input do problema

        # c -> Matrix dos custos
        # A -> Matrix dos coenficientes das restriçõees
        # b -> Matrix das restrições
        # p -> coeficiente de arredondamento 

    if A.shape[0]!=len(b) or A.shape[1]!=len(c):                                    
        print("O problema fornecido contém matrizes de tamanhos incompatíveis.")
        return None 
    
    # ---------------------------------------------------------------------------------------------------------------------------------

    # Problema Auxiliar | Simplex Fase 1

    i=0                                             # contador das iterações (do simplex)

    m,n = A.shape[0], A.shape[1]

    A_aux = concatenate((A,identity(m)),axis=1)     # criando m variáveis artificiais -> Uma Identidade mxm na matrix dos coeficientes
    n_aux = A_aux.shape[1]                          # número de colunas da matrix dos coeficientes com as variáveis auxiliares


    custo_aux = concatenate((np.zeros(n_aux-m),np.ones(m)),axis=0)                  # custo auxiliar
    Base_aux = [n for n in range(n,n_aux)]                                          # base auxiliar
    custo_atual_aux = -dot(custo_aux[Base_aux],b)                                   # custo atual do problema auxiliar
    custo_reduzido_aux = custo_aux -  dot(custo_aux[Base_aux].reshape(1,m), A_aux)  # custo reduzido do problema auxiliar
    tableau_aux = criar_tableau(custo_atual_aux, custo_reduzido_aux, b, A_aux)      # criação do tableau


    sol_inicial, B, i = iteração_simplex(tableau_aux, Base_aux, i, p)              # aplicação do tableau no problema auxiliar
    
    if round(-sol_inicial[0,0],p)>0:                                                # teste de viabilidade -> se o custo reduzido
        print(sol_inicial[0][0])                                                    # do problema auxiliar for maior que zero então
        print('O problema original não tem solução.')                               # o problema original é inviável
        return None

    print('---------------------------------Solução Auxiliar encontrada---------------------------------')

    artificial_var = where(np.array(B)>n)[0]                                     # verifica se há alguma variável artificial na base
    if len(artificial_var) > 0:                                                     # caso haja alguma variável artifcial na base
        for l in artificial_var:
            if np.all(sol_inicial[l+1,:n+1]==0):                                    # checa  a existência de restricão redundante 
                sol_inicial = sol_inicial[[n for n in range(m+1) if n!=l+1]]        # descarta a restrição redundante
            else:
                for index, l_i in enumerate(sol_inicial[l+1,1:n+1]):                
                    if l_i==0:
                        continue
                    else:
                        sol_inicial = pivot(sol_inicial,l+1,index+1)                
                        B[l] = index                                                # grava a base viável para o problema original
                        break

    x_ = np.zeros(A_aux.shape[1])                                                   
    x_[B] = sol_inicial[1:,0]
    x = x_[:-m]

    # ---------------------------------------------------------------------------------------------------------------------------------

    # Problema Principal | Simplex Fase 2

    var_basicas = sol_inicial[1:,0]                                                 # custo reduzido na base B
    custo_atual = -dot(c[B],x[B])                                                   # custo atual na base B
    inv_base = inv(A[:,B])                                                          # Inverso da base inicial B
    table_A = np.round(dot(inv_base,A),p)
    custo_reduzido = c - dot(c[B].reshape(1,m),table_A)

    tableau = criar_tableau(custo_atual, custo_reduzido, var_basicas, table_A)      # cria o tableau pro problema original na base B

    # print(B,'\n',tableau)
    resultado, base_final, i = iteração_simplex(tableau, B, i, p)                   # resolve o tableau da fase 2 do simplex



    # Solução

    x_final = np.zeros(len(c))                                                      
    x_final[base_final] = resultado[1:,0]                                           # armazena os valores das variáveis na solução ótima
    custo_otimo = - resultado[0,0]                                                  # guarda o custo ótimo obtido no simplex

    print(f"\nCusto ótimo : {custo_otimo}\nSolução ótima : {x_final}\nNúmero de iterações : {i}")
    print(f"--- {time() - start_time:.4f} seconds ---")
    
    return custo_otimo


if __name__ == '__main__':
    np.set_printoptions(suppress=True)
    A = np.array([[1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0],
                  [0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0],
                  [0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,0],
                  [0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1],
                  [1,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0],
                  [0,1,0,0,1,0,0,1,0,0,1,0,0,0,0,0],
                  [0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,0]])
    c = np.array([30,13,21,12,40,26,27,15,35,37,25,19,0,0,0,0])
    b = np.array([433,215,782,300,697,421,612])
    # print(len(b),len(c))
    simplex(c,A,b,14)


