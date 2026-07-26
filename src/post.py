import re


def clean_bio(text, max_sentences=3):
    """Limit to N sentences, remove repeated sentences, tidy whitespace."""
    
    text = re.sub(r"\s+", " ", text).strip()


    sentences = re.split(r"(?<=[.!?]) +", text)

   
    seen = set()
    unique_sentences = []
    for s in sentences:
        s_clean = s.strip()
        if s_clean and s_clean.lower() not in seen:
            seen.add(s_clean.lower())
            unique_sentences.append(s_clean)

   
    limited = unique_sentences[:max_sentences]

    return " ".join(limited)