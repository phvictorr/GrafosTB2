from csv import reader
from operator import index

from numpy import double

class Network:
    def __init__(self, num_vert=0, num_arestas=0, mat_adj=None, size_v=None, capacidade=None):
        self.num_vert = num_vert
        self.num_arestas = num_arestas
        self.lista_professores = []
        self.lista_disciplinas = []
        self.demanda = []
        self.dict = {}
            
        if mat_adj is None:
            self.mat_adj = [[0 for j in range(num_vert)] for i in range(num_vert)]
        else:
            self.mat_adj = mat_adj
            
        if capacidade is None:
            self.capacidade = [[0 for j in range(num_vert)] for i in range(num_vert)]
    
    def add_aresta(self, u, v, c, w=1):
        """Adiciona aresta de u a v com peso w"""
        if u < self.num_vert and v < self.num_vert:
            self.num_arestas.append((u,v,w,c))
            self.mat_adj[u][v] = w
            self.capacidade[u][v] = c
        else:
            print("Aresta invalida!")

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
        proxima_chave = 0
        
        #Mapeando nome dos professores
        for i in range(tamanho_professores):
            self.adiciona_dict(self.lista_professores[i][0], i)
            proxima_chave = i+1
        
        #Envia proxima_chave com valor de i
        
        #Mapeando cursos
        for i in range(tamanho_disciplinas):
            if self.lista_disciplinas[i][0] != None:
                self.adiciona_dict(self.lista_disciplinas[i][0], proxima_chave)
                proxima_chave = proxima_chave+1
        
        #Mapeando disciplinas dos cursos
        for i in range(tamanho_disciplinas):
            if self.lista_disciplinas[i][1] != None:
                self.adiciona_dict(self.lista_disciplinas[i][1], proxima_chave)
                proxima_chave = proxima_chave+1
        
        print('Dicionário: ', self.dict)
    
    def bellman_ford(self, s, t):
        dist = [float("inf") for _ in range(self.size_v)]  # Distance from s
        pred = [None for _ in range(self.size_v)]  # Predecessor in shortest path from s
        dist[s] = 0
        for it in range(self.size_v):
            updated = False
            for (u, v, w) in self.edge_list:
                if dist[v] > dist[u] + w:
                    dist[v] = dist[u] + w
                    pred[v] = u
                    updated = True
            if not updated:
                return dist, pred
        return dist, 

    
    def executar_scm(self, w, c, b, s, t):
        F = [[0 for i in range(len(G))] for i in range(leng(G))]
        C = bellman_ford(self, s, t)
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
                    E.remove((u,v,w[u][v]))
                if G[v][u] == 0:
                    G[v][u] = 1
                    E.append((v,u,-w[u][v]))
                    w[v][u] = -w[u][v]
            C = bellman_ford(self, s, t)
