"""
compare.py  --  Step 3: compare the idea with the similar patents, feature by feature.

Syllabus link: Unit III - Fuzzy Logic (handling uncertainty).

A "feature" here is an important word/concept of the idea (after cleaning).

For each feature we calculate a MATCH SCORE between 0 and 1:

    match score = (sum of similarity of top patents that contain the feature)
                  / (sum of similarity of all top patents)

    1.0 -> every similar patent has it     0.0 -> none of them has it

Real life is not "yes or no", so we use FUZZY membership functions.
A score can belong a little to "Partial" and a little to "Existing" at once.
The label with the HIGHEST membership degree wins:

    Unexplored : full (1.0) up to score 0.1, falls to 0 at 0.3
    Partial    : triangle, starts at 0.1, peaks at 0.4, ends at 0.7
    Existing   : starts at 0.4, full (1.0) from 0.7

We also find "candidate features": words that appear in at least 2 of the top
patents but are missing from the idea. rules.py turns them into suggestions.

No learning is involved. The thresholds are chosen by us.
"""
from collections import Counter

from backend import features as kb
from backend import preprocess

MIN_PATENTS_FOR_CANDIDATE = 2   # a word must appear in at least 2 top patents
MAX_CANDIDATES = 8

# Very generic words that should not be suggested as "features to add".
GENERIC_CANDIDATES = {preprocess.simple_stem(w) for w in
                      "online platform service services digital indian india free app apps website portal".split()}


# ---- fuzzy membership functions (each returns a number between 0 and 1) ----
def mu_unexplored(x):
    if x <= 0.1:
        return 1.0
    if x >= 0.3:
        return 0.0
    return (0.3 - x) / 0.2


def mu_partial(x):
    if x <= 0.1 or x >= 0.7:
        return 0.0
    if x <= 0.4:
        return (x - 0.1) / 0.3
    return (0.7 - x) / 0.3


def mu_existing(x):
    if x <= 0.4:
        return 0.0
    if x >= 0.7:
        return 1.0
    return (x - 0.4) / 0.3


def fuzzy_label(score):
    """Pick the label with the highest membership degree. Ties go to 'Partial'."""
    degrees = {
        "Partial": mu_partial(score),
        "Existing": mu_existing(score),
        "Unexplored": mu_unexplored(score),
    }
    best = "Partial"
    for label, degree in degrees.items():
        if degree > degrees[best]:
            best = label
    return best, degrees[best]


def compare_features(idea_text, top_patents):
    idea_tokens = preprocess.process(idea_text)

    # unique words of the idea, keeping the order they were written in
    unique_features = []
    for token in idea_tokens:
        if token not in unique_features:
            unique_features.append(token)

    total_similarity = sum(p["score"] for p in top_patents)

    # ---------- 1. word level match (the basic numbers) ----------
    word_features = []
    for token in unique_features:
        matched = sum(p["score"] for p in top_patents if token in p["tokens"])
        count = sum(1 for p in top_patents if token in p["tokens"])
        score = matched / total_similarity if total_similarity > 0 else 0.0
        label, degree = fuzzy_label(score)
        word_features.append({
            "name": preprocess.display(token), "score": round(score, 2),
            "label": label, "degree": round(degree, 2), "count": count,
        })

    # words that similar patents share but the idea does not mention
    idea_set = set(idea_tokens)
    word_counts = Counter()
    for patent in top_patents:
        # tokens is a set -> counts patents, not repeats; the category label is not a feature
        word_counts.update(patent["tokens"] - patent.get("skip", set()))
    word_candidates = [
        {"name": preprocess.display(token), "count": count}
        for token, count in word_counts.items()
        if count >= MIN_PATENTS_FOR_CANDIDATE and token not in idea_set
        and token not in GENERIC_CANDIDATES
    ]
    word_candidates.sort(key=lambda c: (-c["count"], c["name"]))

    # ---------- 2. feature level match (what the user actually cares about) ----------
    # features.py turns words into readable features such as "Home tutoring".
    idea_labels = kb.match(idea_set)
    for patent in top_patents:
        patent["labels"] = kb.match(patent["tokens"])

    concept_features = []
    for name in idea_labels:
        owners = [p for p in top_patents if name in p["labels"]]
        score = sum(p["score"] for p in owners) / total_similarity if total_similarity > 0 else 0.0
        label, degree = fuzzy_label(score)
        concept_features.append({
            "name": name, "score": round(score, 2),
            "label": label, "degree": round(degree, 2), "count": len(owners),
        })

    label_counts = Counter()
    for patent in top_patents:
        label_counts.update(set(patent["labels"]))
    concept_candidates = [
        {"name": name, "count": count}
        for name, count in label_counts.items()
        if count >= MIN_PATENTS_FOR_CANDIDATE and name not in idea_labels
    ]
    concept_candidates.sort(key=lambda c: (-c["count"], c["name"]))

    concept_mode = len(concept_features) > 0

    # For every similar item: what it offers and what the idea adds that it does NOT offer.
    for patent in top_patents:
        if concept_mode:
            mine = [n for n in idea_labels if n in patent["labels"]]
            others = [n for n in patent["labels"] if n not in idea_labels]
            patent["offers"] = (mine + others)[:6]
            patent["lacks"] = [n for n in idea_labels if n not in patent["labels"]]
        else:
            patent["offers"] = [preprocess.display(t) for t in unique_features if t in patent["tokens"]]
            patent["lacks"] = [preprocess.display(t) for t in unique_features if t not in patent["tokens"]]

    return {
        "concept_mode": concept_mode,
        "features": concept_features if concept_mode else word_features,
        "candidates": (concept_candidates if concept_mode else word_candidates)[:MAX_CANDIDATES],
        "word_features": word_features,
        "titles_only": sum(1 for p in top_patents if not p["abstract"]),
    }
