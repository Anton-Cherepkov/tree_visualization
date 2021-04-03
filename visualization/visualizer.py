from .tree_contours import TreeContours

from pygraphml import GraphMLParser
import matplotlib.pyplot as plt

import os
import sys


def eprint(*args, **kwargs):
    print("Error:", *args, file=sys.stderr, **kwargs)


def find_roots(graph):
    roots = []
    for node in graph.nodes():
        if not node.parent():
            roots.append(node)
    return roots


def is_binary_tree(graph):
    for node in graph.nodes():
        if len(node.children()) > 2:
            return False
    return True


def calculate_depth(node, current_depth=0):
    node.depth = current_depth
    for child in node.children():
        calculate_depth(child, current_depth + 1)


def calculate_layered_tree_down_offsets(node):
    # If node does not exist
    if node is None:
        return TreeContours()
    
    # If node is a root
    if not node.parent():
        node.x_offset = 0
    
    # Get children
    left_child, right_child = None, None
    try:
        left_child = node.children()[0]
        right_child = node.children()[1]
    except IndexError:
        pass

    # Build subtrees recursively and get contours
    left_subtree_contours  = calculate_layered_tree_down_offsets(left_child)
    right_subtree_contours = calculate_layered_tree_down_offsets(right_child)

    # If node has no children
    if left_child is None and right_child is None:
        contours = TreeContours()
        contours.extend(node, 0)

    # If node has only one child
    if (left_child is None) != (right_child is None):
        if left_child is not None:
            left_child.x_offset = 0
            contours = left_subtree_contours
            contours.extend(left_child, 0)
        else:
            right_child.x_offset = 0
            contours = right_subtree_contours
            contours.extend(right_child, 0)

    # If node has two children
    if left_child is not None and right_child is not None:
        left_child.x_offset = -1
        right_child.x_offset = 1
        
        # Find distance between contours
        closest_distance = float("inf")
        for a, b in zip(left_subtree_contours.right_contour_offsets_from_root,
                        right_subtree_contours.left_contour_offsets_from_root):
            closest_distance = min(closest_distance, (b + 1) - (a - 1))
        
        # Move subtrees according to the distance
        if closest_distance < 1:
            right_child.x_offset += (1 - closest_distance)

        # Center
        distance_between_children = right_child.x_offset - left_child.x_offset
        new_left_offset  = distance_between_children // 2
        new_right_offset = distance_between_children - new_left_offset
        left_child.x_offset = -new_left_offset
        right_child.x_offset = new_right_offset
    
        contours = TreeContours.merge_contours(
            left_subtree_contours,
            right_subtree_contours,
            node,
            left_child.x_offset,
            right_child.x_offset)
    
    return contours


def save_figure(root, fpath, node_color, edge_color):
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    def add_node_to_figure(node):
        ax.scatter(
            [node.x_offset_global],
            [-node.depth],
            lw=10,
            color=node_color)
    
    def add_edge_to_figure(parent, child):
        ax.plot(
            [parent.x_offset_global, child.x_offset_global],
            [-parent.depth, -child.depth],
            lw=2,
            c=edge_color
        )

    def rec(node, current_x_offset=0):
        current_x_offset += node.x_offset
        node.x_offset_global = current_x_offset

        add_node_to_figure(node)
        if node.parent():
            add_edge_to_figure(node.parent()[0], node)

        for child in node.children():
            rec(child, current_x_offset)
            
    
    rec(root)
        
    fig.savefig(fpath)


def visualize(graph_fpath, args):
    # Read graph
    parser = GraphMLParser()
    graph = parser.parse(graph_fpath)
    graph_name, _ = os.path.splitext(graph_fpath)
    figure_fpath = f"{graph_name}.png"

    # Find root node
    roots = find_roots(graph)
    if not roots:
        eprint("Failed to find root node!")
        return
    if len(roots) > 1:
        eprint("Found multiple root nodes!")
        return
    root = roots[0]
    del roots

    # Check whether the tree is binary
    if not is_binary_tree(graph):
        eprint("Only binary trees are supported!")
    
    calculate_depth(root)
    calculate_layered_tree_down_offsets(root)
    save_figure(
        root,
        fpath=figure_fpath,
        node_color=args.node_color,
        edge_color=args.edge_color)
