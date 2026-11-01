# AI Multi-Model Assistant

A Streamlit learning application with separate handlers for text generation (OpenAI),
summarization, sentiment classification and image captioning (Hugging Face). The user
selects a task; this is not autonomous agent routing.

## Setup
Use Python 3.12, create/activate `.venv`, then:
```bash
python -m pip install -r requirements.txt
# Copy .env.example to .env.local and set your own provider keys.
python -m streamlit run App.py
```
The four handlers are root modules imported by `App.py`. Clients are created lazily;
importing handlers does not require credentials. Model/provider availability and account
access may vary; a configured key does not guarantee a hosted model is available.
Live requests send your text/images to the chosen provider and may incur costs.
Images are verified as JPEG/PNG and their actual MIME type is sent. Text/image size limits
and safe provider errors are enforced. No accuracy or production-readiness claim is made.

## Offline tests
```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```
Fake-client tests cover lazy configuration, all four handlers, strongest sentiment label,
image validation/MIME type and redacted failures. They make no paid provider calls.
This small integration exercise is supporting learning work; RAG, Signal and TenderProof
are the more substantial AI engineering projects in this portfolio.
