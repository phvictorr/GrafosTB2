import network

g = network.Network()
g.ler_arquivo_professores("professores.csv")
g.ler_arquivo_disciplinas("disciplinas.csv")
g.criar_rede()