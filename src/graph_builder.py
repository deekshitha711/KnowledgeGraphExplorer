"""NetworkX Graph Construction & Dynamic UI Injection for PyVis."""

import networkx as nx
from pyvis.network import Network
import textwrap

def build_graph(root_title: str, related_titles: list[str], details: dict, source_type: str) -> nx.DiGraph:
    """Builds a formal NetworkX directed graph representing extracted relationships."""
    graph = nx.DiGraph()
    root_info = details.get(root_title, {})
    
    relation_label = "Wikidata Property" if source_type == "Wikidata" else "Wikipedia Reference"

    # 1. Add Central Target (Root Node)
    graph.add_node(
        root_title, 
        kind="Root Concept",
        summary=root_info.get("summary", ""), 
        url=root_info.get("url", "")
    )

    # 2. Add Relational Targets (Related Nodes)
    for title in related_titles:
        item = details.get(title, {})
        graph.add_node(
            title, 
            kind="Related Entity",
            summary=item.get("summary", ""), 
            url=item.get("url", "")
        )
        graph.add_edge(root_title, title, relation=relation_label)

    return graph

def graph_statistics(graph: nx.DiGraph) -> dict:
    """Calculates Data Science topological network analysis metrics."""
    n_nodes = graph.number_of_nodes()
    n_edges = graph.number_of_edges()
    degrees = dict(graph.degree())
    
    return {
        "nodes": n_nodes, 
        "edges": n_edges,
        "density": (nx.density(graph) if n_nodes > 1 else 0.0),
        "components": (nx.number_connected_components(graph.to_undirected()) if n_nodes else 0),
        "average_degree": (sum(degrees.values()) / n_nodes if n_nodes else 0.0),
        "degrees": degrees, 
        "centrality": nx.degree_centrality(graph)
    }

def make_graph_html(graph: nx.DiGraph, root_title: str) -> str:
    """Generates an advanced PyVis graph with Clean Hover Tooltips."""
    net = Network(
        height="640px", width="100%", bgcolor="#05060A", font_color="#FFFFFF",
        directed=True, notebook=False, cdn_resources="in_line"
    )
    
    # Smooth Antigravity Physics
    net.barnes_hut(
        gravity=-10000, 
        central_gravity=0.05, 
        spring_length=250, 
        spring_strength=0.015, 
        damping=0.09
    )

    for node, attrs in graph.nodes(data=True):
        is_root = node == root_title
        summary_text = attrs.get("summary", "No details available.")
        
        # -----------------------------------------------------------------
        # MEDIUM-SIZED SUMMARY (~280 characters, cut cleanly at whole word)
        # -----------------------------------------------------------------
        if len(summary_text) > 280:
            medium_summary = summary_text[:280].rsplit(" ", 1)[0] + "..."
        else:
            medium_summary = summary_text

        # Line wrap at 65 characters so it forms a clean 4-line readable box
        wrapped_summary = "\n".join(textwrap.wrap(medium_summary, width=65))
        clean_tooltip = f"Concept: {node}\n\nSummary:\n{wrapped_summary}"
        
        # Cyberpunk Neon Node Colors
        if is_root:
            color = {"background": "#FF00EA", "border": "#FFFFFF", "highlight": {"background": "#FF4DFF", "border": "#00F3FF"}}
        else:
            color = {"background": "rgba(0,243,255,0.1)", "border": "#00F3FF", "highlight": {"background": "#00F3FF", "border": "#FFFFFF"}}

        net.add_node(
            node, 
            label=node, 
            title=clean_tooltip,
            size=50 if is_root else 20, 
            color=color,
            font={"color": "#E2E8F0", "size": 18 if is_root else 12, "face": "Inter", "strokeWidth": 3, "strokeColor": "#05060A"},
            borderWidth=2 if is_root else 1, 
            borderWidthSelected=4,
            shadow={"enabled": True, "color": color["border"] if not is_root else color["background"], "size": 20}
        )

    for source, target, attrs in graph.edges(data=True):
        net.add_edge(
            source, target, 
            title=attrs.get("relation", "Connection"),
            color={"color": "rgba(0, 243, 255, 0.25)", "highlight": "#FF00EA"},
            arrows={"to": {"enabled": True, "scaleFactor": 0.5}}, 
            smooth={"type": "continuous"}
        )

    # Standard interactions, hover enabled, no JS redirect
    net.set_options('{"interaction": {"hover": true, "tooltipDelay": 100, "navigationButtons": false, "keyboard": false}, "physics": {"minVelocity": 0.75}}')
    
    return net.generate_html()