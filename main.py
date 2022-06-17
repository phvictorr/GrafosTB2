import network

g = network.Network()
g.ler_arquivo_professores("professores_toy.csv")
g.ler_arquivo_disciplinas("disciplinas_toy.csv")
g.criar_rede()