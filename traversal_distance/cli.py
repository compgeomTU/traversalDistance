"""Command-line interface for computing traversal distances."""

from __future__ import annotations

import argparse

from .distances import compute_traversal_distances
from .graph import Graph


def build_parser():
    parser = argparse.ArgumentParser(
        description="Compute directed, symmetric, and complete traversal distances."
    )
    parser.add_argument("graph1", help="first graph filename prefix")
    parser.add_argument("graph2", help="second graph filename prefix")
    parser.add_argument(
        "--tolerance",
        type=float,
        default=1e-6,
        help="absolute epsilon tolerance (default: 1e-6)",
    )
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    g1 = Graph(args.graph1)
    g2 = Graph(args.graph2)
    d = compute_traversal_distances(g1, g2, tolerance=args.tolerance)
    print(f"Graph 1 -> Graph 2: {d.first_to_second:.10g}")
    print(f"Graph 2 -> Graph 1: {d.second_to_first:.10g}")
    print(f"Symmetric:          {d.symmetric:.10g}")
    print(f"Complete:           {d.complete:.10g}")


if __name__ == "__main__":
    main()
