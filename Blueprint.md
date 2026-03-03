# BYTEBRIEF

## AI-Powered News Aggregation & Digest Platform

### Project Blueprint & Technical Specification

| Type            | Stack              | Core Tech          | Features                           |
| --------------- | ------------------ | ------------------ | ---------------------------------- |
| Web Application | Full-Stack + AI/ML | BART / T5 / TF-IDF | Scrape · Digest · Search · Compare |

> **Stack Philosophy**: ByteBrief runs entirely without Docker, Redis, or Elasticsearch.
> MongoDB is the single database for all data. Whoosh provides pure-Python full-text search
> with zero external services. Celery uses a MongoDB broker via `mongo-celery`. Everything
> runs with simple terminal commands.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Web Scraping & Data Ingestion](#3-web-scraping--data-ingestion)
4. [The Digest Feature — AI Summarization](#4-the-digest-feature--ai-summarization)
5. [Search & Compare Feature](#5-search--compare-feature)
6. [Personalization Ranking Algorithm](#6-personalization-ranking-algorithm)
7. [Frontend Web Application](#7-frontend-web-application)
8. [Backend API Design](#8-backend-api-design)
9. [Project Folder Structure](#9-project-folder-structure)
10. [Running the App — Local Setup](#10-running-the-app--local-setup)
11. [Environment Variables Reference](#11-environment-variables-reference)
12. [LLM-Ready Implementation Prompts](#12-llm-ready-implementation-prompts)
13. [Development Roadmap](#13-development-roadmap)

---

## 1. Project Overview

ByteBrief is a full-stack AI-powered news aggregation platform that automatically scrapes news articles from multiple sources across the web, presents them in a clean reader-friendly interface, and uses state-of-the-art NLP models to generate concise digestible summaries. An intelligent search engine detects when multiple outlets cover the same story and surfaces the differences in coverage side by side.

### 1.1 What Makes ByteBrief Different from NewsFlow

| Concern                 | NewsFlow               | ByteBrief                                       |
| ----------------------- | ---------------------- | ----------------------------------------------- |
| Database                | PostgreSQL + pgvector  | **MongoDB (single service)**                    |
| Search Engine           | Elasticsearch (Docker) | **Whoosh (pure Python, no install)**            |
| Message Broker          | Redis (Docker)         | **MongoDB via mongo-celery (no extra service)** |
| Vector Storage          | pgvector extension     | **MongoDB Atlas Vector Search / pymongo**       |
| Deployment              | Docker Compose         | **Plain terminal commands**                     |
| Infrastructure overhead | High (5+ services)     | **Low (MongoDB only)**                          |

### 1.2 Core Product Goals

- Aggregate news from multiple online sources automatically via web scraping
- Display both the original full article and an AI-generated digest side by side
- Enable users to search for topics and compare how different outlets cover the same story
- Apply advanced NLP: TF-IDF, semantic similarity, BART/T5 summarization, and sentiment analysis
- Personalize news rankings per user and evaluate model quality with ROUGE-N and BLEU metrics

### 1.3 The Digest Feature

> **What is the Digest?**
> When a user does not have time to read a full article, they click "Digest" to get an AI-generated abstractive summary produced by a fine-tuned BART or T5 model. The platform shows both the original scraped article and the digest simultaneously, giving the user the choice of depth — full read or 30-second brief.

### 1.4 The Search & Compare Feature

> **What is Search & Compare?**
> When a user searches for a topic, ByteBrief retrieves all matching articles using Whoosh (a pure-Python full-text search library — no server required). It then detects if the same news story appears across multiple outlets using TF-IDF and semantic similarity. When the same story is found in multiple newspapers, a diff view highlights what each outlet reported differently — unique facts, omitted angles, different sentiment tones.

---

## 2. System Architecture

ByteBrief uses a simplified three-service architecture. MongoDB handles all persistence (documents, vectors, user data, Celery task queue). Whoosh handles full-text search as a local index on disk. The NLP engine runs as in-process Python workers.

### 2.1 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│           LAYER 5 — FRONTEND (React / Next.js)                  │
│   News Feed · Article View · Digest Panel · Search & Compare    │
├─────────────────────────────────────────────────────────────────┤
│           LAYER 4 — BACKEND API (FastAPI)                       │
│   News · Digest · Search · Compare · Auth · Personalization     │
├─────────────────────────────────────────────────────────────────┤
│           LAYER 3 — NLP PROCESSING ENGINE                       │
│   BART/T5 Summarizer · TF-IDF · Semantic Sim · Sentiment · Eval │
├─────────────────────────────────────────────────────────────────┤
│           LAYER 2 — SEARCH INDEX (Whoosh)                       │
│   Pure-Python · File-based index on disk · No server needed     │
├─────────────────────────────────────────────────────────────────┤
│           LAYER 1 — DATA & TASK LAYER (MongoDB only)            │
│   Articles · Users · Digests · Embeddings · Celery Broker/Beat  │
└─────────────────────────────────────────────────────────────────┘

         [ Scrapy + Playwright ]  →  MongoDB  ←→  Whoosh Index
                   ↑
         [ Celery Workers (MongoDB broker) ]
```

### 2.2 Why Whoosh for Search?

Whoosh is a pure-Python, file-based full-text search library. It requires **zero installation, zero server, zero Docker** — just `pip install whoosh`. It creates an index directory on disk and supports BM25 ranking, phrase queries, wildcard search, and field boosting. For a news platform at moderate scale (tens of thousands of articles), Whoosh performs excellently.

```
Elasticsearch  →  requires JVM, Docker, 512 MB+ RAM minimum
Whoosh         →  pip install whoosh, runs in-process, index stored in /data/whoosh_index/
```

### 2.3 Why MongoDB as the Celery Broker?

Normally Celery requires Redis or RabbitMQ as a message broker. With the `celery-with-mongodb` backend (`mongo-celery`), MongoDB itself serves as both the **task broker** and the **result backend** — eliminating the need for any additional service. Tasks are stored as MongoDB documents and polled by workers.

### 2.4 Full Technology Stack

| Component        | Technology                       | Purpose                                     |
| ---------------- | -------------------------------- | ------------------------------------------- |
| Frontend         | React.js + Next.js 14            | SSR, routing, user interface                |
| Styling          | Tailwind CSS                     | Utility-first responsive design             |
| Backend          | FastAPI (Python 3.11)            | High-performance async REST API             |
| Task Queue       | Celery 5.x + mongo-celery        | Async scraping & NLP (MongoDB broker)       |
| Scraper          | Scrapy + Playwright              | Static & JS-rendered page scraping          |
| RSS/Feeds        | feedparser + NewsAPI             | Structured news feed ingestion              |
| Database         | MongoDB (via Motor async driver) | All data: articles, users, digests, vectors |
| Full-Text Search | Whoosh                           | Pure-Python, file-based, no server          |
| Summarizer       | BART / T5 (HuggingFace)          | Abstractive news digest generation          |
| Embeddings       | sentence-transformers            | Semantic similarity + MongoDB vector store  |
| TF-IDF           | scikit-learn                     | Keyword relevance & duplicate detection     |
| Sentiment        | VADER + RoBERTa                  | Sentiment scoring on articles               |
| Eval             | rouge-score + sacrebleu          | ROUGE-N and BLEU metrics                    |
| Auth             | JWT + python-jose                | Secure user authentication                  |

---

## 3. Web Scraping & Data Ingestion

The scraping layer collects articles from diverse news sources, handles both static HTML and JavaScript-rendered pages, and feeds cleaned content into MongoDB and the Whoosh search index.

### 3.1 Multi-Source Strategy

- **Scrapy spiders** for static news sites (BBC, Reuters, AP News, The Guardian)
- **Playwright headless browser** for JS-heavy sites (Bloomberg, Wired, TechCrunch)
- **RSS/Atom feed parser** (`feedparser`) for sites with structured feeds
- **NewsAPI integration** for rapid ingestion (requires a free API key at newsapi.org)
- **Celery Beat scheduler** (MongoDB broker): configurable scrape intervals per source

### 3.2 MongoDB Collection: `articles`

Each scraped article is stored as a MongoDB document in the `bytebrief.articles` collection.

```json
{
  "_id": "ObjectId",
  "article_id": "sha256-hash-of-url",
  "title": "AI Breakthrough Announced by Leading Lab",
  "url": "https://bbc.com/news/technology/...",
  "source_name": "BBC News",
  "author": ["Jane Doe"],
  "publish_date": "2025-03-01T10:30:00Z",
  "scraped_at": "2025-03-01T11:00:00Z",
  "content_raw": "<html>...</html>",
  "content_clean": "Cleaned plain text of the article body...",
  "category": "Technology",
  "images": [{ "url": "https://...", "caption": "Image caption" }],
  "digest": "AI researchers announced a major breakthrough...",
  "sentiment_score": -0.23,
  "sentiment_label": "NEGATIVE",
  "embedding": [0.023, -0.412, 0.881, "...768 floats total"],
  "tfidf_keywords": ["AI", "breakthrough", "lab", "model"],
  "whoosh_indexed": true,
  "digest_generated": true
}
```

### 3.3 MongoDB Indexes to Create

```python
# Run once during setup: python -m app.db.setup_indexes

await db.articles.create_index("article_id", unique=True)
await db.articles.create_index("publish_date")
await db.articles.create_index("source_name")
await db.articles.create_index("category")
await db.articles.create_index("whoosh_indexed")
await db.articles.create_index("digest_generated")
# Text index for lightweight MongoDB full-text (used as fallback)
await db.articles.create_index([("title", "text"), ("content_clean", "text")])
```

### 3.4 Text Preprocessing Pipeline

1. Extract raw HTML using Scrapy / Playwright
2. Parse with BeautifulSoup — strip ads, navbars, scripts, footers
3. Strip boilerplate using **Trafilatura** (best-in-class article extractor)
4. Unicode normalization, whitespace cleanup
5. Sentence tokenization using spaCy (`en_core_web_sm`)
6. Store `content_raw` and `content_clean` in MongoDB
7. Trigger Celery task: `post_process_article(article_id)` → runs NLP pipeline
8. Index into Whoosh after NLP completes

### 3.5 Whoosh Index Setup

Whoosh creates and manages a file-based index at `./data/whoosh_index/`. No server needed.

```python
# app/search/whoosh_setup.py
from whoosh import index
from whoosh.fields import Schema, TEXT, ID, DATETIME, STORED

SCHEMA = Schema(
    article_id  = ID(stored=True, unique=True),
    title       = TEXT(stored=True, field_boost=2.0),   # boost title matches
    content     = TEXT(stored=False),
    source_name = TEXT(stored=True),
    category    = ID(stored=True),
    publish_date= DATETIME(stored=True),
    url         = STORED,
)

def create_or_open_index(index_dir="./data/whoosh_index"):
    import os
    os.makedirs(index_dir, exist_ok=True)
    if index.exists_in(index_dir):
        return index.open_dir(index_dir)
    return index.create_in(index_dir, SCHEMA)
```

---

## 4. The Digest Feature — AI Summarization

The Digest feature uses a fine-tuned Transformer Encoder-Decoder model (BART or T5) to produce an abstractive summary of any article. The digest is cached in MongoDB so it is only generated once per article.

### 4.1 Model: BART / T5 via HuggingFace

> **Why BART or T5?**
> `BART-large-CNN` is fine-tuned on CNN/DailyMail news articles, making it directly suited to news summarization without any additional fine-tuning. T5 is more flexible and works well when you want to prompt it differently (e.g., `"summarize: {article}"`).

#### 4.1.1 Model Comparison

| Attribute      | BART-large-CNN                               | T5-base / T5-large                  |
| -------------- | -------------------------------------------- | ----------------------------------- |
| Architecture   | Denoising autoencoder + fine-tune            | Text-to-text unified framework      |
| Pre-training   | Masked token prediction + sentence shuffling | Span masking on C4 corpus           |
| Best For       | News summarization (CNN/DM fine-tune)        | Flexible general-purpose tasks      |
| Speed          | Moderate (~1.6 GB model)                     | T5-base is faster and lighter       |
| Output Quality | Excellent fluency, news-specific             | High quality, slightly more generic |
| HuggingFace ID | `facebook/bart-large-cnn`                    | `t5-base` or `google/flan-t5-large` |
| Input prefix   | None required                                | `"summarize: "` prefix needed       |

### 4.2 Summarizer Module

```python
# app/nlp/summarizer.py
from transformers import pipeline
from loguru import logger
import time

class NewsSummarizer:
    _instance = None

    def __new__(cls, model_name="facebook/bart-large-cnn"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            logger.info(f"Loading summarizer model: {model_name}")
            cls._instance.pipe = pipeline(
                "summarization",
                model=model_name,
                device=-1,   # CPU; set to 0 for GPU
            )
        return cls._instance

    def summarize(self, text: str, max_length=300, min_length=80) -> str:
        # Chunk long articles (BART max input = 1024 tokens)
        chunks = self._chunk_text(text, max_tokens=900, overlap=100)
        if len(chunks) == 1:
            return self._summarize_chunk(chunks[0], max_length, min_length)
        # Multi-chunk: summarize each, then re-summarize combined
        chunk_summaries = [self._summarize_chunk(c, 150, 40) for c in chunks]
        combined = " ".join(chunk_summaries)
        return self._summarize_chunk(combined, max_length, min_length)

    def _summarize_chunk(self, text, max_length, min_length) -> str:
        t0 = time.time()
        result = self.pipe(
            text,
            max_length=max_length,
            min_length=min_length,
            num_beams=4,
            no_repeat_ngram_size=3,
            early_stopping=True,
        )
        logger.debug(f"Summarized in {time.time()-t0:.2f}s")
        return result[0]["summary_text"]

    def _chunk_text(self, text: str, max_tokens: int, overlap: int) -> list[str]:
        words = text.split()
        chunks, i = [], 0
        while i < len(words):
            chunks.append(" ".join(words[i:i+max_tokens]))
            i += max_tokens - overlap
        return chunks
```

### 4.3 Summarization Pipeline (End to End)

1. Celery task `generate_digest(article_id)` fires after article is scraped
2. Fetch `content_clean` from MongoDB
3. Check if `digest_generated: true` — return cached digest if so
4. Pass to `NewsSummarizer().summarize(text)`
5. Update MongoDB: `{"digest": summary, "digest_generated": true}`
6. API serves digest from MongoDB on next request — zero re-computation

### 4.4 Evaluation Metrics — ROUGE-N & BLEU

#### ROUGE-N

- **ROUGE-1**: Unigram overlap (recall) between generated and reference
- **ROUGE-2**: Bigram overlap — phrase-level quality
- **ROUGE-L**: Longest common subsequence — structural fluency
- Library: `pip install rouge-score`

#### BLEU

- Precision-based n-gram metric with brevity penalty
- **BLEU-4** is the standard for summarization
- Library: `pip install sacrebleu`

#### Evaluation Script

```bash
# Run after setup:
python -m app.evaluation.eval --model bart --num_samples 200
# Output: prints scores + saves eval_report.json
```

---

## 5. Search & Compare Feature

### 5.1 Search Architecture — Whoosh + TF-IDF + Semantic

ByteBrief uses a **three-stage pipeline** entirely in Python with no external search server:

```
User Query
    │
    ▼
[ Stage 1: Whoosh BM25 Full-Text Search ]
  → Fast file-based search across all articles
  → Returns top-50 candidate article IDs
    │
    ▼
[ Stage 2: TF-IDF Cosine Reranking ]
  → scikit-learn TfidfVectorizer on candidate content
  → Cosine similarity between query vector and candidates
  → Rerank candidates
    │
    ▼
[ Stage 3: Semantic Cosine Reranking ]
  → sentence-transformers embeds query + candidates
  → Cosine similarity on 768-dim vectors
  → Blend: 0.4 × TF-IDF score + 0.6 × Semantic score
    │
    ▼
[ Duplicate Grouping ]
  → Articles with pairwise similarity > 0.78 → same story
  → Tag with same_story_group_id
    │
    ▼
Return top-K results to frontend
```

### 5.2 Whoosh Search Implementation

```python
# app/search/whoosh_search.py
from whoosh.qparser import MultifieldParser, FuzzyTermPlugin
from whoosh.searching import Results
from app.search.whoosh_setup import create_or_open_index

def search_articles(query_str: str, top_n: int = 50) -> list[dict]:
    ix = create_or_open_index()
    with ix.searcher() as searcher:
        parser = MultifieldParser(
            ["title", "content", "source_name"],
            schema=ix.schema
        )
        parser.add_plugin(FuzzyTermPlugin())
        query = parser.parse(query_str)
        results: Results = searcher.search(query, limit=top_n)
        return [
            {
                "article_id": r["article_id"],
                "title": r["title"],
                "source_name": r["source_name"],
                "score": r.score,
            }
            for r in results
        ]

def index_article(article: dict):
    """Call this after every new article is saved."""
    ix = create_or_open_index()
    writer = ix.writer()
    writer.update_document(
        article_id   = article["article_id"],
        title        = article["title"],
        content      = article["content_clean"],
        source_name  = article["source_name"],
        category     = article["category"],
        url          = article["url"],
    )
    writer.commit()
```

### 5.3 TF-IDF for Relevance Scoring

```python
# app/nlp/similarity.py  (TF-IDF part)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def tfidf_rerank(query: str, candidates: list[dict]) -> list[dict]:
    """Rerank candidate articles by TF-IDF cosine similarity to query."""
    docs = [query] + [c["content_clean"] for c in candidates]
    vectorizer = TfidfVectorizer(max_features=10000, stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(docs)
    query_vec = tfidf_matrix[0]
    doc_vecs  = tfidf_matrix[1:]
    scores = cosine_similarity(query_vec, doc_vecs).flatten()
    for i, candidate in enumerate(candidates):
        candidate["tfidf_score"] = float(scores[i])
    return sorted(candidates, key=lambda x: x["tfidf_score"], reverse=True)
```

### 5.4 Semantic Similarity & Duplicate Detection

```python
# app/nlp/similarity.py  (semantic + dedup part)
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-mpnet-base-v2")
    return _model

def semantic_rerank(query: str, candidates: list[dict]) -> list[dict]:
    model = get_model()
    texts = [query] + [c["title"] + " " + c["content_clean"][:500] for c in candidates]
    embeddings = model.encode(texts, convert_to_numpy=True)
    query_emb = embeddings[0:1]
    doc_embs   = embeddings[1:]
    scores = cosine_similarity(query_emb, doc_embs).flatten()
    for i, candidate in enumerate(candidates):
        candidate["semantic_score"] = float(scores[i])
        # Blend: 40% TF-IDF + 60% Semantic
        candidate["final_score"] = (
            0.4 * candidate.get("tfidf_score", 0) +
            0.6 * candidate["semantic_score"]
        )
    return sorted(candidates, key=lambda x: x["final_score"], reverse=True)

def detect_duplicates(candidates: list[dict], threshold: float = 0.78) -> list[dict]:
    """Group articles that cover the same story."""
    model = get_model()
    texts = [c["title"] + " " + c["content_clean"][:500] for c in candidates]
    embeddings = model.encode(texts, convert_to_numpy=True)
    sim_matrix = cosine_similarity(embeddings)

    group_id = 0
    assigned = {}
    for i in range(len(candidates)):
        if i in assigned:
            continue
        assigned[i] = group_id
        for j in range(i + 1, len(candidates)):
            if j not in assigned and sim_matrix[i][j] >= threshold:
                assigned[j] = group_id
        group_id += 1

    for i, candidate in enumerate(candidates):
        candidate["same_story_group_id"] = assigned[i]
    return candidates
```

### 5.5 MongoDB Vector Storage

Article embeddings are stored directly in MongoDB as float arrays, enabling lightweight vector lookups for the duplicate detection step.

```python
# Store embedding when article is processed
await db.articles.update_one(
    {"article_id": article_id},
    {"$set": {"embedding": embedding.tolist()}}
)

# Retrieve embeddings for a batch of candidates
pipeline = [
    {"$match": {"article_id": {"$in": candidate_ids}}},
    {"$project": {"article_id": 1, "embedding": 1, "title": 1}}
]
docs = await db.articles.aggregate(pipeline).to_list(length=100)
```

### 5.6 Compare View — Difference Highlighting

Once same-story articles are grouped, the Compare View shows side-by-side differences:

```python
# app/nlp/diff.py
import difflib

def compute_article_diff(text_a: str, text_b: str) -> dict:
    """Return sentence-level diff between two articles."""
    sents_a = text_a.split(". ")
    sents_b = text_b.split(". ")
    matcher = difflib.SequenceMatcher(None, sents_a, sents_b)

    unique_to_a, unique_to_b, common = [], [], []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            common.extend(sents_a[i1:i2])
        elif tag in ("delete", "replace"):
            unique_to_a.extend(sents_a[i1:i2])
            if tag == "replace":
                unique_to_b.extend(sents_b[j1:j2])
        elif tag == "insert":
            unique_to_b.extend(sents_b[j1:j2])

    return {
        "unique_to_a": unique_to_a,
        "unique_to_b": unique_to_b,
        "common": common,
    }
```

**What the Compare View shows:**

- Side-by-side layout: Outlet A (left) vs Outlet B (right)
- Sentences only in A → highlighted yellow
- Sentences only in B → highlighted blue
- Sentiment badge per outlet (POSITIVE / NEGATIVE / NEUTRAL)
- Word count, publish time, and author comparison
- Key Differences summary panel at the bottom

### 5.7 Sentiment Analysis

```python
# app/nlp/sentiment.py
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline as hf_pipeline

vader = SentimentIntensityAnalyzer()

def score_title(title: str) -> dict:
    """Fast VADER scoring for headlines."""
    scores = vader.polarity_scores(title)
    compound = scores["compound"]
    label = "POSITIVE" if compound >= 0.05 else "NEGATIVE" if compound <= -0.05 else "NEUTRAL"
    return {"sentiment_score": compound, "sentiment_label": label}

_roberta = None

def score_body(text: str) -> dict:
    """Deep RoBERTa scoring for full article body (async Celery task)."""
    global _roberta
    if _roberta is None:
        _roberta = hf_pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment",
            truncation=True,
            max_length=512
        )
    result = _roberta(text[:2000])[0]
    label_map = {"LABEL_0": "NEGATIVE", "LABEL_1": "NEUTRAL", "LABEL_2": "POSITIVE"}
    return {
        "sentiment_score": result["score"],
        "sentiment_label": label_map.get(result["label"], "NEUTRAL")
    }
```

---

## 6. Personalization Ranking Algorithm

ByteBrief learns from each user's reading behavior and surfaces the most relevant articles at the top of their feed.

### 6.1 MongoDB Collection: `user_events`

```json
{
  "_id": "ObjectId",
  "user_id": "user_abc123",
  "article_id": "sha256-hash",
  "event_type": "read",
  "category": "Technology",
  "source_name": "BBC News",
  "time_spent_seconds": 142,
  "used_digest": false,
  "timestamp": "2025-03-01T12:00:00Z"
}
```

### 6.2 MongoDB Collection: `user_profiles`

```json
{
  "_id": "ObjectId",
  "user_id": "user_abc123",
  "category_weights": {
    "Technology": 0.8,
    "Politics": 0.4,
    "Sports": 0.1
  },
  "source_weights": {
    "BBC News": 0.7,
    "Reuters": 0.6
  },
  "digest_preference": 0.6,
  "updated_at": "2025-03-01T12:05:00Z"
}
```

### 6.3 Ranking Score Function

```
Score(article, user) =
    w1 × CategoryMatch(article.category, user.category_weights)
  + w2 × SourceMatch(article.source_name, user.source_weights)
  + w3 × RecencyScore(article.publish_date)
  + w4 × TrendingBoost(article.view_count_24h)
  + w5 × SentimentAlignment(article.sentiment_label, user.sentiment_pref)
```

Weights `w1–w5` start equal (0.2 each) and are updated per user using a lightweight **gradient update** every time a `user_event` is recorded. No separate ML framework needed — pure NumPy math.

### 6.4 Implementation

```python
# app/personalization/ranker.py
from datetime import datetime, timezone
import math

def score_article(article: dict, profile: dict) -> float:
    cat_score    = profile["category_weights"].get(article["category"], 0.1)
    source_score = profile["source_weights"].get(article["source_name"], 0.1)

    # Recency: exponential decay — articles older than 48h score near 0
    age_hours = (datetime.now(timezone.utc) - article["publish_date"]).seconds / 3600
    recency   = math.exp(-age_hours / 24)

    trending  = min(article.get("view_count_24h", 0) / 1000, 1.0)

    return (
        0.25 * cat_score +
        0.20 * source_score +
        0.30 * recency +
        0.25 * trending
    )
```

---

## 7. Frontend Web Application

The frontend is built with React.js and Next.js 14, using the App Router for server components and Tailwind CSS for styling.

### 7.1 Key Screens & Components

| Screen             | Key Components                                                                                                                                    |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Home / Feed**    | Infinite scroll `ArticleCard` grid. Category tabs. Trending sidebar. "For You" personalized toggle. Sentiment badge on each card.                 |
| **Article View**   | Full article with clean typography. Collapsible **Digest Panel** on the right. Sentiment indicator. Related articles below. Save / Share actions. |
| **Digest Mode**    | Summary-only view. Estimated read time (30–60 sec). "Read full article" expand button.                                                            |
| **Search Results** | Autocomplete search bar. Same-story grouped cards with a "Compare" badge. Grid/list toggle.                                                       |
| **Compare View**   | Split-screen diff. Yellow/blue sentence highlights. Sentiment badges per outlet. Key Differences panel. Metadata comparison row.                  |

### 7.2 State Management

Use **Zustand** (lightweight, no boilerplate) for global state:

```javascript
// store/useNewsStore.js
import { create } from "zustand";

const useNewsStore = create((set) => ({
  articles: [],
  searchResults: [],
  compareArticles: [null, null],
  setArticles: (articles) => set({ articles }),
  setSearchResults: (results) => set({ searchResults: results }),
  setCompareArticles: (pair) => set({ compareArticles: pair }),
}));
```

---

## 8. Backend API Design

FastAPI backend, fully async via `motor` (async MongoDB driver). All routes versioned under `/api/v1/`.

### 8.1 MongoDB Connection (Motor)

```python
# app/db/mongo.py
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.MONGODB_DB_NAME]   # bytebrief

# Collections
articles_col   = db["articles"]
users_col      = db["users"]
events_col     = db["user_events"]
profiles_col   = db["user_profiles"]
```

### 8.2 Core API Endpoints

| Method | Endpoint                              | Purpose                                         |
| ------ | ------------------------------------- | ----------------------------------------------- |
| `GET`  | `/api/v1/news/`                       | Paginated article feed (personalized if authed) |
| `GET`  | `/api/v1/news/{id}/`                  | Single article by ID                            |
| `GET`  | `/api/v1/news/{id}/digest/`           | Get or generate AI digest                       |
| `GET`  | `/api/v1/news/trending/`              | Top articles by view count (last 24h)           |
| `GET`  | `/api/v1/search/?q={query}`           | Whoosh → TF-IDF → Semantic search               |
| `GET`  | `/api/v1/search/compare/?ids=id1,id2` | Sentence diff + sentiment for two articles      |
| `POST` | `/api/v1/users/register/`             | User registration (stored in MongoDB)           |
| `POST` | `/api/v1/users/login/`                | JWT token auth                                  |
| `GET`  | `/api/v1/users/feed/`                 | Personalized feed for authenticated user        |
| `POST` | `/api/v1/users/preferences/`          | Save category/source preferences                |
| `POST` | `/api/v1/events/`                     | Record user interaction event                   |
| `GET`  | `/api/v1/categories/`                 | List all categories from MongoDB                |
| `GET`  | `/api/v1/metrics/eval/`               | ROUGE/BLEU evaluation report (admin)            |

### 8.3 Example Route: Digest

```python
# app/api/news.py
from fastapi import APIRouter, HTTPException
from app.db.mongo import articles_col
from app.nlp.summarizer import NewsSummarizer
from bson import ObjectId

router = APIRouter(prefix="/api/v1/news", tags=["news"])

@router.get("/{article_id}/digest/")
async def get_digest(article_id: str):
    article = await articles_col.find_one({"article_id": article_id})
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # Return cached digest if it exists
    if article.get("digest_generated") and article.get("digest"):
        return {"article_id": article_id, "digest": article["digest"], "cached": True}

    # Generate new digest
    summarizer = NewsSummarizer()
    digest = summarizer.summarize(article["content_clean"])

    # Cache in MongoDB
    await articles_col.update_one(
        {"article_id": article_id},
        {"$set": {"digest": digest, "digest_generated": True}}
    )
    return {"article_id": article_id, "digest": digest, "cached": False}
```

### 8.4 Example Route: Search & Compare

```python
# app/api/search.py
from fastapi import APIRouter
from app.search.whoosh_search import search_articles
from app.nlp.similarity import tfidf_rerank, semantic_rerank, detect_duplicates
from app.nlp.diff import compute_article_diff
from app.nlp.sentiment import score_title
from app.db.mongo import articles_col

router = APIRouter(prefix="/api/v1/search", tags=["search"])

@router.get("/")
async def search(q: str, top_k: int = 20):
    # Stage 1: Whoosh
    candidates_meta = search_articles(q, top_n=50)
    ids = [c["article_id"] for c in candidates_meta]

    # Fetch full content from MongoDB
    cursor = articles_col.find({"article_id": {"$in": ids}})
    candidates = await cursor.to_list(length=50)

    # Stage 2 & 3: TF-IDF + Semantic reranking
    candidates = tfidf_rerank(q, candidates)
    candidates = semantic_rerank(q, candidates)

    # Duplicate detection
    candidates = detect_duplicates(candidates[:top_k])
    return {"results": candidates, "query": q}

@router.get("/compare/")
async def compare(ids: str):
    id_list = ids.split(",")[:2]
    docs = []
    for aid in id_list:
        doc = await articles_col.find_one({"article_id": aid})
        if doc:
            docs.append(doc)
    if len(docs) < 2:
        return {"error": "Need two valid article IDs"}

    diff = compute_article_diff(docs[0]["content_clean"], docs[1]["content_clean"])
    return {
        "article_a": {
            "title": docs[0]["title"],
            "source": docs[0]["source_name"],
            "sentiment": score_title(docs[0]["title"]),
        },
        "article_b": {
            "title": docs[1]["title"],
            "source": docs[1]["source_name"],
            "sentiment": score_title(docs[1]["title"]),
        },
        "diff": diff,
    }
```

---

## 9. Project Folder Structure

```
bytebrief/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── news.py           # Article CRUD + digest endpoint
│   │   │   ├── search.py         # Whoosh search + compare endpoint
│   │   │   ├── users.py          # Auth, register, login
│   │   │   └── events.py         # User interaction tracking
│   │   ├── core/
│   │   │   ├── config.py         # Pydantic Settings (reads .env)
│   │   │   └── security.py       # JWT helpers
│   │   ├── db/
│   │   │   ├── mongo.py          # Motor client + collection refs
│   │   │   └── setup_indexes.py  # Run once to create MongoDB indexes
│   │   ├── scraper/
│   │   │   ├── spiders/          # Scrapy spiders per news source
│   │   │   ├── playwright_scraper.py
│   │   │   └── rss_fetcher.py
│   │   ├── nlp/
│   │   │   ├── summarizer.py     # BART/T5 NewsSummarizer class
│   │   │   ├── similarity.py     # TF-IDF + semantic + dedup
│   │   │   ├── sentiment.py      # VADER + RoBERTa
│   │   │   └── diff.py           # difflib sentence diff
│   │   ├── search/
│   │   │   ├── whoosh_setup.py   # Schema + index open/create
│   │   │   └── whoosh_search.py  # search_articles() + index_article()
│   │   ├── tasks/
│   │   │   ├── celery_app.py     # Celery app with MongoDB broker
│   │   │   ├── scrape_tasks.py   # Celery scraping tasks
│   │   │   └── nlp_tasks.py      # Digest, sentiment, embedding tasks
│   │   ├── personalization/
│   │   │   └── ranker.py         # score_article() + weight update
│   │   ├── evaluation/
│   │   │   └── eval.py           # ROUGE + BLEU evaluation script
│   │   └── main.py               # FastAPI app entry point
│   ├── data/
│   │   └── whoosh_index/         # Whoosh index files (auto-created)
│   ├── tests/
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── app/                      # Next.js 14 App Router
│   │   ├── page.js               # Home feed
│   │   ├── article/[id]/page.js  # Article + digest view
│   │   └── search/page.js        # Search & compare
│   ├── components/
│   │   ├── ArticleCard.jsx
│   │   ├── DigestPanel.jsx
│   │   ├── CompareView.jsx
│   │   ├── SearchBar.jsx
│   │   └── SentimentBadge.jsx
│   ├── store/
│   │   └── useNewsStore.js       # Zustand global state
│   ├── styles/
│   ├── .env.local
│   └── package.json
├── .env.example
└── README.md
```

---

## 10. Running the App — Local Setup

ByteBrief requires only **one external service: MongoDB**. Everything else (Whoosh index, Celery broker, NLP models) runs as Python processes or files on disk.

### 10.1 Prerequisites

| Tool    | Version  | Notes                                         |
| ------- | -------- | --------------------------------------------- |
| Python  | 3.11.x   | Use `pyenv` to manage: `pyenv install 3.11.9` |
| Node.js | 20.x LTS | Use `nvm`: `nvm install 20`                   |
| MongoDB | 7.x      | Only external service needed                  |
| Git     | Any      |                                               |

---

### 10.2 Step 1 — Install MongoDB

#### macOS (Homebrew)

```bash
brew tap mongodb/brew
brew update
brew install mongodb-community@7.0
brew services start mongodb-community@7.0

# Verify
mongosh --eval "db.runCommand({ connectionStatus: 1 })"
```

#### Ubuntu / Debian

```bash
# Import MongoDB GPG key
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc \
  | sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor

# Add repo
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] \
  https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" \
  | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

sudo apt update && sudo apt install -y mongodb-org
sudo systemctl start mongod && sudo systemctl enable mongod

# Verify
mongosh --eval "db.runCommand({ connectionStatus: 1 })"
```

#### Windows

Download and run the MongoDB Community Server installer from:
https://www.mongodb.com/try/download/community

Then start the service:

```powershell
net start MongoDB
```

---

### 10.3 Step 2 — Clone the Repo

```bash
git clone https://github.com/yourname/bytebrief.git
cd bytebrief
cp .env.example backend/.env
# Edit backend/.env — see Section 11
```

---

### 10.4 Step 3 — Backend Setup

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# Install all Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browser (for JS-heavy news sites)
playwright install chromium

# Set up MongoDB indexes (run once)
python -m app.db.setup_indexes

# Set up Whoosh index directory (auto-created on first search)
mkdir -p data/whoosh_index
```

---

### 10.5 `backend/requirements.txt`

```txt
# Web framework
fastapi==0.111.0
uvicorn[standard]==0.29.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9

# MongoDB (async)
motor==3.4.0
pymongo==4.7.2

# Task queue (MongoDB broker — no Redis needed)
celery==5.3.6
celery[mongodb]==5.3.6

# Scraping
scrapy==2.11.1
playwright==1.44.0
beautifulsoup4==4.12.3
trafilatura==1.9.0
feedparser==6.0.11

# Full-text search (pure Python, no server)
whoosh==2.7.4

# NLP — Summarization
transformers==4.40.0
torch==2.3.0
sentencepiece==0.2.0
accelerate==0.30.0

# NLP — Similarity & TF-IDF
scikit-learn==1.4.2
sentence-transformers==3.0.0
numpy==1.26.4

# NLP — Sentiment
vaderSentiment==3.3.2

# NLP — Evaluation
rouge-score==0.1.2
sacrebleu==2.4.0
datasets==2.19.0

# Utilities
python-dotenv==1.0.1
pydantic==2.7.1
pydantic-settings==2.2.1
httpx==0.27.0
loguru==0.7.2
spacy==3.7.4
```

After installing, download the spaCy model:

```bash
python -m spacy download en_core_web_sm
```

---

### 10.6 Step 4 — Configure Celery with MongoDB Broker

```python
# app/tasks/celery_app.py
from celery import Celery
from app.core.config import settings

# MongoDB as both broker and result backend — no Redis required
app = Celery(
    "bytebrief",
    broker=f"mongodb://{settings.MONGODB_HOST}:{settings.MONGODB_PORT}/bytebrief_celery",
    backend=f"mongodb://{settings.MONGODB_HOST}:{settings.MONGODB_PORT}/bytebrief_celery",
)

app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    beat_schedule={
        "scrape-all-sources": {
            "task": "app.tasks.scrape_tasks.scrape_all_sources",
            "schedule": 1800.0,   # every 30 minutes
        },
    },
)
```

---

### 10.7 Step 5 — Start Backend Services

You need **three terminal windows**:

**Terminal 1 — FastAPI server**

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 — Celery worker** (runs NLP tasks: digest, sentiment, embedding)

```bash
cd backend
source venv/bin/activate
celery -A app.tasks.celery_app worker --loglevel=info --concurrency=2
```

**Terminal 3 — Celery Beat** (runs the scraper scheduler)

```bash
cd backend
source venv/bin/activate
celery -A app.tasks.celery_app beat --loglevel=info
```

---

### 10.8 Step 6 — Frontend Setup

**Terminal 4 — Next.js**

```bash
cd frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm run dev
```

---

### 10.9 Step 7 — Trigger the First Scrape

```bash
# With venv active in the backend directory:
celery -A app.tasks.celery_app call app.tasks.scrape_tasks.scrape_all_sources
```

---

### 10.10 Verify Everything is Running

```bash
# MongoDB
mongosh bytebrief --eval "db.articles.countDocuments()"

# FastAPI
curl http://localhost:8000/api/v1/news/
# Expected: JSON array of articles

# Whoosh (check index exists)
ls backend/data/whoosh_index/
# Expected: several .seg, .toc, .lock files

# Test search
curl "http://localhost:8000/api/v1/search/?q=technology"
```

**Open the app:**

| Service      | URL                        |
| ------------ | -------------------------- |
| News Feed    | http://localhost:3000      |
| Backend API  | http://localhost:8000      |
| Swagger Docs | http://localhost:8000/docs |

---

### 10.11 Useful Commands

```bash
# Run ROUGE/BLEU evaluation
cd backend && source venv/bin/activate
python -m app.evaluation.eval --model bart --num_samples 200

# Run all tests
pytest tests/ -v

# Celery Flower dashboard (task monitor)
pip install flower
celery -A app.tasks.celery_app flower --port=5555
# Open: http://localhost:5555

# Rebuild Whoosh index from scratch (if index gets corrupted)
python -m app.search.rebuild_index

# MongoDB shell — inspect data
mongosh bytebrief
> db.articles.find().limit(3).pretty()
> db.articles.countDocuments({"digest_generated": true})

# Build Next.js for production
cd frontend && npm run build && npm start
```

---

## 11. Environment Variables Reference

```bash
# ── MongoDB ───────────────────────────────────────────────────────
MONGODB_URL=mongodb://localhost:27017
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DB_NAME=bytebrief

# ── Auth ─────────────────────────────────────────────────────────
SECRET_KEY=replace_with_a_long_random_string_minimum_32_characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# ── External APIs ─────────────────────────────────────────────────
NEWSAPI_KEY=your_key_from_newsapi_org

# ── NLP Model Settings ────────────────────────────────────────────
SUMMARIZER_MODEL=facebook/bart-large-cnn
# Alternatives: t5-base | google/flan-t5-large
SUMMARIZER_MAX_LENGTH=300
SUMMARIZER_MIN_LENGTH=80
SUMMARIZER_NUM_BEAMS=4

SIMILARITY_MODEL=all-mpnet-base-v2
DUPLICATE_THRESHOLD=0.78

# ── Scraper ───────────────────────────────────────────────────────
SCRAPE_INTERVAL_MINUTES=30
SCRAPER_USER_AGENT=ByteBriefBot/1.0

# ── Whoosh Index ─────────────────────────────────────────────────
WHOOSH_INDEX_DIR=./data/whoosh_index

# ── Frontend ─────────────────────────────────────────────────────
NEXT_PUBLIC_API_URL=http://localhost:8000
```

> **Security**: Never commit `.env` to version control. Add it to `.gitignore`. Only commit `.env.example` with placeholder values.

---

## 12. LLM-Ready Implementation Prompts

### 12.1 Master System Prompt

```
You are an expert full-stack engineer and NLP specialist. Build a web application called
ByteBrief — an AI-powered news aggregation platform. The stack uses NO Docker, NO Redis,
and NO Elasticsearch. MongoDB is the only database (and the Celery broker). Whoosh is the
full-text search library (pure Python, no server).

[1. SCRAPER] Build a Scrapy spider that scrapes BBC News. Extract: title, URL, publish_date,
author, full article text, and images. Use Playwright middleware for JS rendering. Clean text
using Trafilatura + spaCy. Store as a document in MongoDB (motor async driver) with fields:
article_id (sha256 of url), title, url, source_name, content_raw, content_clean, category,
publish_date, scraped_at. After saving, trigger Celery task post_process_article(article_id).
Schedule scraping every 30 minutes using Celery Beat with MongoDB as the broker.

[2. WHOOSH INDEXING] After each article is saved and cleaned, call index_article(article) to
write it into the Whoosh file-based index at ./data/whoosh_index/ using the schema:
article_id (ID, unique), title (TEXT, boost=2.0), content (TEXT), source_name (TEXT),
category (ID), publish_date (DATETIME), url (STORED).

[3. DIGEST] Build async FastAPI endpoint GET /api/v1/news/{id}/digest/ using Motor.
Check MongoDB for cached digest. If digest_generated=True, return it. Otherwise call
NewsSummarizer().summarize(content_clean) using facebook/bart-large-cnn with chunking
for long articles. Update MongoDB with the digest and digest_generated=True. Return JSON.

[4. SEARCH] Build GET /api/v1/search/?q={query}:
  Stage 1: search_articles(q, top_n=50) using Whoosh MultifieldParser on title+content
  Stage 2: tfidf_rerank(q, candidates) using scikit-learn TfidfVectorizer cosine similarity
  Stage 3: semantic_rerank(q, candidates) using sentence-transformers all-mpnet-base-v2,
           blend 0.4*tfidf_score + 0.6*semantic_score as final_score
  Stage 4: detect_duplicates(candidates, threshold=0.78) groups articles by pairwise
           semantic cosine similarity, adds same_story_group_id to each
Return top-20 results as JSON.

[5. COMPARE] Build GET /api/v1/search/compare/?ids=id1,id2:
Fetch both articles from MongoDB. Run compute_article_diff(text_a, text_b) using
difflib.SequenceMatcher on sentences. Run score_title() (VADER) on each title. Return:
article_a metadata + sentiment, article_b metadata + sentiment, diff with unique_to_a,
unique_to_b, and common lists.

[6. SENTIMENT] Celery task post_process_article(article_id): fetch article from MongoDB.
Apply VADER on title → store sentiment_score and sentiment_label. Apply
cardiffnlp/twitter-roberta-base-sentiment on first 512 tokens of content_clean →
update sentiment fields. Then generate and store embedding using sentence-transformers
all-mpnet-base-v2 → store as embedding array in MongoDB.

[7. EVALUATION] Build evaluation/eval.py: load CNN/DailyMail test split via HuggingFace
datasets. Generate 200 summaries using NewsSummarizer. Compute ROUGE-1, ROUGE-2, ROUGE-L
(F-measure) with rouge_scorer.RougeScorer. Compute BLEU-4 with sacrebleu.corpus_bleu.
Print mean ± std for each metric. Save to eval_report.json. CLI: --model (bart|t5), --num_samples.

[8. FRONTEND] Build React/Next.js 14 (App Router) CompareView component:
Props: articleA, articleB (each with title, source_name, sentiment, url).
Props: diff (unique_to_a[], unique_to_b[], common[]).
Layout: two columns, side by side. Highlight unique_to_a sentences with yellow background,
unique_to_b with blue background using Tailwind (bg-yellow-100, bg-blue-100).
Show SentimentBadge component (green=POSITIVE, red=NEGATIVE, gray=NEUTRAL) per column header.
Show a "Key Differences" card below with a count of unique sentences per side.

[9. CELERY MONGODB BROKER] Configure Celery in app/tasks/celery_app.py using MongoDB as
both broker and backend: broker="mongodb://localhost:27017/bytebrief_celery",
backend="mongodb://localhost:27017/bytebrief_celery". Add beat_schedule for scraping
every 30 minutes. No Redis. No RabbitMQ.

Tech versions: Python 3.11, FastAPI 0.111, Motor 3.4, MongoDB 7, Celery 5.3 with celery[mongodb],
Whoosh 2.7.4, transformers 4.40, sentence-transformers 3.0, scikit-learn 1.4, React 18,
Next.js 14, Tailwind CSS 3.4. Async Python throughout. loguru for logging. Include error handling.
```

---

### 12.2 Prompt A — Whoosh Search Module

```
Build app/search/whoosh_setup.py and app/search/whoosh_search.py for ByteBrief.

whoosh_setup.py:
- Define SCHEMA with fields: article_id (ID, stored, unique), title (TEXT, stored, boost=2.0),
  content (TEXT, not stored), source_name (TEXT, stored), category (ID, stored),
  publish_date (DATETIME, stored), url (STORED)
- Function create_or_open_index(index_dir="./data/whoosh_index") -> index
  Creates dir if not exists, creates index if not exists, else opens existing

whoosh_search.py:
- Function search_articles(query_str: str, top_n: int = 50) -> list[dict]
  Opens index, uses MultifieldParser on ["title", "content", "source_name"]
  Adds FuzzyTermPlugin for typo tolerance
  Returns list of dicts with article_id, title, source_name, score, url
- Function index_article(article: dict) -> None
  Opens index, calls writer.update_document() with all schema fields, commits
- Function rebuild_index(articles: list[dict]) -> None
  Deletes and recreates the index, reindexes all articles in batch

Include error handling for locked index (use AsyncWriter if needed).
```

---

### 12.3 Prompt B — MongoDB + Motor Setup

```
Build app/db/mongo.py and app/db/setup_indexes.py for ByteBrief.

mongo.py:
- AsyncIOMotorClient connected to settings.MONGODB_URL
- db = client[settings.MONGODB_DB_NAME]  (bytebrief)
- Expose collection references: articles_col, users_col, events_col, profiles_col

setup_indexes.py (run once via: python -m app.db.setup_indexes):
- articles: unique index on article_id, index on publish_date, source_name, category,
  whoosh_indexed, digest_generated. Compound text index on title+content_clean.
- users: unique index on email, index on username
- user_events: index on user_id, article_id, timestamp
- user_profiles: unique index on user_id

Print confirmation after each index is created.
```

---

### 12.4 Prompt C — Celery MongoDB Broker Config

```
Build app/tasks/celery_app.py for ByteBrief. Requirements:
- Use MongoDB as BOTH broker and result backend (no Redis, no RabbitMQ)
- broker = "mongodb://localhost:27017/bytebrief_celery"
- backend = "mongodb://localhost:27017/bytebrief_celery"
- Install: pip install "celery[mongodb]"
- task_serializer = "json", accept_content = ["json"]
- Beat schedule: scrape_all_sources every 30 minutes, generate_missing_digests every 2 hours
- Build app/tasks/scrape_tasks.py: task scrape_all_sources() that triggers one spider per source
- Build app/tasks/nlp_tasks.py: task post_process_article(article_id) that runs sentiment,
  embedding generation, and digest generation in sequence, then calls index_article()
Include proper Celery task retry logic with max_retries=3, countdown=60.
```

---

### 12.5 Prompt D — ROUGE/BLEU Evaluation Script

```
Build app/evaluation/eval.py for ByteBrief. Requirements:

1. CLI args: --model (bart|t5, default=bart), --num_samples (int, default=200)
2. Load CNN/DailyMail test split from HuggingFace datasets
3. Initialize NewsSummarizer with the chosen model
4. For each sample: generate summary, store (reference, hypothesis) pair
5. Compute ROUGE-1, ROUGE-2, ROUGE-L F-measure using rouge_scorer.RougeScorer
6. Compute corpus BLEU-4 using sacrebleu.corpus_bleu
7. Print a table: metric | mean | std | min | max
8. Save full per-sample results + aggregate to eval_report_{model}_{timestamp}.json
9. Add a --compare flag that runs both BART and T5 and prints a side-by-side comparison table
```

---

## 13. Development Roadmap

| Phase                 | Milestone                    | Key Deliverables                                                                                                                |
| --------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **Phase 1** (Wk 1–2)  | MongoDB + Scraper Foundation | MongoDB setup, indexes, Scrapy spiders for 3 sources, Celery with MongoDB broker, Playwright scraper, feedparser RSS            |
| **Phase 2** (Wk 3–4)  | NLP Pipeline                 | BART summarizer, Whoosh indexing, TF-IDF + semantic similarity modules, VADER + RoBERTa sentiment, embedding storage in MongoDB |
| **Phase 3** (Wk 5–6)  | Backend API                  | FastAPI async routes, Motor queries, JWT auth, search pipeline (Whoosh → TF-IDF → Semantic), compare/diff endpoint              |
| **Phase 4** (Wk 7–8)  | Frontend                     | Next.js 14 App Router, news feed, article + digest view, search results, compare view with diff highlighting, Zustand state     |
| **Phase 5** (Wk 9–10) | Personalization & Eval       | User event tracking, ranking score function, ROUGE/BLEU eval script, per-model comparison report                                |
| **Phase 6** (Wk 11+)  | Polish & Launch              | Production MongoDB config, model warm-up on startup, Whoosh async writer, load testing, full README                             |

---

## Quick-Start Cheatsheet

```bash
# 1. Start MongoDB (only external dependency)
brew services start mongodb-community@7.0   # macOS
sudo systemctl start mongod                 # Linux

# 2. Backend setup (one time)
cd backend && python3.11 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
python -m spacy download en_core_web_sm
python -m app.db.setup_indexes

# 3. Start everything (4 terminals)
uvicorn app.main:app --reload --port 8000           # Terminal 1
celery -A app.tasks.celery_app worker --concurrency=2  # Terminal 2
celery -A app.tasks.celery_app beat                    # Terminal 3
cd ../frontend && npm install && npm run dev            # Terminal 4

# 4. Trigger first scrape
celery -A app.tasks.celery_app call app.tasks.scrape_tasks.scrape_all_sources

# 5. Open app
open http://localhost:3000
```

---

_ByteBrief Project Blueprint — MongoDB-only stack, pure-Python Whoosh search, no Docker, no Redis, no Elasticsearch. Full NLP pipeline with BART/T5 digests, TF-IDF + semantic search, sentiment analysis, and ROUGE/BLEU evaluation._
