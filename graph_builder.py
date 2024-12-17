from screen_functions import showNodes, showEdges, showGraphs

class TreeNode:
    def __init__(self):
        self.children = set()
        self.parent = None

    def addChild(self, child):
        self.children.update(child)

    def addParent(self, parent):
        self.parent = parent

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
        return f"Position: {self.position} Level: {self.level} Type: {self.type} Connected: {[node.nicePrint() for node in self.connected]}"

    def __str__(self):
        return f"Position: {self.position} Level: {self.level} Type: {self.type} Connected: {[node.nicePrint() for node in self.connected]}"

    def nicePrint(self):
        return f"Position: {self.position} Level: {self.level} Type: {self.type}"

    def addChild(self, node):
        self.connected.append(node)

    def countExclusiveConnections(self):
        def isExclusive(node, visited):
            # If the node has already been visited, skip it to prevent cycles
            if node in visited:
                return False
            visited.add(node)

            for neighbor in node.connected:
                # If any connected neighbor is the same as self, skip it
                if neighbor == self:
                    continue
                # If any neighbor leads to a non-exclusive connection, return False
                if not isExclusive(neighbor, visited):
                    return False
            return True

        exclusive_count = 0
        for neighbor in self.connected:
            visited = set()
            if isExclusive(neighbor, visited):
                exclusive_count += 1

        return exclusive_count

class Graph:
    def __init__(self):
        self.roots = []
        self.nodes = []

    def addRoot(self, root):
        self.roots.append(root)

    def addNodes(self, nodes):
        self.nodes = nodes

    def printAllNodes(self):
        if not self.nodes:
            print("The graph has no nodes.")
        else:
            for node in self.nodes:
                print(node)

def buildGraph(nodes, edges, image=None):
    roots = findRoots(nodes[0], edges)
    root_edges = [edge for edge in edges if not (nodes[0] == edge[0] or nodes[0] == edge[1])]

    connected_components = connectedComponents(roots, root_edges)

    graphs = [Graph() for _ in range(len(connected_components))]

    for i, group in enumerate(connected_components):
        graphs[i].addNodes(group)

        for node in group:
            if node in roots:
                graphs[i].addRoot(node)

        for node in graphs[i].nodes:
            for connected in group:
                for edge in edges:
                    if node == edge[0] and connected == edge[1]:
                        node.addChild(connected)

                    if node == edge[1] and connected == edge[0]:
                        node.addChild(connected)

    #showNodes(image, [graphs[4].roots[0]], False)
    #showNodes(image, graphs[4].roots[0].connected, False)

    #showGraphs(image, [graphs[1]], edges, False)
    #print(graphs[1].nodes[2].countExclusiveConnections())
    #print(graphs[0].nodes)

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

    all_connected_components = [list(fset) for fset in all_connected_components]
    return all_connected_components

