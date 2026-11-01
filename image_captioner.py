import base64
import io
import os
from PIL import Image
from providers import hf_client

def caption_image(image_bytes, client=None):
    if not image_bytes or len(image_bytes) > 10 * 1024 * 1024:
        raise ValueError("Image must be nonempty and at most 10 MiB")
    try:
        with Image.open(io.BytesIO(image_bytes)) as image:
            image.verify()
            mime = {"JPEG": "image/jpeg", "PNG": "image/png"}.get(image.format)
    except Exception:
        raise ValueError("Invalid image") from None
    if mime is None: raise ValueError("Use a JPEG or PNG image")
    client = client if client is not None else hf_client()
    try:
        response = client.chat.completions.create(model=os.getenv("HF_CAPTION_MODEL", "zai-org/GLM-4.5V"), messages=[{"role": "user", "content": [
            {"type": "text", "text": "Describe this image in one sentence."},
            {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{base64.b64encode(image_bytes).decode()}"}}]}])
        return response.choices[0].message.content or "No caption returned"
    except Exception:
        raise RuntimeError("Caption request failed; check model availability and provider access") from None
