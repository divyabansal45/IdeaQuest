# IdeaQuest: AI-Based Patent Discovery and Innovation Gap Analysis

The user describes an invention. IdeaQuest finds similar Indian patents, compares the
features of the idea with them, and suggests innovation gaps.

## How to run

```
pip3 install flask
python3 app.py
```
Open http://127.0.0.1:5000 in the browser.

## Folder structure

```
IdeaQuest/
├── app.py                    Flask server (connects the web page to the AI files)
├── requirements.txt
├── data/                     Lens.org CSV exports (raw data)
├── backend/
│   ├── prepare_data.py       merges data/*.csv into indian_patents.csv
│   ├── indian_patents.csv    the patent dataset used by the app
│   ├── make_software_data.py builds indian_software.csv (hand-written list of Indian apps and websites)
│   ├── indian_software.csv   dataset for the website/app mode
│   ├── preprocess.py         text cleaning, stopwords, stemming
│   ├── ontology.py           synonym groups
│   ├── concept_graph.py      related concepts with BFS and DFS
│   ├── search.py             Bag of Words, TF-IDF, cosine similarity, ranking
│   ├── compare.py            feature comparison with fuzzy logic
│   └── rules.py              rule-based expert system
└── frontend/
    ├── base.html             shared header and footer
    ├── home.html             home page
    ├── analyze.html          page where the user types the idea
    ├── results.html          results page
    ├── how_it_works.html     explains every step and the syllabus topic
    ├── about.html            project, data and limits
    └── style.css             design (beige and green theme)
```

## Two modes

The check page has a switch. "Physical invention" searches Indian patents. "Website or app" searches a hand-made list of Indian apps, websites and startups (software is rarely patented in India, so patents cannot answer that question). Both modes use the same TF-IDF, fuzzy logic and rules. To add more products, edit the list in `backend/make_software_data.py` and run it.

## Flow

Idea -> preprocess.py -> search.py (top 5 patents) -> compare.py (feature labels)
-> rules.py (gaps and suggestions) -> results.html

## Syllabus mapping

| Part of project | File | Syllabus topic |
|---|---|---|
| Bag of Words, TF-IDF | search.py | Unit II: Text Feature Extraction |
| Similar patent ranking | search.py | Unit IV: Information Retrieval |
| Related concepts | concept_graph.py | Unit I: Search, BFS, DFS |
| Synonym groups | ontology.py | Unit II: Ontology, WordNet |
| Existing / Partial / Unexplored | compare.py | Unit III: Fuzzy Logic |
| Gaps and suggestions | rules.py | Unit II: Rule Based Systems, Unit IV: Expert System Architecture |
| Disclaimer on the pages | index.html, results.html | Unit IV: Ethics in AI |

## Why this is NOT machine learning

- Nothing is trained. There are no weights, no training data, no accuracy score.
- TF-IDF and cosine similarity are fixed formulas.
- Fuzzy thresholds and IF-THEN rules are written by hand.
- The CSV is a document collection to search in (like a search engine index), not training data.
- Same input always gives the same output.

## Adding more patents

1. Export CSV files from lens.org (Jurisdiction = India, Granted Patent).
2. Put them in the `data/` folder.
3. Run `python backend/prepare_data.py`, then restart `python app.py`.

Patents that have an abstract give much better results than title-only patents.

## Limitations (say these in the viva)

- The system only searches the patents in the dataset. It is not a live patent database.
- Many older patents have only a title, so their feature comparison is rough.
- Words are matched by stem and by the small ontology, so it does not understand meaning like a human.
- It gives guidance only. It cannot say whether an idea is patentable.
