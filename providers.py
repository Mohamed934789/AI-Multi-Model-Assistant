"""Lazy provider clients; importing handlers never requires a key or network."""
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).with_name(".env.local"), override=False)

def require_key(name):
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"Set {name} in your environment or .env.local")
    return value

def openai_client():
    from openai import OpenAI
    return OpenAI(api_key=require_key("OPENAI_API_KEY"), timeout=45, max_retries=1)

def hf_client():
    from huggingface_hub import InferenceClient
    return InferenceClient(token=require_key("HUGGINGFACE_API_KEY"), timeout=45)

def validate_text(text, maximum=20000):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Enter nonempty text")
    if len(text) > maximum:
        raise ValueError(f"Text exceeds the {maximum}-character limit")
    return text.strip()
