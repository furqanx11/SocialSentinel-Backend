import re
import faiss
from unidecode import unidecode
from sentence_transformers import SentenceTransformer
from nltk.util import ngrams
import json
from app.auth.db import update_fairness_score, add_detected_words

# embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

with open(r"D:\SocialSentinel\hatewords.json", "r") as f:
    keyword_data = json.load(f)
keywords = list(set(unidecode(k.lower()) for k in keyword_data.keys()))
print(f"Loaded {len(keywords)} keywords")

keyword_embeddings = embedding_model.encode(keywords, normalize_embeddings=True)
index = faiss.IndexFlatIP(keyword_embeddings.shape[1])
index.add(keyword_embeddings)

def deobfuscate(text):
    text = re.sub(r"(\w)(\s+)(\w)", r"\1\3", text) 
    return text

def normalize_text(text):
    text = unidecode(text.lower())
    replacements = {
        '*': 'i',   
        '!': 'i',
        '1': 'i',
        '$': 's',
        '@': 'a',
        '0': 'o',
        '3': 'e',
        '7': 't'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    
    text = re.sub(r"[^\w\s]", "", text)  
    text = re.sub(r"\s+", " ", text).strip()
    return text

def get_ngrams(text, n=2):
    tokens = text.split()
    return [' '.join(gram) for gram in ngrams(tokens, n)]

def embedding_match(text, threshold=0.75):
    query_embedding = embedding_model.encode([text], normalize_embeddings=True)
    scores, indices = index.search(query_embedding, k=1)
    if scores[0][0] >= threshold:
        return True, scores[0][0], keywords[indices[0][0]]
    return False, scores[0][0], None

async def detect_abuse(text, user_id, embedding_thresh=0.75, update=False):
    original = text
    text = deobfuscate(text)
    text = normalize_text(text)
    
    for kw in keywords:
        if kw in text:
            score = keyword_data[kw]
            # if update:
            await update_fairness_score(user_id, score)
            await add_detected_words(user_id, kw)
            return True, f"Exact match ({kw})", score
    phrases = get_ngrams(text, n=2) + get_ngrams(text, n=3)
    for phrase in phrases:
        is_semantic, score, matched_kw = embedding_match(phrase, threshold=embedding_thresh)
        if is_semantic:
            return True, f"Semantic match (~ {matched_kw})", score

    return False, "Clean", 0.0
