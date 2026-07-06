from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
import base64

from streamlit import image
load_dotenv()

client = InferenceClient(token=os.getenv("HUGGINGFACE_API_KEY"))

def caption_image (image_bytes: bytes): 
    base64_string = base64.b64encode(image_bytes).decode("utf-8")
    response = client.chat.completions.create(
    model="zai-org/GLM-4.5V",  
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image in one sentence."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_string}"}}
            ]
        }
    ]
)

    return response.choices[0].message.content






