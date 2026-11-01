from providers import hf_client, validate_text

def analyze_sentiment(text, client=None):
    text = validate_text(text)
    client = client if client is not None else hf_client()
    try:
        predictions = client.text_classification(text, model="cardiffnlp/twitter-roberta-base-sentiment-latest")
        if not predictions: raise ValueError("No labels")
        return max(predictions, key=lambda item: item.score).label
    except Exception:
        raise RuntimeError("Sentiment request failed; check model availability and provider access") from None
