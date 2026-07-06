from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
load_dotenv()

client = InferenceClient(token=os.getenv("HUGGINGFACE_API_KEY"))

def summarize_text(text: str):
    
    response=client.summarization(text, model="facebook/bart-large-cnn")

    return response.summary_text

