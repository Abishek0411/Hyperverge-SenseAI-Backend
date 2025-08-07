# src/api/services/similarity_check.py

import difflib

# Dummy list of known answers or plagiarized content samples
REFERENCE_ANSWERS = [
    "The mitochondria is the powerhouse of the cell.",
    "A linked list is a linear data structure where elements are not stored at contiguous memory locations.",
    "Machine learning is a subset of AI that allows systems to learn from data."
]

def check_similarity(answer_text):
    highest_similarity = 0  
    best_match = None

    for ref in REFERENCE_ANSWERS:
        similarity = difflib.SequenceMatcher(None, ref, answer_text).ratio()
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = ref

    if highest_similarity > 0.85:
        return {
            "flag": True,
            "confidence": round(highest_similarity, 2),
            "evidence": f"Similar to known answer: \"{best_match}\""
        }

    return {
        "flag": False,
        "confidence": round(highest_similarity, 2),
        "evidence": "No strong similarity detected"
    }
