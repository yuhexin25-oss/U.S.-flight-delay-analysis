"""Flight-route network construction and centrality metrics."""

from __future__ import annotations

import networkx as nx
import pandas as pd


def build_route_graph(flights: pd.DataFrame) -> nx.DiGraph:
    """Build a directed route graph with flight volume and delay intensity."""
    routes = flights.groupby(["origin", "destination"]).agg(
        total_flights=("origin", "size"),
        average_delay=("arrival_delay", "mean"),
    )
    graph = nx.DiGraph()
    for (origin, destination), row in routes.iterrows():
        graph.add_edge(origin, destination, **row.to_dict())
    return graph


def centrality_table(graph: nx.DiGraph) -> pd.DataFrame:
    """Calculate comparable degree and betweenness scores."""
    return pd.DataFrame({
        "degree_centrality": nx.degree_centrality(graph),
        "betweenness_centrality": nx.betweenness_centrality(graph),
    }).sort_values("degree_centrality", ascending=False)

