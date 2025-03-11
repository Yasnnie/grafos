import csv
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, value):
        self.value = value
        self.prox = None

class List:
    def __init__(self):
        self.cab = None
        self.last = None

    def add_last(self, new_node):
        if self.cab is None:
            self.cab = new_node
            self.last = new_node
        else:
            self.last.prox = new_node
            self.last = new_node

    def print_nodes(self):
        text = f"| {self.cab.value} |"
        aux = self.cab.prox
        while aux:
            text += f" -> {aux.value}"
            aux = aux.prox
        print(text)

class Grafo:
    def __init__(self):
        self.adj = []
        self.pesos = {}

    def searc_index_vertice(self, vertice):
        for i in range(len(self.adj)):
            if vertice == self.adj[i].cab.value:
                return i
        return None

    def add_vertice(self, v):
        if self.searc_index_vertice(v.value) is None:
            lista = List()
            lista.cab = v
            lista.last = v
            self.adj.append(lista)

    def add_aresta(self, v1, v2, peso):
        idx_v1 = self.searc_index_vertice(v1.value)
        idx_v2 = self.searc_index_vertice(v2.value)

        if idx_v1 is not None and idx_v2 is not None:
            self.adj[idx_v1].add_last(Node(v2.value))
            self.adj[idx_v2].add_last(Node(v1.value))
            self.pesos[(v1.value, v2.value)] = peso
            self.pesos[(v2.value, v1.value)] = peso

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
                    self.melhor_caminho = caminho_atual[:]
        else:
            index = self.grafo.searc_index_vertice(atual)
            if index is not None:
                aux = self.grafo.adj[index].cab.prox
                while aux:
                    if aux.value not in cidades_visitadas:
                        peso_aresta = self.grafo.pesos.get((atual, aux.value))
                        self.tsp_dfs(origem, aux.value, cidades_visitadas, custo_atual + peso_aresta, caminho_atual)
                    aux = aux.prox

        cidades_visitadas.remove(atual)
        caminho_atual.pop()

    def iniciar_busca(self, origem):
        self.tsp_dfs(origem, origem)
        print("Melhor caminho encontrado:", self.melhor_caminho)
        print("Custo do melhor caminho:", self.melhor_custo)

    def exibir_grafo_tsp(self):
        G = nx.Graph()
        for (v1, v2), peso in self.grafo.pesos.items():
            G.add_edge(v1, v2, weight=peso)

        pos = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G, 'weight')
        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, edge_color='gray')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
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
                n1 = Node(v1)
                n2 = Node(v2)
                grafo.add_vertice(n1)
                grafo.add_vertice(n2)
                grafo.add_aresta(n1, n2, peso)

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
            grafo.add_vertice(Node(v))
        elif opcao == '2':
            v1 = input("Digite o primeiro vértice: ")
            v2 = input("Digite o segundo vértice: ")
            peso = int(input("Digite o peso da aresta: "))
            grafo.add_aresta(Node(v1), Node(v2), peso)
        elif opcao == '3':
            for lista in grafo.adj:
                lista.print_nodes()
        elif opcao == '4':
            origem = input("Digite o vértice de origem: ")
            solver = TPS(grafo)
            solver.iniciar_busca(origem)
        elif opcao == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    interface()
