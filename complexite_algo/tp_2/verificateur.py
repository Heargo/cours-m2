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
            if (link[0] not in self._graph):
                self._graph[link[0]] = [link[1]]
            else:
                if (link[1] not in self._graph[link[0]]):
                    self._graph[link[0]].append(link[1])

        print(self._graph)


def verifyGraph(graph, coloration):
    colored_correctly = True

    for i in range(len(graph)):
        for j in range(len(graph)):
            if graph[i][j] == 1 and coloration[i] == coloration[j]:
                colored_correctly = False
                break

    return colored_correctly


def construct_verification_graph(graph):
    verification_graph = []

    for i in range(len(graph)):
        verification_graph.append([])
        for j in range(len(graph)):
            if graph[i][j] == 1 and coloration[i] != coloration[j]:
                verification_graph[i].append(1)
            else:
                verification_graph[i].append(0)

    return verification_graph
