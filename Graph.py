from Entities import Node, Edge
class Graph:
    def __init__(self, name: str):
        self.name = name
        self.nodes = []
        self.edges = []

    def add_node(self, *args):
        self.nodes.append(Node(*args))

    def add_edge(self, first, second, *args):
        labels = map(lambda x: x.label, self.nodes)
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
        pass

    def load(self, loadPath: str):
        pass
    