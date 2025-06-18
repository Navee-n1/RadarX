import spacy
from keybert import KeyBERT
from models import db

nlp = spacy.load("en_core_web_sm")
kw_model = KeyBERT()

def extract_skills(text, top_n=15):
    """
    Extract dynamic, open-domain skills from JD or resume text.
    Returns high-relevance noun phrases and skill terms.
    """
    text = text.strip().replace("\n", " ")
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 3), stop_words='english', top_n=top_n)
    extracted = set()

    # Add spaCy noun chunks
    doc = nlp(text)
    for chunk in doc.noun_chunks:
        if len(chunk.text) > 2 and not chunk.text.lower() in extracted:
            extracted.add(chunk.text.lower())

    # Add KeyBERT results
    for kw, _ in keywords:
        extracted.add(kw.lower())

    return sorted(list(extracted))
