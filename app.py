"""
app.py  --  The web server (Flask). It only connects the web pages to the AI files.

Pages:
    /               home page
    /analyze        form (GET) and results (POST)
    /how-it-works   explains every step and the syllabus topic
    /about          project, data and limits

Check flow:  form -> /analyze -> backend files -> results page
    1. search.find_similar()      finds similar patents      (TF-IDF + cosine)
    2. compare.compare_features() labels each feature         (fuzzy logic)
    3. rules.run_rules()          finds gaps and suggestions  (expert system)
    4. concept_graph.related_concepts()  related ideas         (BFS and DFS)

Run:  python3 app.py      then open  http://127.0.0.1:5000
"""
from flask import Flask, render_template, request

from backend import compare, concept_graph, preprocess, rules, search

# The HTML and CSS files live in the "frontend" folder.
app = Flask(__name__, template_folder="frontend", static_folder="frontend", static_url_path="/static")

search.load_data()   # builds the TF-IDF index once when the server starts

MIN_WORDS = 4
MAX_CHARS = 1000


def build_stats():
    """Simple counts about the dataset, shown on the pages."""
    years = [int(p["year"]) for p in search.PATENTS if p["year"].isdigit()]
    return {
        "total": len(search.PATENTS),
        "software_total": len(search.INDEXES["software"].items),
        "with_abstract": sum(1 for p in search.PATENTS if p["abstract"]),
        "first_year": min(years) if years else "",
        "last_year": max(years) if years else "",
    }


STATS = build_stats()


@app.context_processor
def inject_stats():
    return {"stats": STATS}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "GET":
        return render_template("analyze.html", error=None, idea="", mode="hardware")

    idea = request.form.get("idea", "").strip()[:MAX_CHARS]
    if len(idea.split()) < MIN_WORDS:
        return render_template(
            "analyze.html", idea=idea, mode=request.form.get("mode", "hardware"),
            error=f"Describe your idea in at least {MIN_WORDS} words, for example what it is and what it does.")

    mode = request.form.get("mode", "hardware")
    if mode not in search.INDEXES:
        mode = "hardware"

    similar = search.find_similar(idea, mode=mode, top_n=5)
    comparison = compare.compare_features(idea, similar)
    facts = rules.build_facts(comparison, similar, mode)
    conclusions = rules.run_rules(facts)
    related = concept_graph.related_concepts(preprocess.process(idea))

    return render_template(
        "results.html", idea=idea, patents=similar, mode=mode,
        comparison=comparison, conclusions=conclusions, related=related)


@app.route("/how-it-works")
def how_it_works():
    return render_template("how_it_works.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=False)   # set debug=True only while you are editing the code
