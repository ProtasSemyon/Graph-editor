from Entities import Node, Edge
import json
from pyvis.network import Network
class Graph:
    def __init__(self, name: str):
        self.name = name
        self.nodes = []
        self.edges = []

    def add_node(self, label, *args):
        labels = list(map(lambda x: x.label, self.nodes))
        try:
            assert label not in labels
        except AssertionError:
            print("Already exist node with such name")
            raise SystemExit
        self.nodes.append(Node(label, *args))

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
        edges = list(map(lambda x: (x.getNodes()[0].label,x.getNodes()[1].label, x.isOriented), self.edges))
        return labels, edges
    
    def save(self, savePath: str):
        net = Network("650px", "1500px", heading = self.name)
        for node in self.nodes:
            net.add_node(node.label, label = node.label, color = node.color, shape = node.shape)
        for edge in self.edges:
            net.directed = edge.isOriented
            net.add_edge(edge.first.label, edge.second.label, color = edge.color, label = edge.label)
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
    