# ByteBrief 📰

**Smart News Digest for Busy Humans**

ByteBrief is an intelligent news aggregation and summarization platform. It scrapes news from various online sources and delivers concise, personalized digests for people who want to stay informed without spending hours reading.

## Project Overview

In today's fast-paced world, staying updated with current events is crucial but time-consuming. ByteBrief solves this by automatically collecting news from multiple sources, analyzing the content, using AI agents to fetch and summarize news, and presenting it in a clean, modern web interface.

## Tech Stack

*   **Frontend**: React, TailwindCSS, Lucide React
*   **Backend**: Django, Python 3.12+
*   **Package Manager**: `uv` (for Python)
*   **Database**: SQLite (default for dev)

## Project Structure

```
ByteBrief/
├── Frontend/           # React Application
│   ├── src/
│   ├── public/
│   └── package.json
├── backend/            # Django Backend
│   ├── manage.py
│   ├── pyproject.toml
│   ├── src/
│   └── ...
└── README.md
```

## Getting Started

Follow these steps to set up the project locally.

### Prerequisites

*   **Python 3.12+**
*   **Node.js 18+** & **npm**
*   **uv** (Python package manager) - [Install uv](https://github.com/astral-sh/uv)

### Backend Setup

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```

2.  Sync dependencies (creates virtual environment automatically):
    ```bash
    uv sync
    ```

3.  Apply migrations:
    ```bash
    uv run python manage.py migrate
    ```

4.  Start the Development Server:
    ```bash
        uv run python manage.py migrate

    ```
    The backend API will be available at `http://locacdlhost:8000`.

### Frontend Setup

1.  Open a new terminal and navigate to the `Frontend` directory:
    ```bash
    cd Frontend
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

3.  Start the Development Server:
    ```bash
    npm start
    ```
    The application will open at `http://localhost:3000`.

## Features

*   **🕷️ News Scraper**: Collects news from various sources.
*   **🤖 AI Agents**: Specialized agents for different categories (Breaking, Tech, Business, etc.).
*   **📝 Summarization**: Generates concise summaries of articles.
*   **💻 Modern UI**: Clean, responsive interface built with React and TailwindCSS.
*   **🌙 Light/Dark Mode**: (Coming soon/In progress)

## Contributing

We welcome contributions! Please fork the repository and submit a pull request.

## License

*To be determined*

---

**Mission**: *Making news consumption efficient, intelligent, and accessible for everyone.*
