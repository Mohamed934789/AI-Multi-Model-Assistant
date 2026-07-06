# 🤖 AI Multi-Model Assistant

> A modular, multi-model AI assistant built with Python and Streamlit — combining OpenAI's language models with Hugging Face's Inference API to deliver text generation, summarization, sentiment analysis, and image captioning through a single, clean interface.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI_API-412991?style=for-the-badge&logo=openai&logoColor=white)
![Hugging Face](https://img.shields.io/badge/🤗_Hugging_Face-FFD21E?style=for-the-badge)

---

## 📖 Overview

**AI Multi-Model Assistant** is a hands-on engineering project that demonstrates how to design and build a multi-model AI system from the ground up — not just call an API and print the result, but architect a system where each AI capability is isolated, testable, and independently swappable.

The project was built feature-by-feature, with a deliberate focus on **clean architecture**: separating the UI layer, the business logic (handlers), and configuration/secrets — so that adding a new AI capability never requires touching existing, working code.

## ✨ Features

| Feature | Description | Backend |
|---|---|---|
| 📝 **Text Generation** | Generate natural language responses from a prompt | OpenAI API (`gpt-4o-mini`) |
| 📄 **Text Summarization** | Condense long text into a concise summary | Hugging Face Inference API |
| 😊 **Sentiment Analysis** | Classify text as positive / negative / neutral | Hugging Face Inference API |
| 🖼️ **Image Captioning** | Generate a natural-language description of an uploaded image | Hugging Face Inference API (Vision-Language Model via Chat Completions) |
| 🔀 **Automatic Task Routing** | Dispatches user input to the correct handler dynamically — no hardcoded branching per feature | Custom dictionary-based router |

## 🏗️ Architecture

The project follows a simple but scalable pattern:

```
User Input (Streamlit UI)
        │
        ▼
   Task Router  ──────►  Handler (isolated module per AI task)
        │                       │
        │                       ▼
        │              External API (OpenAI / Hugging Face)
        │                       │
        ◄───────────────────────┘
   Normalized Output
        │
        ▼
   Displayed in UI
```

Each AI capability lives in its own **handler module**. The Streamlit UI never talks to OpenAI or Hugging Face directly — it only calls a clean function like `generate_text(prompt)` or `caption_image(image_bytes)`. This means:

- Swapping a model or provider only requires editing **one file**.
- Adding a new feature means writing **one new handler** and registering it — no existing code is modified (Open/Closed Principle).
- Every handler can be tested **in isolation**, independent of the UI.

## 📂 Project Structure

```
AI-Multi-Model-Assistant/
│
├── App.py                     # Streamlit UI + task router
├── requirements.txt            # Project dependencies
├── .env                        # API keys (NOT committed — see below)
├── .gitignore
│
└── handlers/
    ├── __init__.py
    ├── text_generator.py       # OpenAI — Chat Completions
    ├── summarizer.py           # Hugging Face — Summarization
    ├── sentiment.py            # Hugging Face — Text Classification
    └── image_captioner.py      # Hugging Face — Vision-Language Model captioning
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/ai-multi-model-assistant.git
cd ai-multi-model-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your API keys

Create a `.env` file in the project root with the following:

```env
OPENAI_API_KEY=your_openai_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

- Get an OpenAI API key from [platform.openai.com](https://platform.openai.com/api-keys)
- Get a Hugging Face token (Read access is enough) from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

> ⚠️ Never commit your `.env` file. It's already excluded via `.gitignore`.

### 4. Run the app

```bash
streamlit run App.py
```

The app will open automatically in your browser at `http://localhost:8501`.

## 🧠 Key Engineering Concepts Applied

This project was built as a learning exercise with a strong emphasis on **thinking like an engineer, not just following a tutorial**. Concepts practiced along the way:

- **Separation of Concerns** — UI, business logic, and secrets are fully decoupled
- **DRY Principle** — shared validation logic is centralized, not repeated per feature
- **Open/Closed Principle** — new features are added via a handler registry (dictionary dispatch), not by modifying existing conditional chains
- **Environment-based configuration** — secrets are never hardcoded
- **API integration patterns** — REST-style clients, request/response shapes, and provider-specific quirks (OpenAI Chat Completions vs. Hugging Face Inference Providers)
- **Binary data handling** — encoding image bytes as Base64 to transmit images through JSON-based chat APIs
- **Systematic debugging** — isolating and testing each handler independently before wiring it into the UI

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **UI Framework:** Streamlit
- **LLM Provider:** OpenAI API
- **Open-Source Models:** Hugging Face Inference API (`huggingface_hub`)
- **Config Management:** python-dotenv

## 🔮 Future Improvements

- [ ] Add robust error handling for API failures (network errors, rate limits, timeouts)
- [ ] Add a translation feature
- [ ] Cache repeated requests to reduce API usage
- [ ] Add unit tests for each handler
- [ ] Deploy publicly via Streamlit Community Cloud

## 📄 License

This project is open-source and available for learning purposes.

---

<p align="center">Built as a hands-on learning project in AI Engineering — Python, LLM APIs, and clean software architecture.</p>
