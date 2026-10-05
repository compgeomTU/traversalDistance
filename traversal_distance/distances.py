"""Traversal-distance computations for embedded straight-line graphs.

This module generalizes the connected-component/projection test used in
``compgeomTU/traversalDistance``.  For a fixed epsilon, the free space in every
edge-edge product cell is convex.  A connected free-space component supports

* a directed traversal G -> H iff its projection covers all of G,
* a directed traversal H -> G iff its projection covers all of H, and
* a complete traversal iff its projections cover both graphs.

The distance values are obtained by binary search on this monotone decision
problem.  The geometric decisions themselves are analytic (quadratic), not
sampling based.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
import math

import numpy as np


@dataclass(frozen=True)
class TraversalDistances:
    """Four traversal-distance values for an ordered pair of graphs.

    ``first_to_second`` and ``second_to_first`` are the directed distances.
    ``symmetric`` is their maximum; ``complete`` requires one free-space
    component to cover both inputs.
    """

    first_to_second: float
    second_to_first: float
    symmetric: float
    complete: float
    tolerance: float

    @property
    def graph_to_curve(self):
        """Backward-compatible alias used by FSDvis."""
        return self.first_to_second

    @property
    def curve_to_graph(self):
        """Backward-compatible alias used by FSDvis."""
        return self.second_to_first

    def as_dict(self):
        return {
            "first_to_second": self.first_to_second,
            "second_to_first": self.second_to_first,
            "symmetric": self.symmetric,
            "complete": self.complete,
            "tolerance": self.tolerance,
        }


def _clip01(value):
    return min(1.0, max(0.0, float(value)))


def _quadratic_roots(a, b, c, tolerance=1e-12):
    scale = max(1.0, abs(a), abs(b), abs(c))
    tol = tolerance * scale

    if abs(a) <= tol:
        if abs(b) <= tol:
            return []
        return [-c / b]

    disc = b * b - 4.0 * a * c
    if disc < -tol:
        return []
    disc = max(0.0, disc)
    root = math.sqrt(disc)
    return [(-b - root) / (2.0 * a), (-b + root) / (2.0 * a)]


def _quadratic_sublevel_interval(a, b, c, left, right, tolerance=1e-10):
    """Return the part of [left,right] on which a*x^2+b*x+c <= 0.

    In the uses below the quadratic is convex, so the feasible set is an
    interval (possibly a point).  The implementation also handles degenerate
    linear/constant cases robustly.
    """
    candidates = [float(left), float(right)]
    candidates.extend(
        x
        for x in _quadratic_roots(a, b, c)
        if left - tolerance <= x <= right + tolerance
    )
    candidates = sorted(
        set(max(left, min(right, float(x))) for x in candidates)
    )

    def q(x):
        return a * x * x + b * x + c

    feasible = []
    for x in candidates:
        if q(x) <= tolerance:
            feasible.append(x)

    for x0, x1 in zip(candidates, candidates[1:]):
        midpoint = 0.5 * (x0 + x1)
        if q(midpoint) <= tolerance:
            feasible.extend((x0, x1))

    if not feasible:
        return None
    return min(feasible), max(feasible)


def _closest_parameters(A, B, P, Q):
    """Squared distance minimum between two segments and its parameters."""
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)
    P = np.asarray(P, dtype=float)
    Q = np.asarray(Q, dtype=float)

    u = B - A
    v = Q - P
    w = A - P
    uu = float(np.dot(u, u))
    vv = float(np.dot(v, v))
    uv = float(np.dot(u, v))
    uw = float(np.dot(u, w))
    vw = float(np.dot(v, w))

    candidates = []

    def add(t, s):
        t, s = _clip01(t), _clip01(s)
        d = w + t * u - s * v
        candidates.append((float(np.dot(d, d)), t, s))

    det = uu * vv - uv * uv
    if det > 1e-14 * max(1.0, uu * vv):
        t = (-uw * vv + uv * vw) / det
        s = (uu * vw - uv * uw) / det
        if -1e-12 <= t <= 1.0 + 1e-12 and -1e-12 <= s <= 1.0 + 1e-12:
            add(t, s)

    for t in (0.0, 1.0):
        s = float(np.dot(v, w + t * u) / vv) if vv > 1e-15 else 0.0
        add(t, s)

    for s in (0.0, 1.0):
        t = float(-np.dot(u, w - s * v) / uu) if uu > 1e-15 else 0.0
        add(t, s)

    for t in (0.0, 1.0):
        for s in (0.0, 1.0):
            add(t, s)

    return min(candidates, key=lambda item: item[0])


def _point_segment_interval(point, A, B, epsilon):
    """Parameters t in [0,1] with |A+t(B-A)-point| <= epsilon."""
    point = np.asarray(point, dtype=float)
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)
    u = B - A
    w = A - point

    a = float(np.dot(u, u))
    b = 2.0 * float(np.dot(u, w))
    c = float(np.dot(w, w) - epsilon * epsilon)
    return _quadratic_sublevel_interval(a, b, c, 0.0, 1.0)


def _projection_interval_on_first_segment(A, B, P, Q, epsilon):
    """Projection of one cell's free space onto the first segment parameter.

    This solves
        min_s |A+t(B-A) - (P+s(Q-P))| <= epsilon
    analytically.  The point-to-segment squared distance is a piecewise
    quadratic convex function of t.
    """
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)
    P = np.asarray(P, dtype=float)
    Q = np.asarray(Q, dtype=float)

    u = B - A
    v = Q - P
    w = A - P

    uu = float(np.dot(u, u))
    vv = float(np.dot(v, v))
    uv = float(np.dot(u, v))
    uw = float(np.dot(u, w))
    vw = float(np.dot(v, w))
    ww = float(np.dot(w, w))
    eps2 = epsilon * epsilon

    if uu <= 1e-15:
        min_dist2, _, _ = _closest_parameters(A, B, P, Q)
        return (0.0, 1.0) if min_dist2 <= eps2 + 1e-10 else None

    # s*(t) = (v dot (w+t*u))/|v|^2 changes formula at s=0 and s=1.
    breaks = [0.0, 1.0]
    if vv > 1e-15 and abs(uv) > 1e-15:
        for t in (-vw / uv, (vv - vw) / uv):
            if 0.0 < t < 1.0:
                breaks.append(float(t))
    breaks = sorted(set(breaks))

    feasible_intervals = []
    for left, right in zip(breaks, breaks[1:]):
        midpoint = 0.5 * (left + right)
        if vv <= 1e-15:
            branch = 0
        else:
            s_star = (vw + uv * midpoint) / vv
            branch = 0 if s_star <= 0.0 else (1 if s_star >= 1.0 else 2)

        if branch == 0:
            a = uu
            b = 2.0 * uw
            c = ww - eps2
        elif branch == 1:
            wm = w - v
            a = uu
            b = 2.0 * float(np.dot(u, wm))
            c = float(np.dot(wm, wm)) - eps2
        else:
            a = uu - uv * uv / vv
            b = 2.0 * (uw - vw * uv / vv)
            c = ww - vw * vw / vv - eps2

        interval = _quadratic_sublevel_interval(a, b, c, left, right)
        if interval is not None:
            feasible_intervals.append(interval)

    # Preserve isolated feasible breakpoints exactly, e.g. a tangency.
    for t in breaks:
        X = A + t * u
        if vv <= 1e-15:
            s = 0.0
        else:
            s = _clip01(float(np.dot(v, X - P) / vv))
        d = X - (P + s * v)
        if float(np.dot(d, d)) <= eps2 + 1e-10:
            feasible_intervals.append((t, t))

    if not feasible_intervals:
        return None
    return (
        min(interval[0] for interval in feasible_intervals),
        max(interval[1] for interval in feasible_intervals),
    )


def _interval_union_covers_unit(intervals, tolerance=1e-8):
    if not intervals:
        return False

    intervals = sorted((float(a), float(b)) for a, b in intervals)
    start, end = intervals[0]
    if start > tolerance:
        return False

    for next_start, next_end in intervals[1:]:
        if next_start > end + tolerance:
            return False
        end = max(end, next_end)
        if end >= 1.0 - tolerance:
            return True

    return end >= 1.0 - tolerance


def traversal_decisions(first, second, epsilon):
    """Decision values at epsilon.

    Returns ``(graph_to_curve, curve_to_graph, complete)``.
    """
    epsilon = float(epsilon)
    eps2 = epsilon * epsilon

    nonempty_cells = set()
    graph_projection = {}
    curve_projection = {}

    graph = first
    curve = second

    for graph_edge_id, graph_edge in graph.edges.items():
        A = graph.nodes[graph_edge[0]]
        B = graph.nodes[graph_edge[1]]
        for curve_edge_id, curve_edge in curve.edges.items():
            P = curve.nodes[curve_edge[0]]
            Q = curve.nodes[curve_edge[1]]
            min_dist2, _, _ = _closest_parameters(A, B, P, Q)
            numeric_tol = 1e-10 * max(1.0, eps2, min_dist2)
            if min_dist2 > eps2 + numeric_tol:
                continue

            key = (graph_edge_id, curve_edge_id)
            nonempty_cells.add(key)
            graph_projection[key] = _projection_interval_on_first_segment(
                A, B, P, Q, epsilon
            )
            curve_projection[key] = _projection_interval_on_first_segment(
                P, Q, A, B, epsilon
            )

    if not nonempty_cells:
        return False, False, False

    parent = {key: key for key in nonempty_cells}
    rank = {key: 0 for key in nonempty_cells}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1

    # Same connectivity pass as the traversalDistance free-space DFS, expressed
    # at the cell-component level.  Point-only intervals count as nonempty.
    for graph_vertex_id, graph_vertex in graph.nodes.items():
        incident_graph_edges = [
            edge_id for edge_id, edge in graph.edges.items() if graph_vertex_id in edge
        ]
        if len(incident_graph_edges) < 2:
            continue
        for curve_edge_id, curve_edge in curve.edges.items():
            boundary_interval = _point_segment_interval(
                graph_vertex,
                curve.nodes[curve_edge[0]],
                curve.nodes[curve_edge[1]],
                epsilon,
            )
            if boundary_interval is None:
                continue
            adjacent = [
                (graph_edge_id, curve_edge_id)
                for graph_edge_id in incident_graph_edges
                if (graph_edge_id, curve_edge_id) in nonempty_cells
            ]
            for a, b in combinations(adjacent, 2):
                union(a, b)

    for curve_vertex_id, curve_vertex in curve.nodes.items():
        incident_curve_edges = [
            edge_id for edge_id, edge in curve.edges.items() if curve_vertex_id in edge
        ]
        if len(incident_curve_edges) < 2:
            continue
        for graph_edge_id, graph_edge in graph.edges.items():
            boundary_interval = _point_segment_interval(
                curve_vertex,
                graph.nodes[graph_edge[0]],
                graph.nodes[graph_edge[1]],
                epsilon,
            )
            if boundary_interval is None:
                continue
            adjacent = [
                (graph_edge_id, curve_edge_id)
                for curve_edge_id in incident_curve_edges
                if (graph_edge_id, curve_edge_id) in nonempty_cells
            ]
            for a, b in combinations(adjacent, 2):
                union(a, b)

    components = {}
    for cell_key in nonempty_cells:
        components.setdefault(find(cell_key), []).append(cell_key)

    graph_to_curve = False
    curve_to_graph = False
    complete = False

    for component_cells in components.values():
        graph_intervals = {edge_id: [] for edge_id in graph.edges}
        curve_intervals = {edge_id: [] for edge_id in curve.edges}

        for cell_key in component_cells:
            graph_edge_id, curve_edge_id = cell_key
            graph_interval = graph_projection[cell_key]
            curve_interval = curve_projection[cell_key]
            if graph_interval is not None:
                graph_intervals[graph_edge_id].append(graph_interval)
            if curve_interval is not None:
                curve_intervals[curve_edge_id].append(curve_interval)

        covers_graph = all(
            _interval_union_covers_unit(graph_intervals[edge_id])
            for edge_id in graph.edges
        )
        covers_curve = all(
            _interval_union_covers_unit(curve_intervals[edge_id])
            for edge_id in curve.edges
        )

        graph_to_curve = graph_to_curve or covers_graph
        curve_to_graph = curve_to_graph or covers_curve
        complete = complete or (covers_graph and covers_curve)

    return graph_to_curve, curve_to_graph, complete


def _vertex_distance_upper_bound(first, second):
    if not first.nodes or not second.nodes:
        return 0.0
    return max(
        math.dist(first_point, second_point)
        for first_point in first.nodes.values()
        for second_point in second.nodes.values()
    )


def compute_traversal_distances(first, second, tolerance=1e-6, max_iterations=80):
    """Compute both directed, symmetric, and complete traversal distances.

    Values are returned to within ``tolerance`` (absolute epsilon units).
    ``symmetric`` is the maximum of the two directed values.
    """
    tolerance = float(tolerance)
    if tolerance <= 0.0:
        raise ValueError("tolerance must be positive")

    upper = _vertex_distance_upper_bound(first, second)
    if upper == 0.0:
        return TraversalDistances(0.0, 0.0, 0.0, 0.0, tolerance)

    cache = {}

    def decision(epsilon):
        # Reuse identical binary-search probes when they happen to coincide.
        key = float(epsilon)
        if key not in cache:
            cache[key] = traversal_decisions(first, second, key)
        return cache[key]

    decision_at_zero = decision(0.0)

    def threshold(index):
        if decision_at_zero[index]:
            return 0.0

        low, high = 0.0, upper
        # At upper every point pair lies in free space, so all three decisions
        # are true for connected input graphs.
        if not decision(high)[index]:
            # This should only be possible for malformed/disconnected inputs.
            return math.inf

        for _ in range(int(max_iterations)):
            if high - low <= tolerance:
                break
            midpoint = 0.5 * (low + high)
            if decision(midpoint)[index]:
                high = midpoint
            else:
                low = midpoint
        return high

    first_to_second = threshold(0)
    second_to_first = threshold(1)
    complete = threshold(2)
    symmetric = max(first_to_second, second_to_first)

    return TraversalDistances(
        first_to_second=first_to_second,
        second_to_first=second_to_first,
        symmetric=symmetric,
        complete=complete,
        tolerance=tolerance,
    )
