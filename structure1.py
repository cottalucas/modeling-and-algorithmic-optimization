class Vertice:
    matriz = []
    f = None
    g = None
    h = None
    Pai = None #não há ponteiros em python, somente referências
     
     
    def __init__(self, matriz, f, g, h, Pai):
        self.matriz = matriz
        self.f = f
        self.g = g
        self.h = h
        self.Pai = Pai
        print ("Objeto Vértice Estanciado!") 
