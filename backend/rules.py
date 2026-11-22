"""
rules.py  --  Step 4: a mini EXPERT SYSTEM that finds innovation gaps.

Syllabus links: Unit II - Rule Based Systems, Unit IV - Expert System Architecture.

Parts of an expert system and where they are in this file:
  1. Facts            -> build_facts()  : what we know (feature labels, similarity, shared words)
  2. Knowledge base   -> RULES          : hand-written IF-THEN rules
  3. Inference engine -> run_rules()    : checks every rule against the facts and "fires" the matching ones
  4. Explanation      -> the "why" text : tells the user WHICH rule fired and why

The rules are written by a person, so nothing is learned from data.
"""

MIN_PATENTS_FOR_SUGGESTION = 2   # R4: a word must be in at least 2 similar patents
VERY_SIMILAR = 0.5               # R5
NO_MATCH = 0.15                  # R6


def build_facts(comparison, top_patents, mode="hardware"):
    """Collect everything the rules need to look at."""
    return {
        "features": comparison["features"],
        "candidates": comparison["candidates"],
        "top_n": len(top_patents),
        "thing": "patent" if mode == "hardware" else "product",
        "things": "patents" if mode == "hardware" else "products",
        "top_score": top_patents[0]["score"] if top_patents else 0.0,
        "top_title": top_patents[0]["title"] if top_patents else "",
    }


# Each rule: id, what kind of message it gives, which fact it looks at,
# the IF condition, the THEN message and the WHY explanation.
RULES = [
    {
        "id": "R1", "kind": "novelty", "applies_to": "feature",
        "condition": lambda f, facts: f["label"] == "Unexplored",
        "then": lambda f, facts: (
            (f"None of the {facts['top_n']} similar {facts['things']} offers '{f['name']}'. "
             if f.get("count", 0) == 0 else
             f"Only {f['count']} of {facts['top_n']} similar {facts['things']} offers '{f['name']}'. ")
            + "This could be what makes your idea different."),
        "why": lambda f, facts: (
            f"IF feature '{f['name']}' is Unexplored (match score {f['score']:.2f}) "
            f"THEN mark it as possible novelty."),
    },
    {
        "id": "R2", "kind": "note", "applies_to": "feature",
        "condition": lambda f, facts: f["label"] == "Partial",
        "then": lambda f, facts: (
            f"'{f['name']}' is offered by {f.get('count', 0)} of {facts['top_n']} similar {facts['things']}. "
            f"Add more detail (how, where, for whom) to make your version different."),
        "why": lambda f, facts: (
            f"IF feature '{f['name']}' is Partial (match score {f['score']:.2f}) "
            f"THEN suggest adding more detail."),
    },
    {
        "id": "R3", "kind": "note", "applies_to": "feature",
        "condition": lambda f, facts: f["label"] == "Existing",
        "then": lambda f, facts: (
            f"'{f['name']}' is already offered by {f.get('count', 0)} of {facts['top_n']} similar {facts['things']}, "
            f"so do not present it as new."),
        "why": lambda f, facts: (
            f"IF feature '{f['name']}' is Existing (match score {f['score']:.2f}) "
            f"THEN warn that it is not new."),
    },
    {
        "id": "R4", "kind": "gap", "applies_to": "candidate",
        "condition": lambda c, facts: c["count"] >= MIN_PATENTS_FOR_SUGGESTION,
        "then": lambda c, facts: (
            f"Consider adding '{c['name']}'. It is offered by {c['count']} of "
            f"{facts['top_n']} similar {facts['things']} but is not part of your idea."),
        "why": lambda c, facts: (
            f"IF '{c['name']}' is in {c['count']} similar {facts['things']} (at least "
            f"{MIN_PATENTS_FOR_SUGGESTION}) AND is missing from your idea "
            f"THEN suggest it as an improvement."),
    },
    {
        "id": "R5", "kind": "warning", "applies_to": "overall",
        "condition": lambda facts, f2: facts["top_score"] >= VERY_SIMILAR,
        "then": lambda facts, f2: (
            f"A very similar {facts['thing']} exists: \"{facts['top_title']}\". "
            f"Study it and find what makes your idea different."),
        "why": lambda facts, f2: (
            f"IF top similarity is {facts['top_score']:.2f} (at least {VERY_SIMILAR}) "
            f"THEN warn about a very close match."),
    },
    {
        "id": "R6", "kind": "warning", "applies_to": "overall",
        "condition": lambda facts, f2: facts["top_score"] < NO_MATCH,
        "then": lambda facts, f2: (
            "No close match was found in our data. Your idea may be new, "
            "or our data may not cover this area yet."),
        "why": lambda facts, f2: (
            f"IF top similarity is {facts['top_score']:.2f} (below {NO_MATCH}) "
            f"THEN say that no close match exists."),
    },
]

KIND_ORDER = {"warning": 0, "gap": 1, "novelty": 2, "note": 3}


def run_rules(facts):
    """Inference engine: test every rule on the facts and collect the ones that fire."""
    conclusions = []
    for rule in RULES:
        if rule["applies_to"] == "feature":
            items = facts["features"]
        elif rule["applies_to"] == "candidate":
            items = facts["candidates"]
        else:
            items = [facts]

        for item in items:
            if rule["condition"](item, facts):
                conclusions.append({
                    "rule": rule["id"],
                    "kind": rule["kind"],
                    "text": rule["then"](item, facts),
                    "why": rule["why"](item, facts),
                })

    conclusions.sort(key=lambda c: KIND_ORDER[c["kind"]])
    return conclusions
