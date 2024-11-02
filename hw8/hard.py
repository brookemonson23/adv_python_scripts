import networkx as nx

G = nx.Graph()

G.add_weighted_edges_from ([
    ('A', 'B', 5),
    ('A', 'C', 3),
    ('A', 'D', 6),
    ('A', 'E', 7),
    ('A', 'F', 2),
    ('A', 'G', 4),
    ('B', 'C', 1),
    ('B', 'D', 8),
    ('B', 'E', 3),
    ('B', 'F', 5),
    ('B', 'G', 9),
    ('C', 'D', 2),
    ('C', 'E', 4),
    ('C', 'F', 7),
    ('C', 'G', 6),
    ('D', 'E', 3),
    ('D', 'F', 1),
    ('D', 'G', 8),
    ('E', 'F', 9),
    ('E', 'G', 5),
    ('F', 'G', 2)

])

high_degree = len([degree for _, degree in G.degree() if degree > 5])
print(high_degree)
