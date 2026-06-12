from ai.classifier import classify

def test_classify_basic():
    text = "There is a fire in the building"
    result = classify(text)

    assert result is not None