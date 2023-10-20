
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
