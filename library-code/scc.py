# Calculates the strongly connected components in a direct graph, using 
# Tarjan's strongly connected components algorithm as described in:
# "Depth-first search and linear graph algorithms" (1972)
#
# Given a set of vertices and a dictionary of edges (where the keys are source
# vertices, and the values are iterables of vertices)
# This returns the components as a list of sets in reverse topological order.
def StronglyConnectedComponents(vertices, edges):
    index = 0
    lowlink = {}
    number = {}
    on_stack = set()
    stack = []
    components = []

    # TODO: rewrite to be iterative
    def dfs(v):
        nonlocal index
        index += 1
        lowlink[v] = number[v] = index
        v_pos = len(stack)
        stack.append(v)
        on_stack.add(v)
        for w in edges[v]:
            if w not in number:
                dfs(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif number[w] < number[v]:
                if w in on_stack:
                    lowlink[v] = min(lowlink[v], lowlink[w])
        if lowlink[v] == number[v]:
            component = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                component.append(w)
                if w == v: break
            components.append(component)

    for w in vertices:
        if w not in number:
            dfs(w)

    return components


# Returns a dictionary that maps from vertex to 0-based component index
def ComponentIndex(components):
    return {v: i for i, c in enumerate(components) for v in c}

# Calculates the DAG of components as a set of edges (i, j), so that if
# (i, j) is in the dag, there exists an edge between a vertex v in component[i]
# and a vertex w in component[j].
def ComponentDag(components, edges, index):
    return set((i, j) for v in edges for w in edges[v] if (i := index[v]) != (j := index[w]))


if __name__ == '__main__':
    vertices = {1,2,3,4,5,6,7,8,9,10}
    edges = {
        1: [2],
        2: [3],
        3: [4, 6, 7],
        4: [1, 8],
        5: [5],
        6: [7],
        7: [6],
        8: [9],
        9: [],
        10: [2, 6],
    }
    components = StronglyConnectedComponents(vertices, edges)
    
    assert components == [
        [9],               # 0
        [8],               # 1
        [7, 6],            # 2
        [4, 3, 2, 1],      # 3
        [5],               # 4
        [10],              # 5
    ]

    index = ComponentIndex(components)
    assert index == {
         1: 3,
         2: 3,
         3: 3,
         4: 3,
         5: 4,
         6: 2, 
         7: 2,
         8: 1,
         9: 0,
        10: 5,
    }

    # Note that these pairs of component ids are all descending, because
    # componenets are returned in reverse topological order.
    assert ComponentDag(components, edges, index) == {
        (5, 2),     # {10} -> {6,7}
        (5, 3),     # {10} -> {1,2,3,4}
        (3, 2),     # {1,2,3,4} -> {6,7}
        (3, 1),     # {1,2,3,4} -> {8}
        (1, 0),     # {8} -> {9}
    }
