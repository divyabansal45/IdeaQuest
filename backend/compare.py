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

from backend import preprocess

MIN_PATENTS_FOR_CANDIDATE = 2   # a word must appear in at least 2 top patents
MAX_CANDIDATES = 8


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

    # unique features, keeping the order they were written in
    unique_features = []
    for token in idea_tokens:
        if token not in unique_features:
            unique_features.append(token)

    total_similarity = sum(p["score"] for p in top_patents)

    features = []
    for token in unique_features:
        matched = sum(p["score"] for p in top_patents if token in p["tokens"])
        score = matched / total_similarity if total_similarity > 0 else 0.0
        label, degree = fuzzy_label(score)
        features.append({
            "name": preprocess.display(token),
            "score": round(score, 2),
            "label": label,
            "degree": round(degree, 2),
        })

    # words that similar patents share but the idea does not mention
    idea_set = set(idea_tokens)
    counts = Counter()
    for patent in top_patents:
        counts.update(patent["tokens"])      # tokens is a set -> counts patents, not repeats
    candidates = [
        {"name": preprocess.display(token), "count": count}
        for token, count in counts.items()
        if count >= MIN_PATENTS_FOR_CANDIDATE and token not in idea_set
    ]
    candidates.sort(key=lambda c: (-c["count"], c["name"]))

    return {
        "features": features,
        "candidates": candidates[:MAX_CANDIDATES],
        "titles_only": sum(1 for p in top_patents if not p["abstract"]),
    }
