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

@run.command("create")
@click.option('-n', '--name')
def create(name):
    global g
    with open("current.txt", "w") as nameInfo:
        nameInfo.write(name)
        nameInfo.close()
        g.edges = []
        g.nodes = []
        g.name = name
        output(g)
        
@run.command("graph_info")
def info():
    global g
    print("Nodes", *g.get_graph_info()[0])
    print("Edges")
    edges = g.get_graph_info()[1]
    for edge in edges:
        arrow = "--"
        if edge[2]:
            arrow = "->"
        print(edge[0], arrow, edge[1])


@run.command("add_node")
@click.option('-l', '--label')
@click.option('-c', '--color', default = "black")
@click.option('-s', '--shape', default = "dot")
def addNode(label: str, color: str, shape: str):
    global g
    g.add_node(label, color, shape)
    output(g)
    
@run.command("add_edge")
@click.option('-s', '--start')
@click.option('-e', '--end')
@click.option('-c', '--color', default = "black")
@click.option('-i', "--isoriented", default = 0)
@click.option('-l', "--label", default = "")
def addEdge(start: str, end: str, color: str, isoriented: bool, label: str):
    global g
    g.add_edge(start, end, isoriented, color, label)
    output(g)

@run.command("del_edge")
@click.option('-s', '--start')
@click.option('-e', '--end')
def delEdge(start: str, end: str):
    global g
    g.del_edge(start, end)
    output(g)

@run.command("del_node")
@click.option('-l', '--label')
def delNode(label: str):
    global g
    g.del_node(label)
    output(g)

@run.command("nodes_degree")
@click.option('-l', '--label')
def node_degree(label: str):
    global g
    print(g.node_degree(label))

@run.command("nodes_degrees")
def nodes_degrees():
    global g
    degrees = g.nodes_degrees()
    for i in degrees:
        print(i[0], "-", i[1])

@run.command("switch")
@click.option('-n', '--name')
def switch(name: str):
    global g
    g = Graph(name)
    g.load(f"{g.name}.html")
    with open("current.txt", "w") as nameInfo:
        nameInfo.write(name)
        nameInfo.close()
    output(g)



def output(graph):
    
    net = Network("650px", "1500px", heading = graph.name)
    for node in graph.nodes:
        net.add_node(node.label, label = node.label, color = node.color, shape = node.shape)
    for edge in graph.edges:
        net.directed = edge.isOriented
        net.add_edge(edge.first.label, edge.second.label, color = edge.color, label = edge.label)
    net.save_graph("current.html")
    net.save_graph(f"{graph.name}.html")

if __name__ == "__main__":
    with open("current.txt", "r") as nameInfo:
        name = nameInfo.read()
        nameInfo.close()
    g: Graph = Graph(name)
    g.load("current.html")
    run()








