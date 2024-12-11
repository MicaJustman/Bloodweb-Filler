from screen_functions import showNodes, showEdges, showGraphs


class GraphNode:
    def __init__(self, position, level, type):
        self.position = position
        self.level = level
        self.type = type
        self.connected = []

    def __eq__(self, other):
        if isinstance(other, GraphNode):
            return self.position == other.position and self.level == other.level and self.type == other.type
        return False

    def __hash__(self):
        return hash((self.position, self.level, self.type))

    def __repr__(self):
        return f"Position: {self.position} Level: {self.level} Type: {self.type} Connected: {self.connected}"

    def __str__(self):
        return f"Position: {self.position} Level: {self.level} Type: {self.type} Connected: {self.connected}"

    def add_connected(self, node):
        self.connected.append(node)


class Graph:
    def __init__(self, roots):
        self.roots = []
        self.nodes = []

def build_graph(nodes, edges):
    graphs = []

    roots = findRoots(nodes[0], edges)

    edges = [edge for edge in edges if not (nodes[0] == edge[0] or nodes[0] == edge[1])]
    connected_components = connectedComponents(roots, edges)

    for group in connected_components:
        holder = []

        for node in group:
            if node in roots:
                holder.append(node)

        graphs.append(Graph(holder))

        for node in group:
            if node not in roots:
                for edge in edges:
                    if node == edge[0] and edge[1]  and edge[1].type == 2:
                        node.connected.append(edge[1])
                    elif node == edge[1] and edge[0] and edge[0].type == 2:
                        node.connected.append(edge[0])

            graphs[len(graphs) - 1].nodes.append(node)


    return graphs



def findRoots(center, edges, visited=None, connected=None):
    if connected is None:
        connected = set()

    if visited is None:
        visited = set()

    for edge in edges:
        if center == edge[0] and edge[1].type == 2:
            connected.add(edge[1])

        if center == edge[1] and edge[0].type == 2:
            connected.add(edge[0])

        if center == edge[0] and edge[1].type == 0:
            visited.add(edge[1])
            findRoots(edge[1], edges, visited, connected)

        if center == edge[1] and edge[0].type == 0:
            visited.add(edge[0])
            findRoots(edge[0], edges, visited, connected)


    return connected

def connectedComponents(roots, edges):
    def bfs(start_node, edges, visited):
        queue = [start_node]
        connected = set()

        while queue:
            current = queue.pop(0)
            if current not in visited:
                visited.add(current)
                connected.add(current)

                for edge in edges:
                    if current == edge[0] and edge[1] not in visited and edge[1].type == 2:
                        queue.append(edge[1])
                    elif current == edge[1] and edge[0] not in visited and edge[0].type == 2:
                        queue.append(edge[0])

        return connected

    all_connected_components = set()
    visited_nodes = set()

    for root in roots:
        if root not in visited_nodes:
            connected_component = bfs(root, edges, visited_nodes)
            all_connected_components.add(frozenset(connected_component))

    return all_connected_components

