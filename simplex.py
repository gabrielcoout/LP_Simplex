import numpy as np
from numpy import concatenate, dot, identity, nan, nanargmin, where
from numpy.linalg import inv
from time import time, sleep
from converter import *

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
    """ Retorna a matrix correspondente ao tableau completo a partir do custo atual e do vetor dos custos reduzidos, 
        dos custos (b) e do produto da inversa da base (B) pela matrix dos coeficientes (A)"""
    
    m = len(b)                                          
    
    tableau = concatenate((                             
    np.insert(b,0,custo_atual).reshape(m+1,1),                  
    concatenate((custo_reduzido,B_1A),axis=0)),          
    axis=1)

    return tableau

# ---------------------------------------------------------------------------------------------------------------------------------

def iteracao_simplex(tableau, B, i, p):
    
    while np.any(np.round(tableau[0,1:], p)<0):
        index_j = where(np.round(tableau[0,1:], p)<0)[0][0]       # guarda o índice da primeira variável menor que zero (Regra de Bland)
                                                                  # nos custos reduzidos -> índice que vai entrar na base 
        denominador = tableau[1:,index_j+1].copy()   
        denominador[np.round(denominador,10)<=0] = nan             
        dummy = tableau[1:,0]/denominador                
        index_i = nanargmin(dummy) 

        # print(B[index_i],'<-',index_j)
        B[index_i] = index_j
        
        tableau = pivot(tableau,index_i+1,index_j+1)
        i+=1
        # sleep(0.5)

        
    return tableau, B, i

# ---------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------


def simplex(c, A, b, p=1, msg=False):
    start_time = time()
    
    # Input do problema

        # c -> Matrix dos custos
        # A -> Matrix dos coenficientes das restriçõees
        # b -> Matrix das restrições
        # p -> coeficiente de arredondamento
        # msg -> caso verdadeiro, a função imprime a soluçao básica encontrada 



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
    Base_aux = np.array([n for n in range(n,n_aux)])                                # base auxiliar
    custo_atual_aux = -dot(custo_aux[Base_aux],b)                                   # custo atual do problema auxiliar
    custo_reduzido_aux = custo_aux -  dot(custo_aux[Base_aux].reshape(1,m), A_aux)  # custo reduzido do problema auxiliar
    tableau_aux = criar_tableau(custo_atual_aux, custo_reduzido_aux, b, A_aux)      # criação do tableau

    # ---------------------------------------------------------------------------------------------------------------------------------

    if custo_atual_aux == 0:                                                            # caso o problema auxiliar já tenha custo 0
        print('Solução Auxiliar encontrada[1]')                                         # pode-se usar a base obtida retirando-se
        sol_inicial = tableau_aux                                                       # as variáveis artificiais
        B = Base_aux

    else:
        
        sol_inicial, B, i = iteracao_simplex(tableau_aux, Base_aux, i, p)               # aplicação do tableau no problema auxiliar

        if round(-sol_inicial[0,0],p)>0:                                                # teste de viabilidade -> se o custo reduzido é maior que 0
            print(f'O problema original não tem solução. O custo obtido foi  {-sol_inicial[0][0]:.10f}')                                          
            return None                                                                 
            
        else:
            print('Solução Auxiliar encontrada[2]\n')
            pass
    
    # ---------------------------------------------------------------------------------------------------------------------------------

    artificial_var = where(np.array(B)>n-1)[0]                                            # verifica se há alguma variável artificial na base

    if len(artificial_var) > 0:                                                           # caso haja alguma variável artifcial na base
        for art_var in artificial_var:
            if np.all(np.round(sol_inicial[art_var+1,:n+1],p)==0):                        # checa  a existência de restricão redundante 
                m_ = sol_inicial.shape[0]                                                 # atualiza o número de linhas (restrições)      
                sol_inicial = sol_inicial[[n for n in range(m_) if n!=art_var+1]]         # descarta a restrição redundante
                B[art_var] = -1                                                           # associa -1 ao índice básico relativo a uma
                                                                                          # restrição redundante
            else:
                index = np.argmin(np.round(sol_inicial[art_var+1,1:n+1],p)==0)            # acha o primeiro elemento  da linha diferente de 0     
                sol_inicial = pivot(sol_inicial, art_var+1, index+1)           
                B[art_var] = index                                                        # grava a base viável para o problema original
        B = B[B!=-1]                                                                      # elimina da base as restrições redundantes
        m = sol_inicial.shape[0]-1                                                        # atualiza o valor de m (número de linhas da matriz A)
        
    x = np.zeros(A_aux.shape[1])                                                          # solução básica viável inicial para                                                   
    x[B] = sol_inicial[1:,0]                                                              # o problema original

    # ---------------------------------------------------------------------------------------------------------------------------------

    # Problema Principal | Simplex Fase 2

    var_basicas = sol_inicial[1:,0]                                                 # variáveis básicas do tableau inicial
    custo_atual = -dot(c[B],x[B])                                                   # custo atual na base B
    table_A = sol_inicial[1:,1:n+1]                                                 # matrix B_1A, aproveitada do problema auxiliar
    # table_A = dot(inv(A[B]),A)
    custo_reduzido = c - dot(c[B].reshape(1,m),table_A)                             # custo reduzido na base B
    tableau = criar_tableau(custo_atual, custo_reduzido, var_basicas, table_A)      # cria o tableau pro problema original na base B


    resultado, base_final, i = iteracao_simplex(tableau, B, i, p)                   # resolve o tableau da fase 2 do simplex

    # Solução

    x_final = np.zeros(len(c))                                                      
    x_final[base_final] = resultado[1:,0]                                           # armazena os valores das variáveis na solução ótima
    custo_otimo = - resultado[0,0]                                                  # guarda o custo ótimo obtido no simplex

    print(f"Custo ótimo : {custo_otimo}")
    if msg==True:
        print(f"Solução ótima : {x_final}")
    print(f"Número de iterações : {i}")
    print(f"--- {time() - start_time:.4f} seconds ---")
    
    return custo_otimo


if __name__ == '__main__':
    np.set_printoptions(suppress=True)
   
    c, A, b = mps_to_numpy('test/adlittle.mps')

    simplex(c,A,b)


