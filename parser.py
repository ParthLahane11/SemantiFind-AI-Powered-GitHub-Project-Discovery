import spacy
from word2number import w2n
from typing import Tuple, Optional

nlp = spacy.load("en_core_web_sm")

CATEGORIES = [
    "machine learning", "web development", "devops",
    "mobile development", "security", "data science", "healthtech",
    "ai", "blockchain", "game development"
]

METRICS_MAP = {
    "popular": "popularity_score",
    "star": "stargazers_count",
    "watch": "watchers_count",
    "fork": "forks_count",
    "recent": "updated_at",
    "new": "created_at"
}

def extract_k_category_metric(query: str) -> Tuple[int, Optional[str], Optional[str]]:
    doc = nlp(query.lower())
    k = 5
    category = None
    metric = None

    for token in doc:
        if token.pos_ == "NUM":
            try:
                k = int(token.text)
                break
            except ValueError:
                try:
                    k = w2n.word_to_num(token.text)
                    break
                except:
                    continue

    for cat in CATEGORIES:
        if cat in query.lower():
            category = cat
            break

    for keyword, field in METRICS_MAP.items():
        if keyword in query.lower():
            metric = field
            break

    return k, category, metric