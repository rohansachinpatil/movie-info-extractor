import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import PydanticOutputParser

# 1. Load Environment Variables
load_dotenv()

# 2. Define the Schema
class Movie(BaseModel):
    title: str 
    release_year : Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str

# 3. Setup LangChain
model = ChatMistralAI(model='mistral-small-latest') # Using latest small model
parser = PydanticOutputParser(pydantic_object=Movie)

prompt = ChatPromptTemplate.from_messages([
    ('system', "Extract movie information from the paragraph.\n{format_instructions}"),
    ("human", "{paragraph}")
])

# 4. Initialize FastAPI
app = FastAPI(title="CineExtract API")

# 5. API Endpoint for Extraction
@app.post("/extract")
async def extract_movie(data: dict):
    paragraph = data.get("paragraph")
    if not paragraph:
        raise HTTPException(status_code=400, detail="No paragraph provided")
    
    try:
        # Create the prompt with format instructions
        formatted_prompt = prompt.invoke({
            "paragraph": paragraph,
            "format_instructions": parser.get_format_instructions()
        })
        
        # Get response from Mistral
        response = model.invoke(formatted_prompt)
        
        # Parse the response into the Movie object
        movie_data = parser.parse(response.content)
        
        return movie_data.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 6. Serve the UI
@app.get("/", response_class=HTMLResponse)
async def get_ui():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Movie Info Extractor — AI Parser</title>
  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet"/>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --cream: #faf8f4;
      --paper: #f3efe8;
      --ink: #1a1714;
      --ink-soft: #4a4540;
      --ink-faint: #9a9288;
      --amber: #d4820a;
      --amber-light: #f5e6c8;
      --amber-pale: #fdf6e8;
      --border: #e0d9ce;
      --shadow: rgba(26,23,20,0.08);
      --shadow-deep: rgba(26,23,20,0.16);
    }

    html { font-size: 16px; }

    body {
      background: var(--cream);
      font-family: 'DM Sans', sans-serif;
      color: var(--ink);
      min-height: 100vh;
      overflow-x: hidden;
    }

    /* Grain texture overlay */
    body::before {
      content: '';
      position: fixed; inset: 0;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
      pointer-events: none; z-index: 999;
    }

    /* Header */
    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 1.5rem 3rem;
      border-bottom: 1px solid var(--border);
      background: var(--cream);
      position: sticky; top: 0; z-index: 10;
    }

    .logo {
      display: flex; align-items: center; gap: 0.6rem;
    }

    .logo-icon {
      width: 34px; height: 34px;
      background: var(--ink);
      border-radius: 8px;
      display: flex; align-items: center; justify-content: center;
    }

    .logo-icon svg { width: 18px; height: 18px; fill: var(--cream); }

    .logo-text {
      font-family: 'DM Serif Display', serif;
      font-size: 1.3rem;
      color: var(--ink);
      letter-spacing: -0.02em;
    }

    .logo-text span { color: var(--amber); }

    .badge {
      font-size: 0.7rem;
      font-weight: 500;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--ink-faint);
      border: 1px solid var(--border);
      padding: 0.3rem 0.7rem;
      border-radius: 20px;
    }

    /* Main layout */
    main {
      max-width: 860px;
      margin: 0 auto;
      padding: 4rem 2rem 6rem;
    }

    .hero {
      text-align: center;
      margin-bottom: 3.5rem;
      animation: fadeUp 0.6s ease both;
    }

    .hero h1 {
      font-family: 'DM Serif Display', serif;
      font-size: clamp(2.2rem, 5vw, 3.2rem);
      line-height: 1.15;
      letter-spacing: -0.03em;
      color: var(--ink);
      margin-bottom: 0.8rem;
    }

    .hero h1 em {
      font-style: italic;
      color: var(--amber);
    }

    .hero p {
      font-size: 1rem;
      color: var(--ink-soft);
      font-weight: 300;
      max-width: 480px;
      margin: 0 auto;
      line-height: 1.6;
    }

    /* Input card */
    .input-card {
      background: white;
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 2rem;
      box-shadow: 0 4px 24px var(--shadow);
      margin-bottom: 2.5rem;
      animation: fadeUp 0.6s 0.1s ease both;
    }

    .input-label {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.8rem;
      font-weight: 600;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--ink-faint);
      margin-bottom: 0.8rem;
    }

    .input-label::before {
      content: '';
      width: 6px; height: 6px;
      background: var(--amber);
      border-radius: 50%;
    }

    textarea {
      width: 100%;
      min-height: 140px;
      background: var(--paper);
      border: 1.5px solid var(--border);
      border-radius: 12px;
      padding: 1rem 1.2rem;
      font-family: 'DM Sans', sans-serif;
      font-size: 0.95rem;
      color: var(--ink);
      line-height: 1.6;
      resize: vertical;
      transition: border-color 0.2s, box-shadow 0.2s;
      outline: none;
    }

    textarea::placeholder { color: var(--ink-faint); }

    textarea:focus {
      border-color: var(--amber);
      box-shadow: 0 0 0 3px var(--amber-light);
    }

    .input-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: 1.2rem;
      gap: 1rem;
    }

    .char-count {
      font-size: 0.8rem;
      color: var(--ink-faint);
    }

    .examples {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
      flex: 1;
    }

    .example-btn {
      font-size: 0.75rem;
      color: var(--amber);
      background: var(--amber-pale);
      border: 1px solid var(--amber-light);
      border-radius: 20px;
      padding: 0.25rem 0.7rem;
      cursor: pointer;
      font-family: 'DM Sans', sans-serif;
      font-weight: 500;
      transition: background 0.15s, transform 0.1s;
    }

    .example-btn:hover {
      background: var(--amber-light);
      transform: translateY(-1px);
    }

    .extract-btn {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      background: var(--ink);
      color: var(--cream);
      border: none;
      border-radius: 12px;
      padding: 0.85rem 1.8rem;
      font-family: 'DM Sans', sans-serif;
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
      letter-spacing: 0.01em;
      transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
      box-shadow: 0 2px 8px var(--shadow-deep);
      white-space: nowrap;
    }

    .extract-btn:hover {
      background: #2d2926;
      transform: translateY(-2px);
      box-shadow: 0 6px 20px var(--shadow-deep);
    }

    .extract-btn:active { transform: translateY(0); }

    .extract-btn:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      transform: none;
    }

    .extract-btn svg { width: 16px; height: 16px; }

    /* Loading */
    .loader {
      display: none;
      text-align: center;
      padding: 3rem;
      animation: fadeUp 0.3s ease both;
    }

    .loader.visible { display: block; }

    .film-strip {
      display: inline-flex;
      gap: 6px;
      margin-bottom: 1.2rem;
    }

    .film-strip span {
      width: 10px; height: 36px;
      background: var(--border);
      border-radius: 3px;
      animation: pulse 0.9s ease-in-out infinite;
    }

    .film-strip span:nth-child(2) { animation-delay: 0.15s; background: var(--amber-light); }
    .film-strip span:nth-child(3) { animation-delay: 0.3s; }
    .film-strip span:nth-child(4) { animation-delay: 0.45s; background: var(--amber-light); }
    .film-strip span:nth-child(5) { animation-delay: 0.6s; }

    @keyframes pulse {
      0%, 100% { opacity: 0.3; transform: scaleY(0.7); }
      50% { opacity: 1; transform: scaleY(1); }
    }

    .loader p {
      color: var(--ink-soft);
      font-size: 0.9rem;
    }

    /* Error */
    .error-box {
      display: none;
      background: #fff5f5;
      border: 1.5px solid #fca5a5;
      border-radius: 12px;
      padding: 1rem 1.2rem;
      color: #b91c1c;
      font-size: 0.88rem;
      margin-top: 1rem;
      animation: fadeUp 0.3s ease both;
    }

    .error-box.visible { display: block; }

    /* Result card */
    .result {
      display: none;
      animation: fadeUp 0.5s ease both;
    }

    .result.visible { display: block; }

    .result-card {
      background: white;
      border: 1px solid var(--border);
      border-radius: 20px;
      overflow: hidden;
      box-shadow: 0 8px 40px var(--shadow);
    }

    .card-header {
      background: var(--ink);
      padding: 2rem 2.4rem;
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 1.5rem;
    }

    .card-title-block { flex: 1; }

    .extracted-label {
      font-size: 0.7rem;
      font-weight: 600;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--amber);
      margin-bottom: 0.5rem;
    }

    .movie-title {
      font-family: 'DM Serif Display', serif;
      font-size: clamp(1.6rem, 4vw, 2.2rem);
      color: white;
      line-height: 1.15;
      letter-spacing: -0.02em;
      margin-bottom: 0.6rem;
    }

    .movie-meta {
      display: flex;
      align-items: center;
      gap: 1rem;
      flex-wrap: wrap;
    }

    .year-badge {
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--ink);
      background: var(--amber);
      padding: 0.2rem 0.65rem;
      border-radius: 6px;
    }

    .director-tag {
      font-size: 0.82rem;
      color: rgba(255,255,255,0.6);
    }

    .director-tag strong { color: rgba(255,255,255,0.9); }

    .rating-circle {
      width: 60px; height: 60px;
      border-radius: 50%;
      border: 2.5px solid var(--amber);
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      flex-shrink: 0;
    }

    .rating-num {
      font-family: 'DM Serif Display', serif;
      font-size: 1.1rem;
      color: white;
      line-height: 1;
    }

    .rating-label {
      font-size: 0.55rem;
      color: var(--amber);
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }

    .card-body {
      padding: 2rem 2.4rem;
    }

    .genres {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
      margin-bottom: 2rem;
    }

    .genre-tag {
      font-size: 0.78rem;
      font-weight: 500;
      color: var(--amber);
      background: var(--amber-pale);
      border: 1px solid var(--amber-light);
      padding: 0.3rem 0.8rem;
      border-radius: 20px;
      letter-spacing: 0.02em;
    }

    .section {
      margin-bottom: 1.8rem;
    }

    .section-label {
      font-size: 0.7rem;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--ink-faint);
      margin-bottom: 0.6rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .section-label::after {
      content: '';
      flex: 1;
      height: 1px;
      background: var(--border);
    }

    .summary-text {
      font-size: 0.95rem;
      color: var(--ink-soft);
      line-height: 1.7;
      font-weight: 300;
    }

    .cast-grid {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
    }

    .cast-pill {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      background: var(--paper);
      border: 1px solid var(--border);
      border-radius: 30px;
      padding: 0.35rem 0.9rem 0.35rem 0.5rem;
      font-size: 0.82rem;
      color: var(--ink-soft);
      font-weight: 400;
    }

    .cast-avatar {
      width: 22px; height: 22px;
      background: var(--ink);
      border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      font-size: 0.6rem;
      font-weight: 700;
      color: white;
      flex-shrink: 0;
      text-transform: uppercase;
    }

    .card-footer {
      border-top: 1px solid var(--border);
      padding: 1rem 2.4rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--paper);
    }

    .footer-note {
      font-size: 0.75rem;
      color: var(--ink-faint);
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }

    .footer-note::before {
      content: '✦';
      color: var(--amber);
      font-size: 0.7rem;
    }

    .reset-btn {
      font-size: 0.8rem;
      font-weight: 500;
      color: var(--ink-soft);
      background: none;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.4rem 0.9rem;
      cursor: pointer;
      font-family: 'DM Sans', sans-serif;
      transition: all 0.15s;
    }

    .reset-btn:hover {
      background: white;
      color: var(--ink);
      border-color: var(--ink-soft);
    }

    /* Missing field */
    .na { color: var(--ink-faint); font-style: italic; }

    /* Global Footer */
    footer.global-footer {
      text-align: center;
      padding: 3rem 1.5rem;
      border-top: 1px solid var(--border);
      margin-top: 2rem;
    }

    .footer-content {
      max-width: 860px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 1rem;
    }

    .footer-logo {
      font-family: 'DM Serif Display', serif;
      font-size: 1.1rem;
      color: var(--ink-soft);
    }

    .footer-logo span { color: var(--amber); }

    .footer-links {
      display: flex;
      gap: 2rem;
      margin-bottom: 0.5rem;
    }

    .footer-links a {
      font-size: 0.85rem;
      color: var(--ink-faint);
      text-decoration: none;
      transition: color 0.2s;
    }

    .footer-links a:hover { color: var(--ink); }

    .copyright {
      font-size: 0.8rem;
      color: var(--ink-faint);
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }

    .heart { color: #ef4444; }

    /* Animations */
    @keyframes fadeUp {
      from { opacity: 0; transform: translateY(18px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Responsive */
    @media (max-width: 600px) {
      header { padding: 1.2rem 1.5rem; }
      main { padding: 2.5rem 1.2rem 4rem; }
      .input-footer { flex-direction: column; align-items: stretch; }
      .extract-btn { justify-content: center; }
      .card-header { flex-direction: column; }
      .card-body, .card-header { padding: 1.5rem; }
      .card-footer { padding: 1rem 1.5rem; flex-direction: column; gap: 0.8rem; align-items: flex-start; }
    }
  </style>
</head>
<body>

<header>
  <div class="logo">
    <div class="logo-icon">
      <svg viewBox="0 0 24 24"><path d="M4 3h2v2H4V3zm14 0h2v2h-2V3zM4 19h2v2H4v-2zm14 0h2v2h-2v-2zM2 7h2v10H2V7zm18 0h2v10h-2V7zM6 6h12v12H6V6z"/></svg>
    </div>
    <span class="logo-text">MovieInfo<span>Extractor</span></span>
  </div>
  <span class="badge">AI Powered</span>
</header>

<main>
  <div class="hero">
    <h1>Paste a paragraph,<br/>get <em>movie data</em> instantly</h1>
    <p>Powered by Mistral AI + LangChain. Drop any text about a film and we'll extract structured info for you.</p>
  </div>

  <div class="input-card">
    <div class="input-label">Your paragraph</div>
    <textarea id="para" placeholder="e.g. Inception is a 2010 science fiction action film written and directed by Christopher Nolan, starring Leonardo DiCaprio as a professional thief who steals information by entering people's subconscious…"></textarea>
    <div class="input-footer">
      <div class="examples">
        <button class="example-btn" onclick="fillExample('inception')">Try Inception</button>
        <button class="example-btn" onclick="fillExample('parasite')">Try Parasite</button>
        <button class="example-btn" onclick="fillExample('godfather')">Try The Godfather</button>
      </div>
      <span class="char-count" id="charCount">0 chars</span>
      <button class="extract-btn" id="extractBtn" onclick="extractMovie()">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 3l14 9-14 9V3z"/></svg>
        Extract
      </button>
    </div>
    <div class="error-box" id="errorBox"></div>
  </div>

  <div class="loader" id="loader">
    <div class="film-strip">
      <span></span><span></span><span></span><span></span><span></span>
    </div>
    <p>Reading between the frames…</p>
  </div>

  <div class="result" id="result">
    <div class="result-card">
      <div class="card-header">
        <div class="card-title-block">
          <div class="extracted-label">✦ Extracted</div>
          <div class="movie-title" id="rTitle">—</div>
          <div class="movie-meta">
            <span class="year-badge" id="rYear">—</span>
            <span class="director-tag">Dir. <strong id="rDirector">—</strong></span>
          </div>
        </div>
        <div class="rating-circle" id="ratingCircle">
          <div class="rating-num" id="rRating">—</div>
          <div class="rating-label">Rating</div>
        </div>
      </div>

      <div class="card-body">
        <div class="genres" id="rGenres"></div>

        <div class="section">
          <div class="section-label">Synopsis</div>
          <p class="summary-text" id="rSummary">—</p>
        </div>

        <div class="section">
          <div class="section-label">Cast</div>
          <div class="cast-grid" id="rCast"></div>
        </div>
      </div>

      <div class="card-footer">
        <span class="footer-note">Developed by <strong>rohan patil</strong> | Mistral AI · LangChain</span>
        <button class="reset-btn" onclick="resetUI()">↩ New Extract</button>
      </div>
    </div>
  </div>
</main>

<footer class="global-footer">
  <div class="footer-content">
    <div class="footer-logo">MovieInfo<span>Extractor</span></div>
    <div class="footer-links">
      <a href="#">Github</a>
      <a href="#">Mistral AI</a>
      <a href="#">LangChain</a>
      <a href="#">Documentation</a>
    </div>
    <div class="copyright">
      &copy; 2026 MovieInfoExtractor. Made with <span class="heart">❤</span> by <strong>rohan patil</strong>
    </div>
  </div>
</footer>

<script>
  const EXAMPLES = {
    inception: "Inception is a 2010 science fiction action film written and directed by Christopher Nolan. Starring Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page, and Ken Watanabe, the film follows a group of professional thieves who enter people's subconscious to steal or plant information. It holds an IMDb rating of 8.8 and spans the genres of action, adventure, and sci-fi.",
    parasite: "Parasite is a 2019 South Korean black comedy thriller film directed by Bong Joon-ho. The film stars Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong, Choi Woo-shik, and Park So-dam. It tells the story of two families — one wealthy, one poor — and their uneasy co-existence. Parasite won the Palme d'Or at Cannes and holds an 8.5 rating on IMDb. Genres include thriller, drama, and dark comedy.",
    godfather: "The Godfather is a 1972 American crime film directed by Francis Ford Coppola. Starring Marlon Brando, Al Pacino, James Caan, and Diane Keaton, the film follows the powerful Corleone mafia family. Based on Mario Puzo's 1969 novel, it is widely considered one of the greatest films ever made. The Godfather has an IMDb rating of 9.2 and falls under the crime and drama genres."
  };

  const textarea = document.getElementById('para');
  textarea.addEventListener('input', () => {
    document.getElementById('charCount').textContent = textarea.value.length + ' chars';
  });

  function fillExample(key) {
    textarea.value = EXAMPLES[key];
    document.getElementById('charCount').textContent = textarea.value.length + ' chars';
    textarea.focus();
  }

  async function extractMovie() {
    const para = textarea.value.trim();
    if (!para) { showError('Please enter a paragraph about a movie.'); return; }

    setLoading(true);
    hideError();
    hideResult();

    try {
      const response = await fetch('/extract', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ paragraph: para })
      });

      if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Extraction failed');
      }

      const movie = await response.json();
      renderResult(movie);
    } catch (err) {
      showError('Could not extract movie data. (' + err.message + ')');
    } finally {
      setLoading(false);
    }
  }

  function renderResult(m) {
    document.getElementById('rTitle').textContent = m.title || 'Unknown Title';
    document.getElementById('rYear').textContent = m.release_year || '—';
    document.getElementById('rDirector').textContent = m.director || '—';
    document.getElementById('rSummary').textContent = m.summary || '—';

    const ratingEl = document.getElementById('rRating');
    const circleEl = document.getElementById('ratingCircle');
    if (m.rating) {
      ratingEl.textContent = m.rating;
      circleEl.style.borderColor = m.rating >= 8 ? '#22c55e' : m.rating >= 6 ? '#d4820a' : '#ef4444';
    } else {
      ratingEl.innerHTML = '<span class="na">N/A</span>';
    }

    const genresEl = document.getElementById('rGenres');
    genresEl.innerHTML = '';
    (m.genre || []).forEach(g => {
      const tag = document.createElement('span');
      tag.className = 'genre-tag';
      tag.textContent = g;
      genresEl.appendChild(tag);
    });

    const castEl = document.getElementById('rCast');
    castEl.innerHTML = '';
    (m.cast || []).forEach(name => {
      const pill = document.createElement('div');
      pill.className = 'cast-pill';
      const initials = name.split(' ').map(w => w[0]).slice(0, 2).join('');
      pill.innerHTML = `<div class="cast-avatar">${initials}</div>${name}`;
      castEl.appendChild(pill);
    });

    document.getElementById('result').classList.add('visible');
    document.getElementById('result').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function setLoading(on) {
    document.getElementById('loader').classList.toggle('visible', on);
    document.getElementById('extractBtn').disabled = on;
  }

  function hideResult() { document.getElementById('result').classList.remove('visible'); }
  function showError(msg) {
    const el = document.getElementById('errorBox');
    el.textContent = '⚠ ' + msg;
    el.classList.add('visible');
  }
  function hideError() { document.getElementById('errorBox').classList.remove('visible'); }

  function resetUI() {
    hideResult();
    textarea.value = '';
    document.getElementById('charCount').textContent = '0 chars';
    textarea.focus();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
</script>
</body>
</html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
