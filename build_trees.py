import math

import cv2

from screen_functions import showScreen


class TreeNode:
    def __init__(self, node):
        self.node = node
        self.children = []
        self.parent = None

    def add_child(self, child_node):
        self.children.append(child_node)

    def set_parent(self, parent_node):
        self.parent = parent_node

    def remove_child(self, child_node):
        self.children = [child for child in self.children if child != child_node]

    def traverse(self):
        nodes = [self]  # Add the current node itself
        for child in self.children:
            nodes.extend(child.traverse())  # Recursively add all children's nodes
        return nodes


class Tree:
    def __init__(self, node):
        self.root = TreeNode(node)
        self.corrupted = False

    def children_tally(self):
        return len(self.traverse())
    def traverse(self):
        if self.root:
            return self.root.traverse()
        else:
            return []

def calculate_distance(point, center):
    x1, y1 = point[0], point[1]
    x2, y2 = center[0], center[1]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def sortTrees(trees):
    non_corrupted = [tree for tree in trees if not tree.corrupted]
    corrupted = [tree for tree in trees if tree.corrupted]

    non_corrupted_sorted = sorted(non_corrupted, key=lambda tree: tree.children_tally())

    corrupted_sorted_less_than_3 = sorted([tree for tree in corrupted if tree.children_tally() < 3], key=lambda tree: tree.children_tally())
    corrupted_sorted_rest = sorted([tree for tree in corrupted if tree.children_tally() >= 3], key=lambda tree: tree.children_tally())

    sorted_trees = corrupted_sorted_less_than_3 + non_corrupted_sorted + corrupted_sorted_rest

    return sorted_trees
def buildTrees(nodes, lines, image):
    web_center = (683, 562)
    counter = 1
    processed = []
    trees = []

    sorted_nodes = sorted(nodes, key=lambda point: calculate_distance(point, web_center))

    def findChildren(root):
        for child in sorted_nodes:
            if child not in processed and child[2] == 2 and (((root.node[0], root.node[1]), (child[0], child[1])) in lines or
                                                             ((child[0], child[1]), (root.node[0], root.node[1])) in lines):
                if calculate_distance((child[0], child[1]), web_center) > calculate_distance((root.node[0], root.node[1]), web_center) + 20:
                    processed.append(child)
                    child_node = TreeNode(child)
                    child_node.set_parent(root)
                    root.add_child(child_node)

                    findChildren(child_node)

            if child[2] == 0 and (((root.node[0], root.node[1]), (child[0], child[1])) in lines or ((child[0], child[1]), (root.node[0], root.node[1])) in lines):
                trees[len(trees) - 1].corrupted = True
        return

    for node in sorted_nodes:
        if node not in processed and node[2] == 2:
            processed.append(node)
            trees.append(Tree(node))

            findChildren(trees[len(trees) - 1].root)

    return sortTrees(trees)