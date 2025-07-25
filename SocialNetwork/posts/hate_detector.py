FORBIDDEN_WORDS = [
    "idiot","debil","nacist","zabijem","smrt","nenavidim","spina","neger"
]
def is_hate_speech(text):
    lower_text = text.lower()
    return any(word in lower_text for word in FORBIDDEN_WORDS)