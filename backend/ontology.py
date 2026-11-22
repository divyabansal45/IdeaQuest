"""
ontology.py  --  A small hand-made ontology (synonym groups).

Syllabus link: Unit II - Ontology, WordNet / ConceptNet as knowledge
representation tools.

Idea: different words can mean the same thing. "car" and "automobile" should
count as ONE concept, otherwise TF-IDF treats them as two unrelated words.
Each group below has a main (canonical) word and its synonyms. Every synonym
is replaced by the main word before we search or compare.

This is NOT learned from data. A person wrote it, so you can add your own
groups. It plays the same role WordNet plays in a bigger system.
"""

GROUPS = {
    "vehicle":      ["car", "automobile", "motorcar", "auto", "automotive"],
    "bag":          ["backpack", "rucksack", "satchel", "handbag"],
    "battery":      ["accumulator", "powerpack"],
    "solar":        ["photovoltaic", "pv", "sunlight"],
    "phone":        ["smartphone", "cellphone", "handset"],
    "purification": ["purifier", "purify", "filtration", "filter"],
    "sensor":       ["detector", "transducer"],
    "display":      ["screen", "monitor"],
    "wireless":     ["cordless"],
    "agriculture":  ["farming", "farm", "agricultural"],
    "textile":      ["fabric", "cloth", "clothing", "garment", "apparel"],
    "tyre":         ["tire"],
    "electric":     ["electrical", "electricity"],
    "light":        ["lamp", "led", "illumination"],
    "heat":         ["thermal"],
    "medical":      ["healthcare"],
    "voice":        ["speech", "audio", "spoken", "pronunciation", "speak", "speaking"],
    "website":      ["web", "webpage", "portal", "site"],
    "app":          ["application", "apps"],
    "language":     ["languages", "vernacular", "bhasha"],
    "translation":  ["translate", "translator", "translating"],
}


def build_lookup(stem_function):
    """
    Builds a table  synonym -> main word.
    Words are stemmed first (see preprocess.py) so that "cars" also matches "car".
    Also returns a table to show the main word nicely on the web page.
    """
    lookup = {}
    display = {}
    for main_word, synonyms in GROUPS.items():
        main_stem = stem_function(main_word)
        display[main_stem] = main_word
        for word in synonyms:
            lookup[stem_function(word)] = main_stem
    return lookup, display


def normalize(tokens, lookup):
    """Replace every synonym by its main word."""
    return [lookup.get(token, token) for token in tokens]
