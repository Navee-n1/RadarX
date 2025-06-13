from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    return model.encode([text])[0]

def compute_similarity(jd_text, resumes):
    jd_embedding = get_embedding(jd_text)
    results = []

    for name, resume_text in resumes.items():
        res_embedding = get_embedding(resume_text)
        score = cosine_similarity([jd_embedding], [res_embedding])[0][0]
        results.append((name, score))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:3]
