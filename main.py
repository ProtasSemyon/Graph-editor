import click
from Graph import Graph
from pyvis.network import Network
import os
from pathlib import Path

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
    # graph = Graph(name = "current")
    # graph.add_node("1", "blue", "triangle")
    # graph.add_node("2", "yellow", "diamond")
    # graph.add_node("3", "red", "dot")
    # graph.add_edge("1", "2", True, "black", "12")
    # graph.add_edge("2", "3", True, "black", "23")
    # graph.add_edge("1", "3", True, "black", "13")
    # net.save_graph(f"{graph.name}.html")
    run()








