def classify(text):
    text = text.lower()

    if "trapped" in text:
        return "Critical"
    elif "flood" in text:
        return "High"
    elif "fire" in text:
        return "High"
    elif "earthquake" in text:
        return "High"
    elif "storm" in text:
        return "Medium"
    else:
        return "Low"