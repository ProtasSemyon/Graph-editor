colors = ["red", "green", "blue", "black", "yellow", "gray"]
shapes = ["dot", "square", "star", "diamond", "triangle"]

class Node:
    def __init__(self, label: str, color: str = "black", shape: str = "dot"):
        try:
            assert label != ""
        except AssertionError:
            print("Node label can't be empty")
            raise SystemExit
        self.label = label
        
        try:
            assert color in colors
        except AssertionError:
            print("Wrong color")
            raise SystemExit
        self.color = color

        try:
            assert shape in shapes
        except AssertionError:
            print("Wrong shape")
            raise SystemExit
        self.shape = shape

class Edge:
    def __init__(self, first: Node, second: Node, isOriented: bool = False, color: str = "black", label: str = ""):
        self.label = label
        self.first = first
        self.second = second
        try:
            assert color in colors
        except AssertionError:
            print("Wrong color")
            raise SystemExit
        self.color = color
        self.isOriented = isOriented

    def getNodes(self):
        return self.first, self.second
