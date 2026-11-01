from providers import hf_client, validate_text

def summarize_text(text, client=None):
    text = validate_text(text)
    client = client if client is not None else hf_client()
    try:
        return client.summarization(text, model="facebook/bart-large-cnn").summary_text
    except Exception:
        raise RuntimeError("Summarization failed; check model availability and provider access") from None
