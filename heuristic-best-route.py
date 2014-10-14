from copy import deepcopy
import random
import operator
 
nomeArquivo = input("Digite o nome do arquivo a ser lido: ")
arquivo = open(nomeArquivo)
dados = arquivo.readlines()
qtdeLinhasArquivo = len(dados)
coordenadas = []
quantidadeSolucaoInicial = int(input("Digite a quantidade de soluções inicais: "))
taxaMutacao = int(input("Digite a taxa de mutação(porcentagem): "))
operadorCross = int(input("Qual operador de cruzamento deseja utilizar?[0 = OX, 1 = PMX]: "))
mostrarRota = int(input("Deseja mostrar a melhor rota encontrada?[0 = Não, 1 = Sim] "))
for i in range (6, (qtdeLinhasArquivo - 1)):
    coordenadas.append(dados[i])
#coordenadas de todas cidades se encontram na matriz "coordenadas"
 
 
 
def criaListaVertices():
    listaVertices = []
    for i in range (len (coordenadas)):
        linhaQuebrada = coordenadas[i].split()#cria uma lista de argumentos para linha, onde pos 0 possui o indice da coordenada, pos 1 a coordenada X e pos2 a coordenada Y
        vt = deepcopy(Vertice(int(linhaQuebrada[0]), int(linhaQuebrada[1]), int(linhaQuebrada[2])))
        listaVertices.append(vt)
    return(listaVertices)
    #listaVertices contem uma lista de objetos
 
 
class Vertice:
    numeroCidade = None
    coordX = None
    coordY = None
 
    def __init__(self, numeroCidade, coordX, coordY):#construtor
        self.numeroCidade = numeroCidade
        self.coordX = coordX
        self.coordY = coordY
 
class Solucao:
    rota = None
    custoRota = None
 
    def __init__(self, rota, custoRota):
        self.rota = rota
        self.custoRota = custoRota
 
    def calculaCusto(self):
        #custoRota = 5
        distancia = 0
        for i in range((len(self.rota))-1):
            distancia += ((self.rota[i+1].coordX - self.rota[i].coordX)**2 + (self.rota[i+1].coordY - self.rota[i].coordY)**2)**0.5
        distancia += ((self.rota[i].coordX - self.rota[0].coordX)**2 + (self.rota[i].coordY - self.rota[0].coordY)**2)**0.5#custo para voltar para origem
        self.custoRota = distancia
        #print(i)
 
 
def criaSolucaoGulosa():#testar com random.seed
    verticesNaoVisitados = criaListaVertices()
    verticesVisitados = []
    while (len(verticesNaoVisitados))!= 0:
        aleatorio = random.randint(0, (len(verticesNaoVisitados)-1))
        verticesVisitados.append(verticesNaoVisitados[aleatorio])
        verticesNaoVisitados.remove(verticesNaoVisitados[aleatorio])
    #verticesVisitados.append(verticesVisitados[0])
    return(verticesVisitados)
 
 
def geraNSolucoes(n):
    listaSolucoes = []
    random.seed(0)
    for i in range(n):
        rota = criaSolucaoGulosa()
        solucao = Solucao(rota,0)
        solucao.calculaCusto()
        listaSolucoes.append(solucao)
    return(listaSolucoes)
 
def torneio(populacao):
    indices = []
    for i in range (len(populacao)):
        indices.append(i)
    random.shuffle(indices)
    sorteados = []
    for i in range(3):
        sorteados.append(deepcopy(populacao[indices[i]]))
    sorteados.sort(key = operator.attrgetter('custoRota'))
    return([sorteados[0],sorteados[1]])
 
def posCidadeX(x,cromossomo):#retorna qual a posicacao da cidade X na rota
    i = 0
    achou = False
    while i < len(cromossomo.rota) and (not achou):
        if x == cromossomo.rota[i].numeroCidade:
            achou = True
        else:
            i+=1
    return(i) 
 
def cidadeXestaNoCromossomo(x,cromossomo):#verifica se a cidade X já esta no cromossomo, retorna True se encontrou a cidade no cromossomo
    i = 0
    achou = False
    while i < len(cromossomo.rota) and (not achou):
        if x == cromossomo.rota[i].numeroCidade:
            achou = True
        else:
            i+=1
    return(achou)
 
def crossOX(pai1, pai2):
    tamanhoCorte = len(pai1.rota)//3
    rotavazia = []
    verticeVazio = Vertice(None,None,None)
    for i in range(len(pai1.rota)):
        rotavazia.append(deepcopy(verticeVazio))
    filho1 = deepcopy(Solucao(rotavazia, 0))
    filho2 = deepcopy(Solucao(rotavazia, 0))
 
     
    for i in range(tamanhoCorte):
        filho1.rota[i+tamanhoCorte].coordX = deepcopy(pai2.rota[i+tamanhoCorte].coordX)
        filho1.rota[i+tamanhoCorte].coordY = deepcopy(pai2.rota[i+tamanhoCorte].coordY)
        filho1.rota[i+tamanhoCorte].numeroCidade = deepcopy(pai2.rota[i+tamanhoCorte].numeroCidade)
        filho2.rota[i+tamanhoCorte].coordX = deepcopy(pai1.rota[i+tamanhoCorte].coordX)
        filho2.rota[i+tamanhoCorte].coordY = deepcopy(pai1.rota[i+tamanhoCorte].coordY)
        filho2.rota[i+tamanhoCorte].numeroCidade = deepcopy(pai1.rota[i+tamanhoCorte].numeroCidade)
 
    iPai1 = tamanhoCorte*2
    iFilho1 = iPai1
    checaCidade = cidadeXestaNoCromossomo(pai1.rota[iPai1].numeroCidade,filho1)
    while (iFilho1 != tamanhoCorte):
        if(not checaCidade):
            filho1.rota[iFilho1].coordX = deepcopy(pai1.rota[iPai1].coordX)
            filho1.rota[iFilho1].coordY = deepcopy(pai1.rota[iPai1].coordY)
            filho1.rota[iFilho1].numeroCidade = deepcopy(pai1.rota[iPai1].numeroCidade)
            if (iPai1 == len(pai1.rota)-1):
                iPai1 = 0
            else:
                iPai1 +=1
 
            if (iFilho1 == len(pai1.rota)-1):
                iFilho1 = 0
            else:
                iFilho1 +=1
        else:
            if (iPai1 == len(pai1.rota)-1):
                iPai1 = 0
            else:
                iPai1 +=1
        checaCidade = cidadeXestaNoCromossomo(pai1.rota[iPai1].numeroCidade,filho1)
    iPai2 = tamanhoCorte*2
    iFilho2 = iPai2
    checaCidade = cidadeXestaNoCromossomo(pai2.rota[iPai2].numeroCidade,filho2)
    while (iFilho2 != tamanhoCorte):
        if(not checaCidade):
            filho2.rota[iFilho2].coordX = deepcopy(pai2.rota[iPai2].coordX)
            filho2.rota[iFilho2].coordY = deepcopy(pai2.rota[iPai2].coordY)
            filho2.rota[iFilho2].numeroCidade = deepcopy(pai2.rota[iPai2].numeroCidade)
            if (iPai2 == len(pai2.rota)-1):
                iPai2 = 0
            else:
                iPai2 +=1
 
            if (iFilho2 == len(pai2.rota)-1):
                iFilho2 = 0
            else:
                iFilho2 +=1
        else:
            if (iPai2 == len(pai2.rota)-1):
                iPai2 = 0
            else:
                iPai2 +=1
        checaCidade = cidadeXestaNoCromossomo(pai2.rota[iPai2].numeroCidade,filho2)
 
    filho1.calculaCusto()
    filho2.calculaCusto()
    return([filho1,filho2])        
 
def crossPMX(pai1, pai2):
    tamanhoCorte = len(pai1.rota)//3
    rotavazia = []
    verticeVazio = Vertice(None,None,None)
    for i in range(len(pai1.rota)):
        rotavazia.append(deepcopy(verticeVazio))
    filho1 = deepcopy(Solucao(rotavazia, 0))
    filho2 = deepcopy(Solucao(rotavazia, 0))
 
     
    for i in range(tamanhoCorte):
        filho1.rota[i+tamanhoCorte].coordX = deepcopy(pai2.rota[i+tamanhoCorte].coordX)
        filho1.rota[i+tamanhoCorte].coordY = deepcopy(pai2.rota[i+tamanhoCorte].coordY)
        filho1.rota[i+tamanhoCorte].numeroCidade = deepcopy(pai2.rota[i+tamanhoCorte].numeroCidade)
        filho2.rota[i+tamanhoCorte].coordX = deepcopy(pai1.rota[i+tamanhoCorte].coordX)
        filho2.rota[i+tamanhoCorte].coordY = deepcopy(pai1.rota[i+tamanhoCorte].coordY)
        filho2.rota[i+tamanhoCorte].numeroCidade = deepcopy(pai1.rota[i+tamanhoCorte].numeroCidade)
 
    j = 0
    for i in range(len(filho1.rota)):
        if(filho1.rota[i].coordX == None):
            checaCidade =  cidadeXestaNoCromossomo(pai1.rota[i].numeroCidade, filho1)
            if (checaCidade == False):
                filho1.rota[i].coordX = deepcopy(pai1.rota[i].coordX)
                filho1.rota[i].coordY = deepcopy(pai1.rota[i].coordY)
                filho1.rota[i].numeroCidade = deepcopy(pai1.rota[i].numeroCidade)
            else:
                achou = False
                while j < (len(filho1.rota)) and (achou == False):
                    checa = cidadeXestaNoCromossomo(pai1.rota[j].numeroCidade, filho1)
                    if checa:
                        j+=1
                    else:
                        filho1.rota[i].coordX = deepcopy(pai1.rota[j].coordX)
                        filho1.rota[i].coordY = deepcopy(pai1.rota[j].coordY)
                        filho1.rota[i].numeroCidade = deepcopy(pai1.rota[j].numeroCidade)
                        achou = True
 
    j = 0
    for i in range(len(filho2.rota)):
        if(filho2.rota[i].coordX == None):
            checaCidade =  cidadeXestaNoCromossomo(pai2.rota[i].numeroCidade, filho2)
            if (checaCidade == False):
                filho2.rota[i].coordX = deepcopy(pai2.rota[i].coordX)
                filho2.rota[i].coordY = deepcopy(pai2.rota[i].coordY)
                filho2.rota[i].numeroCidade = deepcopy(pai2.rota[i].numeroCidade)
            else:
                achou = False
                while j < (len(filho2.rota)) and (achou == False):
                    checa = cidadeXestaNoCromossomo(pai2.rota[j].numeroCidade, filho2)
                    if checa:
                        j+=1
                    else:
                        filho2.rota[i].coordX = deepcopy(pai2.rota[j].coordX)
                        filho2.rota[i].coordY = deepcopy(pai2.rota[j].coordY)
                        filho2.rota[i].numeroCidade = deepcopy(pai2.rota[j].numeroCidade)
                        achou = True
    filho1.calculaCusto()
    filho2.calculaCusto()
    return([filho1,filho2])
         
 
def mutacao(f1, f2):
 
    tamanho = len(f1.rota)
 
    sorteia = random.randint(1,100)
 
    if sorteia <= taxaMutacao:
 
        cidade1 = random.randint(0,(tamanho-1))
 
        cidade2 = random.randint(0,(tamanho-1))
 
        auX = deepcopy(f1.rota[cidade1].coordX)
 
        auY = deepcopy(f1.rota[cidade1].coordY)
 
        auNumero = deepcopy(f1.rota[cidade1].numeroCidade)
 
        f1.rota[cidade1].coordX = deepcopy(f1.rota[cidade2].coordX)
 
        f1.rota[cidade1].coordY = deepcopy(f1.rota[cidade2].coordY)
 
        f1.rota[cidade1].numeroCidade = deepcopy(f1.rota[cidade2].numeroCidade)
 
        f1.rota[cidade2].coordX = deepcopy(auX)
 
        f1.rota[cidade2].coordY = deepcopy(auY)
 
        f1.rota[cidade2].numeroCidade = deepcopy(auNumero)
 
        f1.calculaCusto()
#        print('mutou')
 
    sorteia = random.randint(1,100)
 
    if sorteia <= taxaMutacao:
 
        cidade1 = random.randint(0,(tamanho-1))
 
        cidade2 = random.randint(0,(tamanho-1))
 
        auX = deepcopy(f2.rota[cidade1].coordX)
 
        auY = deepcopy(f2.rota[cidade1].coordY)
 
        auNumero = deepcopy(f2.rota[cidade1].numeroCidade)
 
        f2.rota[cidade1].coordX = deepcopy(f2.rota[cidade2].coordX)
 
        f2.rota[cidade1].coordY = deepcopy(f2.rota[cidade2].coordY)
 
        f2.rota[cidade1].numeroCidade = deepcopy(f2.rota[cidade2].numeroCidade)
 
        f2.rota[cidade2].coordX = deepcopy(auX)
 
        f2.rota[cidade2].coordY = deepcopy(auY)
 
        f2.rota[cidade2].numeroCidade = deepcopy(auNumero)
 
        f2.calculaCusto()
#        #print('mutou')
 
 
    return([f1,f2])
         
 
def atualiza(populacao,f1,f2):
    populacao.append(deepcopy(f1))
    populacao.append(deepcopy(f2))
    populacao.sort(key = operator.attrgetter('custoRota'))
    populacao.pop()
    populacao.pop()
 
 
listaSolucoesIniciais = geraNSolucoes(quantidadeSolucaoInicial)
listaSolucoesIniciais.sort(key = operator.attrgetter('custoRota'))
 
print()
print('#####RESULTADOS#####')
print()
print('Menor custo solução gulosa =', listaSolucoesIniciais[0].custoRota)
 
 
 
 
if operadorCross == 0:
    for i in range(10000):#loop
        sorteados = deepcopy(torneio(listaSolucoesIniciais))
        filhos = deepcopy(crossOX(sorteados[0],sorteados[1]))
        mutados = deepcopy(mutacao(filhos[0],filhos[1]))
        atualiza(listaSolucoesIniciais,mutados[0],mutados[1])
elif operadorCross == 1:
    for i in range(10000):#loop
        sorteados = deepcopy(torneio(listaSolucoesIniciais))
        filhos = deepcopy(crossPMX(sorteados[0],sorteados[1]))
        mutados = deepcopy(mutacao(filhos[0],filhos[1]))
        atualiza(listaSolucoesIniciais,mutados[0],mutados[1])    
  
print('Menor custo algoritmo genético =', listaSolucoesIniciais[0].custoRota)
print()
 
if (mostrarRota):
    print('Melhor rota encontrada: ')
    for i in range (len(listaSolucoesIniciais[0].rota)):
        print(listaSolucoesIniciais[0].rota[i].numeroCidade)
    print(listaSolucoesIniciais[0].rota[0].numeroCidade)
