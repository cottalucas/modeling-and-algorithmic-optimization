from estrutura import Vertice
from copy import deepcopy
 
ListaFechados = []
 
#heuristica - quantidade de peças na posição incorreta
def h1(Estado):
    #Definindo matriz final desejada
 
    matrizFinal = [[1, 12, 11, 10],
                  [2, 13, 0, 9],
                  [3, 14, 15, 8],
                  [4, 5, 6, 7]]        
     
 
    global contador
    contador = 0
    for x in range(4):
        for y in range(4):
            if Estado.matriz[x][y] != matrizFinal[x][y]:
                contador +=1
    return(contador)
 
 
 
def GeraSuc(Estado): #na geração de sucessores 4 novos estados podem ser criados.
    global w
 
    #descorberta espaço em branco
     
    for x in range(4):
            for y in range(4):
                if Estado.matriz[x][y] == 0:
                    a = x
                    b = y
 
    #realiza os movimentos possiveis movimentos e faz o calculo das heuristicas
 
    MoverBaixo(Estado, a, b)
    MoverCima(Estado, a, b)    
    MoverEsq(Estado, a, b)
    MoverDir(Estado, a, b)
    Listas(Estado)
    return(Estado.h)
 
def MoverBaixo(Estado, a, b):
    global Estado0
    if a != 0:
        Estado0 = Vertice([[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]], Estado.f, Estado.g, 0, Estado) #estanciando o novo estado        
 
        Estado0.matriz = deepcopy(Estado.matriz) #passagem por valor
        aux = Estado0.matriz[a][b]
        Estado0.matriz[a][b] = Estado0.matriz[a-1][b]
        Estado0.matriz[a-1][b] = aux
 
        #calculo de F(x), H(x) e G(x)
        h1(Estado0)
        Estado0.h = contador
        Estado0.g = Estado.g + 1
        Estado0.f = Estado0.h + Estado0.g
        #print(Estado0.matriz)
        return(Estado0)
 
 
def MoverCima(Estado, a, b):
    global Estado1
    if a != 3:
        Estado1 = Vertice([[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]], Estado.f, Estado.g, 0, Estado) #estanciando novo estado
     
        Estado1.matriz = deepcopy(Estado.matriz) #passagem por valor
        aux = Estado1.matriz[a][b]
        Estado1.matriz[a][b] = Estado1.matriz[a+1][b]
        Estado1.matriz[a+1][b] = aux
 
        #calculo de F(x), H(x) e G(x)
        h1(Estado1)
        Estado1.h = contador
        Estado1.g = Estado.g + 1
        Estado1.f = Estado1.h + Estado1.g
        #print(Estado1.matriz)
        return(Estado1)
 
 
def MoverEsq(Estado, a, b):
    global Estado2
    if b != 3:
        Estado2 = Vertice([[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]], Estado.f, Estado.g, 0, Estado) #estanciando novo estado
     
        Estado2.matriz = deepcopy(Estado.matriz) #passagem por valor
        aux = Estado2.matriz[a][b]
        Estado2.matriz[a][b] = Estado2.matriz[a][b+1]
        Estado2.matriz[a][b+1] = aux
 
        #calculo de F(x), H(x) e G(x)
        h1(Estado2)
        Estado2.h = contador
        Estado2.g = Estado.g + 1
        Estado2.f = Estado2.h + Estado2.g
        #print(Estado2.matriz)
        return(Estado2)
 
 
def MoverDir(Estado, a, b):
    global Estado3
    if b != 0:
        print("ENTROU")
        Estado3 = Vertice([[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]], Estado.f, Estado.g, 0, Estado) #estanciando novo estado
        Estado3.g = Estado.h #atribuindo valor de G(x)
     
        Estado3.matriz = deepcopy(Estado.matriz) #passagem por valor
        aux = Estado3.matriz[a][b]
        Estado3.matriz[a][b] = Estado3.matriz[a][b-1]
        Estado3.matriz[a][b-1] = aux
 
        #calculo de F(x), H(x) e G(x)
        h1(Estado3)
        Estado3.h = contador
        Estado3.g = Estado.g + 1
        Estado3.f = Estado3.h + Estado3.g
        #print(Estado3.matriz)
        return(Estado3)
     
 
def Listas(Estado): #retorna valor do menor estado na lista dos abertos
    global w #variavel que recebe a posição que contem o Estado a ser tomado
    global ListaAbertos
    global ListaFechados
     
    ListaAbertos.append(Estado0) 
    ListaAbertos.append(Estado1)
    ListaAbertos.append(Estado2)
    ListaAbertos.append(Estado3)
 
    #lista para tomada de decisão
    TD = [(Estado0.f)] 
    TD.append(Estado1.f)
    TD.append(Estado2.f)
    TD.append(Estado3.f)
 
    d = min(TD) #menor peso da lista de peças na posição incorreta (peso de f(x))
 
    w = TD.index(d) #posição da lista de menor valor
 
    ListaFechados.append(ListaAbertos[w])
     
    del ListaAbertos[w] #remover estado a ser tomado
 
    print("LISTA DE DECISÃO")
    print(TD)
 
    print(w)
 
    return(ListaAbertos, ListaFechados)
    return(w)
    
 
def Decisão(w):
 
    print(w)
    print(Estado0.matriz)
 
    global EstadoAux
    EstadoAux = Vertice([[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]], 0, 0, 0, None)
    if w == 0:
        EstadoAux = deepcopy(Estado0)
    elif w == 1:
        EstadoAux = deepcopy(Estado1)
    elif w == 2:
        EstadoAux = deepcopy(Estado2)
    elif w == 3:
        EstadoAux = deepcopy(Estado3)
    return(EstadoAux)
 
 
  
#main
 
 
#estanciando o objeto
 
matrizRecebida = [[1, 12, 11, 10],[0, 2, 13, 8],[5, 4, 9, 15],[3, 6, 14, 7]] #recebendo matriz a ser resolvida
Estado = Vertice(matrizRecebida, 0, 0, 0, None)
EstadoAux = deepcopy(Estado)
ListaAbertos = []   #inicializando lista abertos
 
while h1(EstadoAux) != 0:
    #Gerando matrizes filhas
    GeraSuc(EstadoAux)
    #Tomada de Decisão
    Decisão(w)    
    print("MATRIZ AUXILIAR ATUAL!")
    print(EstadoAux.matriz)
 
           
 
 
 
 
 
  
 
 
 
 
 
         
        
