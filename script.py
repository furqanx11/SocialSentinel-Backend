import re
from unidecode import unidecode
import json
from app.auth.db import update_fairness_score, add_detected_words


with open(r"hatewords.json", "r") as f:
    keyword_data = json.load(f)
keywords = list(set(unidecode(k.lower()) for k in keyword_data.keys()))
print(f"Loaded {len(keywords)} keywords")


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



async def detect_abuse(text, user_id, embedding_thresh=0.75, update=False):
    original = text
    text = deobfuscate(text)
    text = normalize_text(text)
    
    for kw in keywords:
        if kw in text:
            score = keyword_data[kw]
            await update_fairness_score(user_id, score)
            await add_detected_words(user_id, kw)
            return True, f"Exact match ({kw})", score
   

    return False, "Clean", 0.0
