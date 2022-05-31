from Entities import Node, Edge
class Graph:
    def __init__(self, name):
        self.name = name
        self.nodes = []
        self.edges = []

    def add_node(self, *args):
        self.nodes.append(Node(*args))

    def add_edge(self):
        pass

    def del_node(self):
        pass
    
    def del_edge(self):
        pass

    def node_degree(self, node: str) -> int:
        return 0
    
    def nodes_degree(self) -> tuple[int]:
        return (0)
    
    def get_graph_info(self):
        pass
    
    def save(self, savePath: str):
        pass

    def load(self, loadPath: str):
        pass
    