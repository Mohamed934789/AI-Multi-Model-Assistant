import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
load_dotenv()
print("Token loaded:", os.getenv("HUGGINGFACE_API_KEY"))
client = InferenceClient(
    provider="hf-inference",
    token = os.getenv("HUGGINGFACE_API_KEY"),
)

def analyze_sentiment(text: str):
    response = client.text_classification(text, model="cardiffnlp/twitter-roberta-base-sentiment-latest")
    return response[0].label




