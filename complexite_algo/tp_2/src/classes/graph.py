class Graph():
    def __init__(self, file):
        self._graph = {}

        # open file
        with open(file, "r") as f:
            content = f.readlines()

        # split by lines
        content = [x.strip() for x in content]
        # remove comments
        content = [x for x in content if x[0] != 'c']
        # remove empty lines
        content = [x for x in content if x != '']
        # split by edges
        content = [x.split() for x in content if x[0] == 'e']
        # remove 'e'
        content = [[x[1], x[2]] for x in content]

        for link in content:
            self.link(link[0], link[1])
            self.link(link[1], link[0])

    def get_voisin(self, i):
        return self._graph.get(i)

    def link(self, node_1, node_2):
        if (node_1 not in self._graph):
            self._graph[node_1] = [node_2]
        else:
            if (node_2 not in self._graph[node_1]):
                self._graph[node_1].append(node_2)

    def get_graph(self):
        return self._graph

    def get_nb_sommets(self):
        return len(self.get_graph().keys())

    def inverse(self):
        nodes = list(self._graph.keys())
        graph_tmp = {}
        for node in nodes:
            if (node not in graph_tmp):
                graph_tmp[node] = []
                for n2 in nodes:
                    if (n2 not in self.get_voisin(node) and n2 != node):
                        graph_tmp[node].append(n2)

        self._graph = graph_tmp
