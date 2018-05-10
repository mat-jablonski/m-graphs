import networkx as nx
import random
import matplotlib.pyplot as plt

RANDOM_M_GRAPHS_OUTPUT_DIRECTORY = "random_m_graphs"
ALL_M_GRAPHS_OUTPUT_DIRECTORY = "all_m_graphs"

def add_short_edges(G):
    n = G.number_of_nodes()

    for i in range(1, n):
        G.add_edge(i, i + 1)

        if i < n - 1:
            G.add_edge(i, i + 2)

def add_long_edges(G):
    
    long_edges = []

    while(True):

        long_edges = get_all_correct_long_edges_to_add(G)
        if not long_edges:
            break
        
        edge_to_add = random.choice(long_edges)

        G.add_edge(*edge_to_add)

def get_all_correct_long_edges_to_add(G):
    
    edges = []
    n = G.number_of_nodes()

    graph_long_edges = [x for x in G.edges() if abs(x[0] - x[1]) > 2]
    
    for i in range(1, n - 1):
      
        edges_from_i = []
        for j in range(i + 2, n + 1):
            if G.has_edge(i, j):
                continue
            if check_edge_correctness(graph_long_edges,(i,j)) == False:
                continue
            
            edges_from_i.append((i,j))
        
        edges.extend(edges_from_i)

    return edges

def check_edge_correctness(graph_long_edges, edge):
   
    if not graph_long_edges:
        return True

    bad_edges = [graph_edge for graph_edge in graph_long_edges if is_under(edge, graph_edge) or is_under(graph_edge, edge)]

    return not bad_edges

#check if edge1 is under edge2
def is_under(edge1, edge2):

    c1 = edge2[0] < edge1[0]
    c2 = edge1[1] < edge2[1]
    c3 = edge2[0] < edge1[1]
    c4 = edge1[0] < edge2[1]

    return c1 and c2 and c3 and c4 

def write_graph_to_file(G):
    
    n = G.number_of_nodes()
    filename = 'm_graph_{0}_{1}'.format(n, 1)
    nx.write_adjlist(G, '{0}\\{1}'.format(RANDOM_M_GRAPHS_OUTPUT_DIRECTORY, filename))

    ax = plt.subplot(111)
    ax.set_title('MGraph n:{0}'.format(n), fontsize=10)

    nx.draw(G, nx.circular_layout(G), node_size=600, node_color='red', font_size=8, font_weight='bold', with_labels=True)
    plt.tight_layout()
    plt.savefig('{0}\\{1}.png'.format(RANDOM_M_GRAPHS_OUTPUT_DIRECTORY,filename), format="PNG")

    plt.close()


def generate_all_m_graphs_with_n_nodes(n):
    G = nx.Graph()
    G.add_nodes_from(list(range(1,n + 1)))
    add_short_edges(G)
   
    return G

def generate_random_m_graph_with_n_nodes(n):
    G = nx.Graph()
    G.add_nodes_from(list(range(1,n + 1)))
    add_short_edges(G)
    add_long_edges(G)
    
    return G

for i in range(6, 21):
    G = generate_random_m_graph_with_n_nodes(i)
    write_graph_to_file(G)
