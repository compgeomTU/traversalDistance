"""U-path / immersed-tree example used in the README and regression tests."""

from traversal_distance import Graph, compute_traversal_distances, traversal_decisions


def make_u_path_immersed_tree():
    """Return the U-shaped path P and immersed tree H from the README example."""
    P = Graph.from_data(
        {0: (0, 0), 1: (0, 20), 2: (20, 20), 3: (20, 0)},
        {0: (0, 1), 1: (1, 2), 2: (2, 3)},
    )
    H = Graph.from_data(
        {0: (8, 6), 1: (8, 12), 2: (13, 10), 3: (10, 10),
         4: (7, 10), 5: (12, 12), 6: (12, 6), 7: (10, 7), 8: (11, 16)},
        {0: (0, 1), 1: (1, 2), 2: (2, 3), 3: (3, 4),
         4: (4, 5), 5: (5, 6), 6: (3, 7), 7: (7, 8)},
    )
    return P, H


def main():
    P, H = make_u_path_immersed_tree()

    d = compute_traversal_distances(P, H, tolerance=1e-6)
    print(f"P -> H:   {d.first_to_second:.7g}")
    print(f"H -> P:   {d.second_to_first:.7g}")
    print(f"Symmetric: {d.symmetric:.7g}")
    print(f"Complete:  {d.complete:.7g}")
    print("At epsilon 12:  ", traversal_decisions(P, H, 12.0))
    print("At epsilon 12.3:", traversal_decisions(P, H, 12.3))


if __name__ == "__main__":
    main()
