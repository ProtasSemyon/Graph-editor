import click
from Graph import Graph
from pyvis.network import Network
import os

@click.group()
def run() -> None:
    pass

@run.command('show')
def show():
    os.system(".\current.html")


def output(graph):
    net = Network("650px", "1500px", heading = graph.name)
    for node in graph.nodes:
        net.add_node(node.label, label = node.label, color = node.color, shape = node.shape)
    for edge in graph.edges:
        net.directed = edge.isOriented
        net.add_edge(edge.first, edge.second, color = edge.color, label = edge.label)
    net.save_graph(f"{graph.name}.html")



if __name__ == "__main__":
    g = Graph("current")
    #g.load("current.html")
    g.add_node("1", "red", "dot")
    g.add_node("2", "red", "dot")
    g.add_edge("1", "2", True, "black", "23")
    output(g)
    #run()








