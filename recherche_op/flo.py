import networkx as nx
import matplotlib.pyplot as plt


def getMinFlow(mat, tmpPath):
    return min([mat[tmpPath[i]][tmpPath[i+1]] for i in range(len(tmpPath)-1)])


def updateMat(mat, tmpPath, tmpFlow):
    for i in range(len(tmpPath)-1):
        mat[tmpPath[i]][tmpPath[i+1]] -= tmpFlow
        mat[tmpPath[i+1]][tmpPath[i]] += tmpFlow


def getOnePath(mat):
    """
    Algorithme de recherche de chemin
    """
    visited = [False for i in range(len(mat))]
    visited[0] = True
    tmpPath = [0]
    while tmpPath:
        tmp = tmpPath[-1]
        if tmp == len(mat)-1:
            return tmpPath
        for i in range(len(mat)):
            if mat[tmp][i] > 0 and not visited[i]:
                tmpPath.append(i)
                visited[i] = True
                break
        else:
            tmpPath.pop()
    return None


def getFlow(mat):
    maxFlow = 0
    tmpPath = getOnePath(mat)
    while tmpPath is not None:
        tmpFlow = getMinFlow(mat, tmpPath)
        maxFlow += tmpFlow
        updateMat(mat, tmpPath, tmpFlow)
        tmpPath = getOnePath(mat)
    return maxFlow, mat


def show_graph_with_capacities(g, mat):
    for i in range(len(mat)):
        for j in range(len(mat)):
            if mat[i][j] > 0:
                G.add_edge(i, j, capacity=mat[i][j])
    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True)
    edge_labels = nx.get_edge_attributes(G, 'capacity')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    return G


if __name__ == "__main__":
    """
    Algorithme de Ford-Fulkerson
    """
    mat = [[0, 6, 8, 0, 0, 0],
           [0, 0, 0, 6, 3, 0],
           [0, 0, 0, 3, 3, 0],
           [0, 0, 0, 0, 0, 8],
           [0, 0, 0, 0, 0, 6],
           [0, 0, 0, 0, 0, 0]]
    flow, mat = getFlow(mat)
    G = nx.DiGraph()
    show_graph_with_capacities(G, mat)
    plt.show()
