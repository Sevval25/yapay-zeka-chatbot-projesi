import re

def preprocess_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9çğıöşüÇĞİÖŞÜ\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
