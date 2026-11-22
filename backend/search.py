"""
search.py  --  Step 2: find similar patents or software products (Information Retrieval).

Syllabus links:
  Unit II : Bag of Words (BoW) and TF-IDF
  Unit IV : Information Retrieval (ranking documents for a query)

How it works (no machine learning, nothing is trained):
  1. Every patent is turned into a Bag of Words = how many times each word appears.
  2. Each word gets a TF-IDF weight:
         TF  = (times word appears in this patent) / (total words in this patent)
         IDF = log( total patents / patents containing the word )
         TF-IDF = TF x IDF
     Common words get a LOW weight, rare/specific words get a HIGH weight.
  3. The user's idea is turned into a TF-IDF vector the same way.
  4. Cosine similarity compares the idea with every patent:
         cosine = (A . B) / (|A| x |B|)       -> a number from 0 to 1
  5. Patents are sorted by this number and the top 5 are returned.

Same input always gives the same output. Nothing is learned.
"""
import csv
import math
import os
from collections import Counter

from backend import preprocess

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(HERE, "indian_patents.csv")
SOFTWARE_FILE = os.path.join(HERE, "indian_software.csv")


def bag_of_words(tokens):
    """BoW: word -> how many times it appears."""
    return Counter(tokens)


def tf_idf_vector(tokens, idf):
    """TF-IDF vector as a dictionary {word: weight}."""
    if not tokens:
        return {}
    bow = bag_of_words(tokens)
    total_words = len(tokens)
    return {word: (count / total_words) * idf[word]
            for word, count in bow.items() if word in idf}


def vector_length(vector):
    return math.sqrt(sum(w * w for w in vector.values()))


def read_patents(path):
    """Patent CSV -> rows with the common keys: title, abstract, label, year, ..."""
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            row["label"] = row["patent_no"]
            row["text"] = (row["title"] + " ") * 2 + row["abstract"]    # title counts double
            yield row


def read_software(path):
    """Software CSV -> rows with the same common keys, so the rest of the code is shared."""
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            row["title"] = row["name"]
            row["abstract"] = row["description"]
            row["label"] = row["category"]
            row["applicant"] = ""
            row["status"] = ""
            row["url"] = ""
            row["text"] = row["name"] + " " + row["category"] + " " + row["description"]
            yield row


class Index:
    """A TF-IDF index over one collection (patents or software products)."""

    def __init__(self):
        self.items = []        # rows
        self.idf = {}          # word -> IDF value
        self.vectors = []      # one TF-IDF vector per item
        self.norms = []        # length of each vector (needed for cosine)

    def load(self, rows):
        documents = []
        for row in rows:
            tokens = preprocess.process(row["text"])
            if not tokens:
                continue
            row["tokens"] = set(tokens)   # used later in compare.py
            if row.get("category"):       # the category label (e.g. "Education") is not a real feature
                row["skip"] = set(preprocess.process(row["category"]))
            self.items.append(row)
            documents.append(tokens)
        if not documents:
            raise RuntimeError("No data loaded.")

        total_docs = len(documents)
        doc_freq = Counter()              # in how many items does each word appear?
        for tokens in documents:
            doc_freq.update(set(tokens))
        self.idf = {word: math.log(total_docs / count) for word, count in doc_freq.items()}

        for tokens in documents:
            vector = tf_idf_vector(tokens, self.idf)
            self.vectors.append(vector)
            self.norms.append(vector_length(vector))

    def find_similar(self, idea_text, top_n=5):
        """Return the top_n most similar items (each with a 'score' between 0 and 1)."""
        query_vector = tf_idf_vector(preprocess.process(idea_text), self.idf)
        query_norm = vector_length(query_vector)
        if query_norm == 0:
            return []

        scored = []
        for index, (vector, norm) in enumerate(zip(self.vectors, self.norms)):
            if norm == 0:
                continue
            dot = sum(weight * vector.get(word, 0.0) for word, weight in query_vector.items())
            if dot > 0:
                scored.append((dot / (query_norm * norm), index))

        scored.sort(reverse=True)
        results = []
        for score, index in scored[:top_n]:
            item = dict(self.items[index])
            item["score"] = score
            results.append(item)
        return results


INDEXES = {"hardware": Index(), "software": Index()}
PATENTS = INDEXES["hardware"].items     # kept so app.py can count patents


def load_data():
    """Build both indexes. Called once when the app starts."""
    INDEXES["hardware"].load(read_patents(DATA_FILE))
    INDEXES["software"].load(read_software(SOFTWARE_FILE))


def find_similar(idea_text, mode="hardware", top_n=5):
    return INDEXES[mode].find_similar(idea_text, top_n)
