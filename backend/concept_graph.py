"""
concept_graph.py  --  Related concepts using BFS and DFS.

Syllabus link: Unit I - Problem solving by searching (BFS, DFS) and
Unit II - Ontology / ConceptNet as a knowledge graph.

Idea: the ontology groups words that mean the SAME thing (ontology.py).
This file connects concepts that are RELATED, like a tiny ConceptNet.
    solar -- battery -- electric -- motor -- vehicle ...
Each line below is one edge of a graph (a concept is a node).

Starting from a concept in the user's idea we search the graph:
    BFS (Breadth First Search): visits all neighbours first, then their
        neighbours. So it finds the CLOSEST related concepts first.
        Uses a queue (first in, first out).
    DFS (Depth First Search): goes as deep as possible along one path
        before coming back. It shows one long chain of ideas.
        Uses a stack (last in, first out).

Nothing is learned. The graph is written by hand, so you can add edges.
"""
from collections import deque

from backend import preprocess

# Each pair is an edge. The graph works in both directions.
EDGES = [
    ("solar", "battery"), ("solar", "inverter"), ("solar", "charging"), ("solar", "panel"),
    ("battery", "charging"), ("battery", "electric"), ("battery", "power"),
    ("charging", "wireless"), ("charging", "power"),
    ("electric", "motor"), ("electric", "vehicle"), ("electric", "power"),
    ("motor", "vehicle"), ("motor", "gear"), ("motor", "pump"),
    ("vehicle", "tyre"), ("vehicle", "brake"), ("vehicle", "engine"), ("vehicle", "navigation"),
    ("engine", "fuel"), ("engine", "heat"), ("engine", "emission"),
    ("tyre", "rubber"), ("brake", "sensor"),
    ("sensor", "monitor"), ("sensor", "wireless"), ("sensor", "alarm"), ("sensor", "camera"),
    ("wireless", "bluetooth"), ("wireless", "internet"),
    ("internet", "cloud"), ("internet", "phone"), ("internet", "software"),
    ("phone", "display"), ("phone", "camera"), ("phone", "app"),
    ("app", "software"), ("software", "data"), ("data", "cloud"),
    ("display", "light"), ("light", "led"), ("light", "solar"),
    ("heat", "cooling"), ("heat", "insulation"), ("cooling", "refrigeration"),
    ("water", "purification"), ("water", "pump"), ("water", "irrigation"), ("water", "tank"),
    ("purification", "filter"), ("purification", "membrane"), ("purification", "sensor"),
    ("irrigation", "agriculture"), ("irrigation", "sensor"),
    ("agriculture", "soil"), ("agriculture", "fertilizer"), ("agriculture", "seed"),
    ("soil", "moisture"), ("moisture", "sensor"),
    ("medical", "patient"), ("medical", "wearable"), ("medical", "sterilization"),
    ("wearable", "sensor"), ("wearable", "textile"), ("wearable", "battery"),
    ("textile", "fiber"), ("textile", "bag"), ("bag", "strap"), ("bag", "lock"),
    ("lock", "alarm"), ("alarm", "wireless"),
    ("food", "packaging"), ("food", "cooling"), ("packaging", "bag"),
    # software ideas
    ("language", "translation"), ("language", "voice"), ("language", "learning"),
    ("voice", "assistant"), ("voice", "recognition"), ("translation", "dictionary"),
    ("learning", "video"), ("learning", "quiz"), ("learning", "certificate"),
    ("chatbot", "assistant"), ("chatbot", "language"), ("website", "app"),
    ("app", "notification"), ("video", "streaming"), ("data", "analytics"),
    ("payment", "wallet"), ("payment", "bank"), ("payment", "app"),
]

# Build the graph: concept -> list of neighbours.
GRAPH = {}
for a, b in EDGES:
    GRAPH.setdefault(a, []).append(b)
    GRAPH.setdefault(b, []).append(a)

# The idea is stemmed ("batteries" -> "battery"), so we look nodes up by stem too.
_NODE_BY_STEM = {preprocess.simple_stem(node): node for node in GRAPH}


def find_node(token):
    """Idea word (stem) -> graph node, or None if the graph does not know it."""
    return _NODE_BY_STEM.get(token)


def bfs(start, max_depth=2):
    """
    Breadth First Search with a queue.
    Returns [(concept, level)] where level 1 = direct neighbour, 2 = neighbour of neighbour.
    """
    visited = {start}
    queue = deque([(start, 0)])
    found = []
    while queue:
        node, level = queue.popleft()          # take from the FRONT
        if level == max_depth:
            continue
        for neighbour in GRAPH.get(node, []):
            if neighbour not in visited:
                visited.add(neighbour)
                found.append((neighbour, level + 1))
                queue.append((neighbour, level + 1))   # add at the BACK
    return found


def dfs(start, max_depth=4, avoid=()):
    """
    Depth First Search with a stack.
    Follows one path as deep as it can and returns that chain of concepts.
    Concepts in 'avoid' (already in the user's idea) are skipped.
    """
    best_chain = [start]
    stack = [[start]]                           # each item is the path so far
    while stack:
        path = stack.pop()                      # take from the TOP
        if len(path) > len(best_chain):
            best_chain = path
        if len(path) - 1 == max_depth:
            continue
        for neighbour in reversed(GRAPH.get(path[-1], [])):
            if neighbour not in path and neighbour not in avoid:
                stack.append(path + [neighbour])
    return best_chain


def related_concepts(idea_tokens, max_starts=3):
    """
    For up to 3 concepts of the idea that exist in the graph, return
    the BFS neighbours (closest first) and one DFS chain.
    """
    idea_nodes = []
    for token in idea_tokens:
        node = find_node(token)
        if node and node not in idea_nodes:
            idea_nodes.append(node)

    results = []
    for start in idea_nodes[:max_starts]:
        near = [(c, lvl) for c, lvl in bfs(start) if c not in idea_nodes]
        results.append({
            "start": start,
            "level1": [c for c, lvl in near if lvl == 1],
            "level2": [c for c, lvl in near if lvl == 2],
            "chain": dfs(start, avoid=set(idea_nodes) - {start}),
        })
    return results
