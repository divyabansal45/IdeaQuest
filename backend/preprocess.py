"""
preprocess.py  --  Step 1: clean the text.

Syllabus link: Unit II - Text Feature Extraction. This is the preparation
step before Bag of Words and TF-IDF.

NO LEARNING involved. Every step is a fixed rule:
  1. lowercase and keep only letters
  2. remove stopwords ("the", "and", ...) and generic patent words ("method", "apparatus", ...)
  3. stemming: cut word endings so "charging", "charges", "charged" all become "charg"
  4. ontology: replace synonyms by one main word ("car" -> "vehicle")
"""
import re
from collections import Counter, defaultdict

from backend import ontology

STOPWORDS = set("""
about above after again all also an and any are because been before being below between both but
can could did does doing down during each few for from further had has have having her here hers
him his how into its itself just more most nor not now off once only other our out over own same
she should some such than that the their theirs them then there these they this those through too
under until very was were what when where which while who whom why will with would you your
""".split())

# Words that appear in almost every patent and say nothing about the invention.
PATENT_WORDS = set("""
method methods system systems device devices apparatus process processes thereof comprising comprises
comprise includes include including invention present according provided provide using use used said
wherein herein improved improvement improvements novel means manufacture manufacturing unit units
assembly arrangement show shows shown allow allows based provides help helps make makes need needs
want wants also may like one two
""".split())


def simple_stem(word):
    """A very small, rule-based stemmer (cuts common word endings)."""
    if len(word) <= 3:
        return word
    if word.endswith("ies") and len(word) > 4:
        word = word[:-3] + "y"                      # batteries -> battery
    else:
        for suffix in ("ing", "ed", "es", "s"):
            if word.endswith(suffix) and len(word) - len(suffix) >= 3:
                if suffix == "s" and word.endswith("ss"):
                    continue                        # "glass" stays "glass"
                word = word[:-len(suffix)]
                break
    if word.endswith("e") and len(word) > 3:
        word = word[:-1]                            # charge -> charg (matches "charging")
    return word


_STEMMED_PATENT_WORDS = {simple_stem(w) for w in PATENT_WORDS}
_SYNONYM_LOOKUP, _MAIN_WORD_DISPLAY = ontology.build_lookup(simple_stem)
_raw_forms = defaultdict(Counter)   # remembers real words so the web page can show "charge" not "charg"


def tokenize(text):
    """Text -> list of cleaned, stemmed words."""
    tokens = []
    for raw in re.findall(r"[a-z]+", (text or "").lower()):
        if raw in STOPWORDS or raw in PATENT_WORDS:
            continue
        stem = simple_stem(raw)
        if len(stem) < 3 or stem in STOPWORDS or stem in _STEMMED_PATENT_WORDS:
            continue
        _raw_forms[stem][raw] += 1
        tokens.append(stem)
    return tokens


def process(text):
    """Full pipeline: clean + stem + ontology. This is what the other files call."""
    return ontology.normalize(tokenize(text), _SYNONYM_LOOKUP)


def display(token):
    """Turn an internal stem back into a readable word for the web page."""
    if token in _MAIN_WORD_DISPLAY:
        return _MAIN_WORD_DISPLAY[token]
    forms = _raw_forms.get(token)
    if forms:
        return min(forms, key=lambda w: (len(w), -forms[w]))
    return token
