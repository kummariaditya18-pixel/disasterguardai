def classify(text):
    text = text.lower()

    if "fire" in text:
        return "fire"
    if "flood" in text:
        return "flood"
    if "earthquake" in text:
        return "earthquake"

    return "unknown"
