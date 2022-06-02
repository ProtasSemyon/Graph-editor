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
        self.edges.append(Edge(first, second, *args))

    def del_node(self, label: str):
        pass
    
    def del_edge(self, first: str, second: str):
        pass

    def node_degree(self, label: str) -> int:
        return 0
    
    def nodes_degree(self) -> tuple[int]:
        return (0)
    
    def get_graph_info(self) -> tuple[int]:
        '''return number of nodes and edges'''
        return (len(self.nodes), len(self.edges))
    
    def save(self, savePath: str):
        net = Network("650px", "1500px", heading = self.name)
        for node in self.nodes:
            net.add_node(node.label, label = node.label, color = node.color, shape = node.shape)
        for edge in self.edges:
            net.directed = edge.isOriented
            net.add_edge(edge.first, edge.second, color = edge.color, label = edge.label)
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
    