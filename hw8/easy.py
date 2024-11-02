import networkx as nx

A = nx.Graph()

A.add_edge(1, 2)
A.add_edge(2, 3)

num_nodes = A.number_of_nodes()
print(num_nodes)