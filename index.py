class Node:
    def __init__(self, value):
        self.value = value
        self.prox = None

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
        self.numero_vertice = 0
        self.numero_aresta = 0
        self.adj = []
    

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
            
    
    def exibir_grafo(self):
        for li in self.adj:
            li.print_nodes()



grafo = Grafo()

v1 = Node("v1")
v2 = Node("v2")
v3 = Node("v3")


grafo.add_vertice(v1)
grafo.add_vertice(v1)
grafo.add_vertice(v2)
grafo.add_vertice(v3)


grafo.add_aresta(v1,v2)
grafo.add_aresta(v2,v3)
grafo.add_aresta(v3,v1)
grafo.exibir_grafo()
