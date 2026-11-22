"""
features.py  --  A small KNOWLEDGE BASE of product and invention features.

Syllabus link: Unit II - Knowledge representation (ontology of features) and
rule-based matching.

Single words are not very useful to the user ("home", "live"). People think in
FEATURES such as "Home tutoring" or "Live classes". This file lists many such
features. Each feature has a readable name and one or more trigger patterns.
A pattern is a group of words that must ALL be present, for example
"home tutor" means the text must contain both "home" and "tutor".

The same cleaning steps (stemming, synonyms) are applied to the patterns, so
"tutors", "tutoring" and "tutor" all match.

Nothing is learned. The list is written by hand and can be extended by adding
a line to FEATURES.
"""
from backend import preprocess

# (feature name, [trigger patterns])
FEATURES = [
    # ---- education ----
    ("Tutoring", ["tutor", "tutoring", "tuition"]),
    ("Home tutoring (tutor visits the student)", ["home tutor", "home tuition"]),
    ("Live classes", ["live class", "live lecture", "live session", "live tutoring", "live video"]),
    ("Recorded video lessons", ["video lesson", "video lecture", "recorded", "video solution", "video course"]),
    ("Exam preparation", ["exam", "jee", "neet", "upsc", "competitive"]),
    ("Doubt solving", ["doubt"]),
    ("Practice tests and quizzes", ["test series", "mock test", "quiz", "practice question", "practice test"]),
    ("School students", ["school"]),
    ("Courses and certificates", ["certification", "certificate", "degree", "course"]),
    ("Coding and tech skills", ["coding", "programming", "software engineering"]),
    ("Free learning content", ["free lesson", "free lecture", "free course", "free learning"]),
    # ---- language ----
    ("Pronunciation audio", ["pronunciation", "audio"]),
    ("Translation", ["translation"]),
    ("Word meanings and dictionary", ["meaning", "dictionary"]),
    ("Voice assistant or speech recognition", ["voice assistant", "speech recognition", "voice bot"]),
    ("Indian languages", ["indian language", "hindi", "regional language"]),
    ("Spoken language practice", ["conversation practice", "speaking practice", "spoken english"]),
    ("Chatbot", ["chatbot", "chat bot"]),
    ("Multi-language support", ["language"]),
    # ---- health ----
    ("Doctor consultation", ["doctor consultation", "online consultation", "doctor consult", "telemedicine", "doctor"]),
    ("Appointment booking", ["appointment"]),
    ("Medicine delivery", ["medicine delivery", "pharmacy", "medicine"]),
    ("Lab tests", ["lab test", "diagnostic"]),
    ("Health records", ["health record", "medical record"]),
    ("Fitness and diet", ["fitness", "diet", "calorie", "workout"]),
    ("Mental health support", ["mental health", "counselling", "emotional wellness"]),
    # ---- money ----
    ("UPI payments", ["upi"]),
    ("Bill payments and recharge", ["bill payment", "recharge", "pay bill"]),
    ("Payment gateway for businesses", ["payment gateway", "accept online payment"]),
    ("Investing and stock trading", ["invest", "stock", "mutual fund", "trading"]),
    ("Loans", ["loan"]),
    ("Insurance", ["insurance"]),
    ("Tax and GST filing", ["tax", "gst"]),
    ("Accounting and billing", ["accounting", "invoice", "billing"]),
    ("Digital wallet", ["wallet"]),
    # ---- shopping and delivery ----
    ("Online shopping marketplace", ["shopping", "marketplace", "online store"]),
    ("Quick delivery", ["quick delivery", "minute delivery", "ten minute", "delivery in minutes"]),
    ("Food delivery", ["food delivery", "restaurant"]),
    ("Grocery delivery", ["grocery"]),
    ("Home delivery", ["delivery"]),
    ("Selling to buyers directly", ["sell buyer", "sell directly", "sell crop", "sell fresh produce"]),
    ("Used items buying and selling", ["classified", "used product", "used car", "used item"]),
    # ---- travel ----
    ("Ticket booking", ["ticket", "flight", "bus ticket", "train"]),
    ("Hotel booking", ["hotel"]),
    ("Cab and ride booking", ["cab", "ride", "taxi", "bike taxi"]),
    ("Holiday and trip planning", ["holiday", "trip", "travel"]),
    # ---- jobs and work ----
    ("Job search", ["job"]),
    ("Internships", ["internship"]),
    ("Resume and profile", ["resume"]),
    # ---- home and local ----
    ("Home services at your door", ["home service", "cleaning", "repair", "salon"]),
    ("Property buying and renting", ["property", "rent", "real estate"]),
    ("Local business search", ["local business", "nearby", "local service"]),
    ("Matrimony and profiles", ["matrimony", "life partner"]),
    # ---- agriculture ----
    ("Crop advice", ["crop advice", "farming advice", "crop"]),
    ("Market prices", ["market price", "price"]),
    ("Weather forecast", ["weather", "forecast"]),
    ("Farm inputs (seeds, fertilizer)", ["seed", "fertilizer", "farm input"]),
    # ---- media, social, government ----
    ("Short videos", ["short video"]),
    ("Music and audio streaming", ["music", "song", "podcast"]),
    ("Video and movie streaming", ["streaming", "movie", "show"]),
    ("Audiobooks and stories", ["audiobook", "story", "novel"]),
    ("News", ["news"]),
    ("Chat and messaging", ["messaging", "chat"]),
    ("Fantasy and mobile games", ["fantasy", "game", "gaming"]),
    ("Government services", ["government", "govt"]),
    ("Digital documents", ["digital document", "certificate storage", "documents"]),
    # ---- physical inventions ----
    ("Solar power", ["solar"]),
    ("Battery and charging", ["battery", "charging"]),
    ("Electric vehicle", ["electric vehicle"]),
    ("Vehicle", ["vehicle"]),
    ("Engine and fuel", ["engine", "fuel"]),
    ("Motor drive", ["motor"]),
    ("Sensor-based monitoring", ["sensor"]),
    ("Water purification", ["water purification", "purification"]),
    ("Filtration", ["filter", "filtration", "membrane"]),
    ("Wireless connectivity", ["wireless", "bluetooth"]),
    ("Display or indicator", ["display", "indicator"]),
    ("Lighting (LED)", ["light", "led"]),
    ("Heating or cooling", ["heat", "heater", "cooling", "refrigeration"]),
    ("Drying", ["dry", "drying", "dryer"]),
    ("Spraying", ["spray", "sprayer"]),
    ("Conveyor belt", ["conveyor"]),
    ("Food processing", ["food"]),
    ("Packaging", ["packaging"]),
    ("Textile and fabric", ["textile", "fabric", "fibre", "fiber"]),
    ("Bag", ["bag"]),
    ("Tyre", ["tyre", "tire"]),
    ("Sterilization and patient care", ["sterilization", "patient"]),
    ("Agriculture equipment", ["agriculture", "irrigation"]),
    ("Pump", ["pump"]),
    ("Camera", ["camera"]),
    ("Alarm and security", ["alarm", "lock", "security"]),
    ("Wearable", ["wearable"]),
]


def _compile():
    """Turn every trigger text into a set of cleaned word stems."""
    compiled = []
    for name, patterns in FEATURES:
        groups = []
        for pattern in patterns:
            words = set(preprocess.process(pattern))
            if words:
                groups.append(frozenset(words))
        compiled.append((name, groups))
    return compiled


_COMPILED = _compile()


def match(tokens):
    """Return the feature names whose trigger words are all present in 'tokens'."""
    tokens = set(tokens)
    return [name for name, groups in _COMPILED if any(g <= tokens for g in groups)]
