"""Toy microtubule lattice scaffolding.

This is a graph scaffold for perturbation plumbing only. It is not a full
cochain-Laplacian implementation and it is not a biological validity claim.
"""

from __future__ import annotations

from dataclasses import dataclass


Edge = tuple[int, int]


@dataclass(frozen=True)
class MicrotubuleLattice:
    protofilaments: int
    rings: int
    nodes: int
    edges: tuple[Edge, ...]


def node_id(protofilament: int, ring: int, rings: int) -> int:
    return protofilament * rings + ring


def build_cylindrical_lattice(protofilaments: int = 13, rings: int = 8) -> MicrotubuleLattice:
    if protofilaments < 3:
        raise ValueError("protofilaments must be at least 3")
    if rings < 2:
        raise ValueError("rings must be at least 2")

    edges: set[Edge] = set()
    for protofilament in range(protofilaments):
        next_protofilament = (protofilament + 1) % protofilaments
        for ring in range(rings):
            current = node_id(protofilament, ring, rings)
            lateral = node_id(next_protofilament, ring, rings)
            edges.add(tuple(sorted((current, lateral))))
            if ring + 1 < rings:
                longitudinal = node_id(protofilament, ring + 1, rings)
                edges.add(tuple(sorted((current, longitudinal))))

    return MicrotubuleLattice(
        protofilaments=protofilaments,
        rings=rings,
        nodes=protofilaments * rings,
        edges=tuple(sorted(edges)),
    )


def deterministic_edge_drop(edges: tuple[Edge, ...], drop_fraction: float) -> tuple[Edge, ...]:
    """Drop an evenly spaced fraction of edges without randomness."""

    if not 0.0 <= drop_fraction < 1.0:
        raise ValueError("drop_fraction must be in [0, 1)")
    if drop_fraction == 0.0:
        return edges

    period = max(1, round(1.0 / drop_fraction))
    kept = [edge for index, edge in enumerate(edges) if (index + 1) % period != 0]
    return tuple(kept)


def edge_retention(original_edges: tuple[Edge, ...], perturbed_edges: tuple[Edge, ...]) -> float:
    if not original_edges:
        raise ValueError("original_edges must not be empty")
    return len(set(perturbed_edges)) / len(set(original_edges))
