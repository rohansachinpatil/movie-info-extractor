# MovieInfoExtractor 🎬

**MovieInfoExtractor** is a modern, AI-powered web application and CLI tool designed to extract structured data from unstructured text about films. Using the power of **Mistral AI**, **LangChain**, and **FastAPI**, it can parse complex paragraphs and turn them into clean, usable movie metadata.

![Project Preview](https://img.shields.io/badge/AI-Powered-amber?style=for-the-badge)
![Tech Stack](https://img.shields.io/badge/FastAPI-LangChain-ink?style=for-the-badge)

## 🌟 Features

-   **Intelligent Extraction**: Automatically identifies Movie Title, Release Year, Director, Cast, Genres, Rating, and Summary from any paragraph.
-   **Structured Output**: Uses Pydantic to ensure data consistency and reliability.
-   **Modern Web UI**: A premium, responsive user interface with a "CineExtract" aesthetic.
-   **Dual Modes**: Use the **Web App** for a visual experience or the **CLI Tool** for quick terminal-based extraction.
-   **Mistral AI Integration**: Leverages high-performance LLMs for accurate natural language understanding.

## 🛠️ Tech Stack

-   **Backend**: Python, [FastAPI](https://fastapi.tiangolo.com/)
-   **AI Orchestration**: [LangChain](https://www.langchain.com/)
-   **LLM**: [Mistral AI](https://mistral.ai/)
-   **Data Validation**: [Pydantic](https://docs.pydantic.dev/)
-   **Frontend**: HTML5, Vanilla CSS (Glassmorphism & Grain Texture), JavaScript (ES6+)

## 🚀 Getting Started

### Prerequisites

-   Python 3.8+
-   A Mistral AI API Key

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/rohansachinpatil/movie_recommendation_system.git
    cd movie_recommendation_system
    ```

2.  **Set up a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**:
    Create a `.env` file in the root directory and add your API key:
    ```env
    MISTRAL_API_KEY=your_api_key_here
    ```

## 📖 Usage

### 1. Web Application (Recommended)
Launch the interactive web interface:
```bash
python MovieInfoExtractor/app.py
```
Open your browser and navigate to `http://127.0.0.1:8000`.

### 2. CLI Tool
For quick extraction directly in your terminal:
```bash
python MovieInfoExtractor/core.py
```

## 🏗️ Project Structure

```text
movie_recommendation_system/
├── MovieInfoExtractor/
│   ├── app.py           # Unified Web App (FastAPI + UI)
│   └── core.py          # CLI-based extraction logic
├── .env                 # API Keys (not in git)
├── requirements.txt     # Project dependencies
└── README.md            # You are here!
```

## 🤝 Credits

Developed with ❤️ by **rohan patil**.

-   Powered by **Mistral AI**
-   Built with **LangChain**
-   UI inspired by modern cinematic aesthetics.

---
© 2026 MovieInfoExtractor | AI Data Solutions
