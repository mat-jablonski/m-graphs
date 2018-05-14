import networkx as nx
import random
import matplotlib.pyplot as plt
import itertools

RANDOM_M_GRAPHS_OUTPUT_DIRECTORY = "random_m_graphs"
ALL_M_GRAPHS_OUTPUT_DIRECTORY = "all_m_graphs"


def add_short_edges(G):
    n = G.number_of_nodes()

    for i in range(1, n):
        G.add_edge(i, i + 1)

        if i < n - 1:
            G.add_edge(i, i + 2)


def add_random_long_edges(G):
    
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
        for j in range(i + 3, n + 1):
            if G.has_edge(i,j):
                continue
            if not check_edge_correctness(graph_long_edges,(i,j)):
                continue
            
            edges_from_i.append((i,j))
        
        edges.extend(edges_from_i)

    return edges


def check_edge_correctness(graph_long_edges, edge):
    """
    Checks if long edge 'edge' can be legally added to 
    a graph with set of long edges in 'graph_long_edges'.
    """
   
    if not graph_long_edges:
        return True

    bad_edges = [graph_edge for graph_edge in graph_long_edges if is_under(edge, graph_edge) or is_under(graph_edge, edge)]

    return not bad_edges

def check_if_maximal(G, edges):
    """Checks if we cannot add any long edge to this set of edges."""

    n = G.number_of_nodes()

    for i in range(1, n - 1):
        for j in range(i + 3, n + 1):
            if (i,j) in edges:
                continue
            if check_edge_correctness(edges, (i,j)):
                return False
    
    return True


def add_long_edges_starting_at(G, edges, left_end, rightmost_end, counter):

    n = G.number_of_nodes()

    if left_end >= n - 2:
        if check_if_maximal(G, edges):
            G.add_edges_from(edges)
            save_graph(G, counter)
            G.remove_edges_from(edges)
            counter = counter + 1
        
        return counter

    for nr_of_edges in range(0, n + 1 - rightmost_end + 1):
        for right_ends in set(itertools.combinations(list(range(max(rightmost_end, left_end + 3), n + 1)), nr_of_edges)):
            new_rightmost_end = rightmost_end
            new_edges = edges.copy()
            if right_ends:  
                for right_end in right_ends:
                    new_edges.append((left_end, right_end))
                    if right_end > new_rightmost_end:
                        new_rightmost_end = right_end
            counter = add_long_edges_starting_at(G, new_edges, left_end + 1, new_rightmost_end, counter)

    return counter


def is_under(edge1, edge2):
    """Checks if edge1 is under edge2."""

    c1 = edge2[0] < edge1[0]
    c2 = edge1[1] < edge2[1]
    c3 = edge2[0] < edge1[1]
    c4 = edge1[0] < edge2[1]

    return c1 and c2 and c3 and c4 


def save_graph(G, counter=1, toConsole=True, toFile=True, toImage=True):
    
    n = G.number_of_nodes()
    filename = 'm_graph_{0}_{1}'.format(n, counter)

    if toConsole:
        print(filename, [x for x in G.edges() if abs(x[0] - x[1]) > 2])

    if toFile:
        nx.write_adjlist(G, '{0}/{1}'.format(RANDOM_M_GRAPHS_OUTPUT_DIRECTORY, filename))

    if toImage:
        ax = plt.subplot(111)
        ax.set_title('MGraph n:{0}'.format(n), fontsize=10)

        nx.draw(G, nx.circular_layout(G), node_size=600, node_color='red', font_size=8, font_weight='bold', with_labels=True)
        plt.tight_layout()
        plt.savefig('{0}/{1}.png'.format(RANDOM_M_GRAPHS_OUTPUT_DIRECTORY,filename), format="PNG")

        plt.close()


def generate_all_m_graphs_with_n_nodes(n):
    G = nx.Graph()
    G.add_nodes_from(list(range(1, n + 1)))
    add_short_edges(G)
    add_long_edges_starting_at(G, [], 1, 4, 1)


def generate_random_m_graph_with_n_nodes(n):
    G = nx.Graph()
    G.add_nodes_from(list(range(1, n + 1)))
    add_short_edges(G)
    add_random_long_edges(G)
    save_graph(G)

    return G


def color_graph(G):
	T = {w: -1 for r in range(G.number_of_nodes() + 1) for w in itertools.combinations(G.nodes(), r)}  # set(w)
	T[()] = 0

	for w in T.keys():
		if len(w) == 1:
			T[w] = 1
	
	for w in T.keys():
		if len(w) <= 1:
			continue

		min_chi = G.number_of_nodes()
		subsets = [s for r in range(1, len(w) + 1) for s in itertools.combinations(w, r)]  # non-empty subsets
		
		for s in subsets:
			if len(s) == len(w):
				g_s = G.subgraph(s)
				if g_s.number_of_edges() > 0:
					continue
			else:
				if T[s] > 1:
					continue

			temp = list(set(w) - set(s))
			temp.sort()
			temp = tuple(temp)
				
			if T[temp] < min_chi:
				min_chi = T[temp]

		T[w] = min_chi + 1

	return T[tuple(G.nodes())]
		

G = generate_random_m_graph_with_n_nodes(15)
chromatic_number = color_graph(G)
print('chromatic_number', chromatic_number)
    
