import io
from types import SimpleNamespace as NS
import pytest
from PIL import Image
from providers import require_key
from sentiment import analyze_sentiment
from summarizer import summarize_text
from text_generator import generate_text
from image_captioner import caption_image

class Fake:
    def __init__(self): self.chat = NS(completions=self); self.request = None
    def create(self, **kwargs): self.request = kwargs; return NS(choices=[NS(message=NS(content="offline answer"))])
    def text_classification(self, *args, **kwargs): return [NS(label="negative", score=.1), NS(label="positive", score=.9)]
    def summarization(self, *args, **kwargs): return NS(summary_text="offline summary")

def test_text_handlers_and_no_credentials_in_output(monkeypatch, capsys):
    monkeypatch.delenv("HUGGINGFACE_API_KEY", raising=False)
    with pytest.raises(ValueError, match="HUGGINGFACE_API_KEY"): require_key("HUGGINGFACE_API_KEY")
    client = Fake()
    assert analyze_sentiment("good", client) == "positive"
    assert summarize_text("long text", client) == "offline summary"
    assert generate_text("hello", client) == "offline answer"
    assert capsys.readouterr().out == ""

@pytest.mark.parametrize("format,mime", [("PNG", "image/png"), ("JPEG", "image/jpeg")])
def test_caption_uses_actual_image_type(format, mime):
    stream = io.BytesIO(); Image.new("RGB", (2, 2)).save(stream, format=format); client = Fake()
    assert caption_image(stream.getvalue(), client) == "offline answer"
    url = client.request["messages"][0]["content"][1]["image_url"]["url"]
    assert url.startswith("data:" + mime + ";base64,")

def test_bad_inputs_and_redacted_provider_failure():
    with pytest.raises(ValueError): generate_text(" ", Fake())
    with pytest.raises(ValueError): caption_image(b"invalid", Fake())
    class Broken(Fake):
        def create(self, **kwargs): raise RuntimeError("sensitive-provider-detail")
    with pytest.raises(RuntimeError) as exc: generate_text("hello", Broken())
    assert "sensitive-provider-detail" not in str(exc.value)
