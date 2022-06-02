from Entities import Node, Edge
import json
from pyvis.network import Network
from itertools import combinations


class Graph:
    def __init__(self, name: str):
        self.name = name
        self.nodes = []
        self.edges = []
        self.matrix = self.matrixUpdate()

    def add_node(self, label, *args):
        labels = list(map(lambda x: x.label, self.nodes))
        try:
            assert label not in labels
        except AssertionError:
            print("Already exist node with such name")
            raise SystemExit
        self.nodes.append(Node(label, *args))
        self.matrix = self.matrixUpdate()

    def add_edge(self, first, second, *args):
        labels = list(map(lambda x: x.label, self.nodes))
        try:
            assert first in labels and second in labels
        except AssertionError:
            print("There's no node with such name")
            raise SystemExit
        for node in self.nodes:
            if node.label == first:
                first = node
                break
        for node in self.nodes:
            if node.label == second:
                second = node
                break
        self.edges.append(Edge(first, second, *args))
        self.matrix = self.matrixUpdate()

    def del_node(self, label: str):
        for i, node in enumerate(self.nodes):
            if label == node.label:
                to_del = []
                for j, edge in enumerate(self.edges):
                    checkEdge = edge.getNodes()
                    if label == checkEdge[0].label or label == checkEdge[1].label:
                        to_del.append(edge)
                for k in to_del:
                    self.edges.remove(k)
                del self.nodes[i]
                break

    def del_edge(self, first: str, second: str):
        for i, edge in enumerate(self.edges):
            edge = edge.getNodes()
            if first == edge[0].label and second == edge[1].label:
                del self.edges[i]
                break

    def node_degree(self, label: str) -> int:
        for i, node in enumerate(self.nodes):
            if label == node.label:
                degree = 0
                for j, edge in enumerate(self.edges):
                    checkEdge = edge.getNodes()
                    if label == checkEdge[0].label or label == checkEdge[1].label:
                        degree += 1
                return degree

    def nodes_degrees(self) -> list:
        labels = list(map(lambda x: x.label, self.nodes))
        rez = []
        for i in labels:
            rez.append((i, self.node_degree(i)))
        return rez

    def get_graph_info(self):
        labels = list(map(lambda x: x.label, self.nodes))
        edges = list(map(lambda x: (x.getNodes()[0].label, x.getNodes()[1].label, x.isOriented), self.edges))
        return labels, edges

    def save(self, savePath: str):
        net = Network("650px", "1500px", heading=self.name)
        for node in self.nodes:
            net.add_node(node.label, label=node.label, color=node.color, shape=node.shape)
        for edge in self.edges:
            net.directed = edge.isOriented
            net.add_edge(edge.first.label, edge.second.label, color=edge.color, label=edge.label)
        net.save_graph(f"{self.name}.html")

    def load(self, loadPath: str):
        self.nodes = []
        self.edges = []
        with open(loadPath, "r") as file:
            info = file.read()
        nodeStart = info.find("nodes = new vis.DataSet([") + 24
        edgeStart = info.find("edges = new vis.DataSet([") + 24
        end = info.rfind("]);")
        nodeInfo = json.loads(info[nodeStart: edgeStart - 35])
        edgeInfo = json.loads(info[edgeStart: end + 1])
        for record in nodeInfo:
            self.add_node(record["label"], record["color"], record["shape"])
        for record in edgeInfo:
            arrow = False
            if record.get("arrows"):
                arrow = True
            self.add_edge(record["from"], record["to"], arrow, record["color"], record["label"])

    def matrixUpdate(self):
        matrix = []
        for fNode in self.nodes:
            row = []
            for sNode in self.nodes:
                isEdgeExist = 0
                for edge in self.edges:
                    if edge.isOriented:
                        if (fNode, sNode) == edge.getNodes():
                            isEdgeExist = 1
                    else:
                        if (fNode, sNode) == edge.getNodes() or (sNode, fNode) == edge.getNodes():
                            isEdgeExist = 1
                row.append(isEdgeExist)
            matrix.append(row)
        return matrix

    def __orientToNoerient(self):
        matrix = self.matrixUpdate()
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if matrix[i][j] == 1:
                    matrix[j][i] = 1
        return matrix

    def isConnected(self):
        matrix = self.matrixUpdate()
        queue = []
        visit = [0] * len(matrix)
        queue.append(0)
        visit[0] = 1
        while len(queue) > 0:
            v = queue[0]
            queue = queue[1:]
            for i in range(len(matrix)):
                if matrix[v][i] == 1 and visit[i] == 0:
                    visit[i] = 1
                    queue.append(i)
        if 0 in visit:
            return False
        return True

    def isEuler(self):
        if not self.isConnected():
            return False
        matrix = self.matrixUpdate()
        for i in range(len(matrix)):
            counter = 0
            for j in range(len(matrix)):
                if matrix[i][j] == 1 and matrix[j][i] != 1:
                    print("Graph must be not oriented")
                    raise SystemExit
                elif matrix[i][j] == 1:
                    counter += 1
            if counter % 2 == 1:
                return False
        return True

    def __getEdges(self):
        matrix = self.matrixUpdate()
        edges = []
        for i in range(len(matrix)):
            for j in range(i, len(matrix)):
                if matrix[i][j] == 1:
                    edges.append((i, j))
        return edges

    def printEulerCycle(self):
        matrix = self.matrixUpdate()
        edges = self.__getEdges()
        stack = []
        stack.append(0)
        while len(stack) > 0:
            w = stack[-1]
            found_edge = False
            for u in range(len(matrix)):
                if (w, u) in edges or (u, w) in edges:
                    stack.append(u)
                    if (w, u) in edges:
                        edges.remove((w, u))
                    else:
                        edges.remove((u, w))
                    found_edge = True
                    break
            if not found_edge:
                stack = stack[:-1]
                print(self.nodes[w].label, end=' ')
                if len(stack) > 0:
                    print('->', end=' ')

    def isPlanar(self):
        self.matrix = self.matrixUpdate()
        for star in combinations([i for i in range(len(self.matrix))], 5):
            if self.__isStar(*star):
                return False
        for bipart in combinations([i for i in range(len(self.matrix))], 6):
            if self.__isBipartite(*bipart):
                return False
        return True

    def __isStar(self, *args):
        nodes = args
        if len(nodes) != 5:
            return False
        for fNode in nodes:
            for sNode in nodes:
                if fNode == sNode:
                    continue
                if self.matrix[fNode][sNode] != 1:
                    return False
        return True

    def __isBipartite(self, *args):
        nodes = args
        if len(nodes) != 6:
            return False
        part1 = []
        part2 = []
        fNode = nodes[0]
        part1.append(fNode)
        for sNode in nodes:
            if fNode == sNode:
                continue
            if self.matrix[fNode][sNode] == 1:
                part2.append(sNode)
            else:
                part1.append(sNode)
        if len(part1) != 3 or len(part2) != 3:
            return False

        for fNode in part1:
            for sNode in part1:
                if fNode == sNode:
                    continue
                if self.matrix[fNode][sNode] == 1:
                    return False

        for fNode in part2:
            for sNode in part2:
                if fNode == sNode:
                    continue
                if self.matrix[fNode][sNode] == 1:
                    return False
        return True

    def printMatrix(self):
        self.matrix = self.matrixUpdate()
        for row in self.matrix:
            for b in row:
                print(b, end=' ')
            print()

    def toPlanar(self):
        self.matrix = self.matrixUpdate()
        while not self.isPlanar():
            sortDegree = sorted(self.__nodesCounter().items(), key=lambda x: x[1])[::-1]
            v = sortDegree[0][0]
            for u in range(len(self.matrix)):
                if self.matrix[u][v] == 1:
                    self.matrix[u][v] = 0
                    if 1 not in self.matrix[u]:
                        self.matrix[u][v] = 1
                        continue
                    else:
                        self.del_edge(self.nodes[u].label, self.nodes[v].label)
                        self.del_edge(self.nodes[v].label, self.nodes[u].label)
                        break


    def __nodesCounter(self):
        degrees = {}
        for i, fNode in enumerate(self.nodes):
            degrees.update({i: self.node_degree(fNode.label)})
        return degrees

    def __getSearchNumber(self, v, setTree):
        for i, Set in enumerate(setTree):
            if v in Set:
                return i
        return -1

    def toTree(self):
        edges = self.__getEdges()
        newEdges = []
        setTree = []
        for edge in edges:
            firstNum = self.__getSearchNumber(edge[0], setTree)
            secondNum = self.__getSearchNumber(edge[1], setTree)
            if firstNum == secondNum == -1:
                setTree.append([edge[0], edge[1]])
                newEdges.append(edge)
                continue

            if firstNum == -1:
                setTree[secondNum].append(edge[0])
                newEdges.append(edge)
                continue

            if secondNum == -1:
                setTree[firstNum].append(edge[1])
                newEdges.append(edge)
                continue

            if firstNum != secondNum:
                setTree[firstNum] = [*setTree[firstNum], *setTree[secondNum]]
                del setTree[secondNum]
                newEdges.append(edge)
                continue

        for edge in edges:
            if edge not in newEdges:
                self.del_edge(self.nodes[edge[0]].label, self.nodes[edge[1]].label)
                self.del_edge(self.nodes[edge[1]].label, self.nodes[edge[0]].label)

    def getLength(self, v1: str, v2: str):
        fNode = sNode = -1
        for i, v in enumerate(self.nodes):
            if v.label == v1:
                fNode = i
            if v.label == v2:
                sNode = i

        matrix = self.matrixUpdate()
        length = 0
        queue = []
        visit = [0] * len(matrix)
        queue.append(fNode)
        visit[fNode] = 1
        while len(queue) > 0:
            v = queue[0]
            queue = queue[1:]
            length += 1
            for i in range(len(matrix)):
                if matrix[v][i] == 1 and visit[i] == 0:
                    visit[i] = 1
                    queue.append(i)
                    if i == sNode:
                        return length
        return -1




