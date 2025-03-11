import csv
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, value):
        self.value = value


class List:
    def __init__(self):
        self.cab = None
        self.last = None

    def add_last(self, new_value):
        self.last.prox = new_value
        self.last = new_value

    def print_nodes(self):
        text = f"| {self.cab.value} |"

        aux = self.cab.prox

        while aux != None:
            text = text + f" -> {aux.value}"
            aux = aux.prox

        print(text)



class Grafo:
    def __init__(self):
        self.adj = []

        self.pesos = {}
    def searc_index_vertice(self, vertice):
        exist = None

        for i in range(len(self.adj)):
            if vertice == self.adj[i].cab:
                exist = i 
                break

        return exist


    def add_vertice(self, v):
        if len(self.adj) == 0:
            lista = List()
            lista.cab = v
            lista.last = v
            self.adj.append(lista)
            print("Adicionado com sucesso")
            return

        exist_vertice = self.searc_index_vertice(v)

        if exist_vertice == None:
            lista = List()
            lista.cab = v
            lista.last = v
            self.adj.append(lista)
            print("Adicionado com sucesso")
        else:
            print("Vertice já existe")


    def add_aresta(self, v1, v2):

        exist_v1 = self.searc_index_vertice(v1)
        exist_v2 = self.searc_index_vertice(v2)

        print(f"valor {v1.value} no index {exist_v1}")
        print(f"valor {v2.value} no index {exist_v2}")

    
        if exist_v1 != None and exist_v2 != None:
            new_v1 = Node(v1.value)
            new_v2 = Node(v2.value)
            print("======= Cheguei ========")
            self.adj[exist_v1].add_last(new_v2)
            self.adj[exist_v2].add_last(new_v1)
            self.pesos[(v1.value, v2)] = peso
            self.pesos[(v2.value, v1)] = peso


    def exibir_grafo(self):
        for vertice, vizinhos in self.adj.items():
            print(f"{vertice} -> {', '.join(vizinhos)}")


class TPS:
    def __init__(self, grafo):
        self.grafo = grafo
        self.melhor_custo = float('inf')
        self.melhor_caminho = []

    def tsp_dfs(self, origem, atual, cidades_visitadas=None, custo_atual=0, caminho_atual=None):
        if cidades_visitadas is None:
            cidades_visitadas = set()
        if caminho_atual is None:
            caminho_atual = []

        cidades_visitadas.add(atual)
        caminho_atual.append(atual)

        if len(cidades_visitadas) == len(self.grafo.adj):
            if (atual, origem) in self.grafo.pesos:
                custo_total = custo_atual + self.grafo.pesos[(atual, origem)]
                if custo_total < self.melhor_custo:
                    self.melhor_custo = custo_total
                    self.melhor_caminho = caminho_atual[:] + [origem]
        else:
            for vizinho in self.grafo.adj[atual]:
                if vizinho not in cidades_visitadas:
                    self.tsp_dfs(origem, vizinho, cidades_visitadas, custo_atual + self.grafo.pesos[(atual, vizinho)], caminho_atual)

        cidades_visitadas.remove(atual)
        caminho_atual.pop()

    def iniciar_busca(self, origem):
        self.melhor_custo = float('inf')
        self.melhor_caminho = []
        self.tsp_dfs(origem, origem)
        print("Melhor caminho encontrado:", self.melhor_caminho)
        print("Custo do melhor caminho:", self.melhor_custo)
        self.exibir_grafo_tsp()

    def exibir_grafo_tsp(self):
        G = nx.Graph()
        
        for v1, v2 in self.grafo.pesos.keys():
            G.add_edge(v1, v2, weight=self.grafo.pesos[(v1, v2)])

        pos = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G, 'weight')
        
        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, edge_color='gray')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        
        if self.melhor_caminho:
            path_edges = list(zip(self.melhor_caminho, self.melhor_caminho[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
        
        plt.title("Melhor Caminho Encontrado pelo TSP")
        plt.show()


def carregar_csv(nome_arquivo, grafo):
    with open(nome_arquivo, newline='', encoding='utf-8') as csvfile:
        leitor = csv.reader(csvfile)
        next(leitor)
        for linha in leitor:
            if len(linha) == 3:
                v1, v2, peso = linha
                peso = int(peso)
                grafo.add_vertice(v1)
                grafo.add_vertice(v2)
                grafo.add_aresta(v1, v2, peso)

def interface():
    grafo = Grafo()
    carregar_csv('csv/grafos2.csv', grafo)

    while True:
        print("\n1. Adicionar Vértice")
        print("2. Adicionar Aresta")
        print("3. Exibir Grafo")
        print("4. Resolver TSP")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            v = input("Digite o nome do vértice: ")
            grafo.add_vertice(v)
        elif opcao == '2':
            v1 = input("Digite o primeiro vértice: ")
            v2 = input("Digite o segundo vértice: ")
            peso = int(input("Digite o peso da aresta: "))
            grafo.add_aresta(v1, v2, peso)
        elif opcao == '3':
            grafo.exibir_grafo()
        elif opcao == '4':
            origem = input("Digite o vértice de origem: ")
            if origem in grafo.adj:
                solver = TPS(grafo)
                solver.iniciar_busca(origem)
            else:
                print("Vértice não encontrado.")
        elif opcao == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    interface()
