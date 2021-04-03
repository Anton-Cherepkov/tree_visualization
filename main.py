from visualization.visualizer import visualize

import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Binary tree visualization tool.')
    parser.add_argument(
        "--node_color",
        default="black",
        help="Colors from matplotlib: https://matplotlib.org/stable/gallery/color/named_colors.html"
    )
    parser.add_argument(
        "--edge_color",
        default="green",
        help="Colors from matplotlib: https://matplotlib.org/stable/gallery/color/named_colors.html"
    )
    parser.add_argument(
        'graphs',
        metavar='graphs',
        nargs='+', 
        help='GraphML files')
    args = parser.parse_args()
    
    for graph_fpath in args.graphs:
        visualize(graph_fpath=graph_fpath, args=args)
