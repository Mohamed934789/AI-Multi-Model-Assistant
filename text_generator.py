import os
from providers import openai_client, validate_text

def generate_text(prompt, client=None):
    prompt = validate_text(prompt)
    client = client if client is not None else openai_client()
    try:
        response = client.chat.completions.create(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), messages=[{"role": "user", "content": prompt}])
        return response.choices[0].message.content or "No text returned"
    except Exception:
        raise RuntimeError("Text generation failed; check provider access and configuration") from None
