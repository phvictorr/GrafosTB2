from csv import reader
from operator import index
from tkinter import W

from numpy import double, ubyte

class Network:
    def __init__(self, num_vert=0, num_arestas=0, mat_adj=None, lista_adj=None, mat_capacidade=None, mat_c=None,demanda=None):
        self.num_vert = num_vert
        self.num_arestas = num_arestas
        self.lista_professores = []
        self.lista_disciplinas = []
        self.dict = {}
            
        if mat_adj is None:
            self.mat_adj = [[0 for i in range(num_vert)] for j in range(num_vert)]
        else:
            self.mat_adj = mat_adj
            
        if mat_capacidade is None:
            self.mat_capacidade = [[0 for i in range(num_vert)] for j in range(num_vert)]
        else:
            self.mat_capacidade = mat_capacidade
        
        if mat_c is None:
            self.mat_c = [[0 for i in range(num_vert)] for j in range(num_vert)]
        else:
            self.mat_c = mat_c
            
        if lista_adj is None:
            self.list_adj = [[] for i in range(num_vert)]
        else:
            self.list_adj = lista_adj
        
        if demanda is None:
            self.demanda = [[] for i in range(num_vert)]
        else:
            self.demanda = demanda
    
    def add_aresta(self, u, v, w, c):
        self.mat_adj[u][v] = [w, c]
        self.mat_capacidade[u][v] = c
        self.mat_c[u][v] = w

    def remove_aresta(self, u, v):
        """Remove aresta de u a v, se houver"""
        if u < self.num_vert and v < self.num_vert:
            if self.mat_adj[u][v] != 0:
                self.num_arestas += 1
                self.mat_adj[u][v] = 0
                for (v2, w2) in self.lista_adj[u]:
                    if v2 == v:
                        self.lista_adj[u].remove((v2, w2))
                        break
            else:
                print("Aresta inexistente!")
        else:
            print("Aresta invalida!")
    
    #Lendo arquivo professores com biblioteca "csv/reader"
    def ler_arquivo_professores(self, nome_arq):
        try:
            with open(nome_arq, 'r') as csv_file:
                
                csv_reader = reader(csv_file, delimiter=';')
                next(csv_reader) #Pula cabeçalho
                self.lista_professores = list(csv_reader)
                print('\nVetor de professores: \n', self.lista_professores)
        except IOError:
            print("Nao foi possivel encontrar ou ler o arquivo!")
            return False
        
    def ler_arquivo_disciplinas(self, nome_arq):
        try:
            with open(nome_arq, 'r') as csv_file:
                csv_reader = reader(csv_file, delimiter=';')
                next(csv_reader) #Pula cabeçalho
                self.lista_disciplinas = list(csv_reader)
                print('\nVetor de disciplinas: \n', self.lista_disciplinas)
        except IOError:
            print("Nao foi possivel encontrar ou ler o arquivo!")
            return False  

    def adiciona_dict(self, valor, chave):
        self.dict[valor] = chave
    
    def criar_rede(self):
        tamanho_professores = len(self.lista_professores) #Guarda tamanho da lista de professores
        tamanho_disciplinas = len(self.lista_disciplinas) #Guarda tamanho da lista de disciplinas
        proxima_chave = 1
        
         # ------------------------------------------------------------------------#
        
        #Mapeando nome dos professores
        for i in range(tamanho_professores):
            self.adiciona_dict(self.lista_professores[i][0], i)
            proxima_chave = i+1
        
        #Envia proxima_chave com valor de i
        
        #Mapeando cursos e disciplinas
        for i in range(tamanho_disciplinas):
            if self.lista_disciplinas[i][0] != None:
                self.adiciona_dict(self.lista_disciplinas[i][0], proxima_chave)
                self.adiciona_dict(self.lista_disciplinas[i][1], proxima_chave)
                proxima_chave = proxima_chave+1
        
        print('\nDicionário: ', self.dict)
        
        #Capturando o tamanho de vértices em relação ao dicionário
        self.num_vert = len(self.dict)
        
        #Preenchendo matrizes
        self.mat_adj = [[0 for i in range((tamanho_disciplinas+tamanho_professores)+2)] for j in range((tamanho_disciplinas+tamanho_professores)+2)]
        self.mat_c = [[0 for i in range((tamanho_disciplinas+tamanho_professores)+2)] for j in range((tamanho_disciplinas+tamanho_professores)+2)]
        self.mat_capacidade = [[0 for i in range((tamanho_disciplinas+tamanho_professores)+2)] for j in range((tamanho_disciplinas+tamanho_professores)+2)]
        
        # ------------------------------------------------------------------------#
        
        #Somatório número de turmas
        contador_turmas = 0
        for i in range(tamanho_disciplinas):
            contador_turmas = contador_turmas + int(self.lista_disciplinas[i][2])
        
        #print(self.dict[self.lista_disciplinas[1][1]])
        
        #Super oferta -> GF e BM
        for i in range((tamanho_professores)-1):
            self.add_aresta(0, self.dict[self.lista_professores[i][0]], self.lista_professores[i][1], self.lista_professores[i][1])
            
        #Professores até disciplinas (por ordem de preferência)
        
        for i in range((tamanho_disciplinas)-1):
            contador = 2
            for j in range(5):
                match contador:
                    case 2: #1
                        self.add_aresta(self.dict[self.lista_professores[i][0]], self.dict[self.lista_disciplinas[i][contador]], 0, 'inf')
                    case 3: #2
                        self.add_aresta(self.dict[self.lista_professores[i][0]], self.dict[self.lista_disciplinas[i][contador]], 3, 'inf')
                    case 4: #3
                        self.add_aresta(self.dict[self.lista_professores[i][0]], self.dict[self.lista_disciplinas[i][contador]], 5, 'inf')
                    case 5: #4
                        self.add_aresta(self.dict[self.lista_professores[i][0]], self.dict[self.lista_disciplinas[i][contador]], 8, 'inf')
                    case 6: #5
                        self.add_aresta(self.dict[self.lista_professores[i][0]], self.dict[self.lista_disciplinas[i][contador]], 10, 'inf')
                contador += 1
            
        # for i in range((tamanho_disciplinas)-1):
        #     self.add_aresta(self.dict[self.lista_professores[i][0]], self.dict[self.lista_disciplinas[i][0]], 0, 'inf')
        
        #Disciplinas até Super-demanda
        
        for i in range((tamanho_disciplinas)-1):
            self.add_aresta(self.dict[self.lista_disciplinas[i][0]], 3, self.lista_disciplinas[i][2], self.lista_disciplinas[i][2])
        
        print("Matriz de adjacências: \n\n--------------------")    
        for i in range(len(self.mat_adj)):
            for j in range(len(self.mat_adj[i])):
                print(self.mat_adj[i][j], end=" ")
            print("\n")
        print("--------------------\n")
        #print(self.mat_adj)
        
        self.bellman_ford(self, 0, 5)
        self.executar_scm(self, self.mat_capacidade, self.list_adj, 0, 5)
    
    def bellman_ford(self, s, t):
        dist = [float("inf") for _ in range(self.num_vert)]
        pred = [None for _ in range(self.num_vert)]
        dist[s] = 0
        for it in range(self.num_vert):
            updated = False
            for (u, v, w) in self.mat_adj:
                if dist[v] > dist[u] + w:
                    dist[v] = dist[u] + w
                    pred[v] = u
                    updated = True
            if not updated:
                return dist, pred
        return dist, 

    
    def executar_scm(self, w, c, b, s, t):
        F = [[0 for i in range(len(self))] for i in range(len(self))]
        C = self.bellman_ford(self, s, t)
        while len(C) != 0 and b[s] != 0:
            f = float('inf')
            for i in range(1, len(C)):
                u = C[i-1]
                v = C[i]
                if c[u][v] < f:
                    f = c[u][v]
            for i in range(1, len(C)):
                u = C[i-1]
                v = C[i]
                F[u][v] += f
                c[u][v] -= f
                c[v][u] += f
                b[s] -= f
                b[t] += f
                if c[u][v] == 0:
                    G[u][v] = 0
                    self.remove_aresta((u,v,w[u][v]))
                if self[v][u] == 0:
                    self[v][u] = 1
                    self.mat_adj.append((v,u,-w[u][v]))
                    w[v][u] = -w[u][v]
            C = self.bellman_ford(self, s, t)
