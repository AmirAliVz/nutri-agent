# NutriAgent 🥗

An AI-powered nutrition intelligence platform that understands natural language,
retrieves real nutrition data, stores your meal history, and generates personalized
health insights — built entirely on open-source models running locally.

> **Example:** `"I had 2 scrambled eggs and a Starbucks bacon wrap at 7am"`
> → structured meal data → full micronutrient breakdown → personalized AI insight

---

## What Makes This Different

Most nutrition apps make you search a database and tap through menus.
NutriAgent lets you describe what you ate in plain English — the same way
you would text a friend — and handles everything else automatically.

The platform is built as a production-grade AI engineering system, not a
school project. Every component is modular, documented, and designed to
be extended or extracted as a standalone library.

---

## Architecture Overview

```
User describes a meal in plain text
            ↓
  ┌─────────────────────────────────┐
  │   Meal Understanding Engine     │  ← Phase 1: LLM + Structured Output
  └─────────────────────────────────┘
            ↓
  ┌─────────────────────────────────┐
  │  Nutrition Retrieval Engine     │  ← Phase 2: USDA + Nutritionix + Web Search
  └─────────────────────────────────┘
            ↓
  ┌─────────────────────────────────┐
  │       Storage Layer             │  ← Phase 3: PostgreSQL + pgvector
  └─────────────────────────────────┘
            ↓
  ┌─────────────────────────────────┐
  │       Insight Engine            │  ← Phase 4: Generative AI
  └─────────────────────────────────┘
            ↓
  ┌─────────────────────────────────┐
  │     RAG Knowledge Base          │  ← Phase 5: Embeddings + Vector Search
  └─────────────────────────────────┘
            ↓
  ┌─────────────────────────────────┐
  │      API and Interface          │  ← Phase 6: FastAPI + Frontend
  └─────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Reason |
|---|---|---|
| Language | Python 3.13 | Dominant in AI/ML ecosystem |
| Backend Framework | FastAPI | Async, auto-generated docs, Pydantic native |
| Database | PostgreSQL 16 + pgvector | Relational and vector search in one service |
| Containerization | Docker + Docker Compose | Reproducible, portable environment |
| Dependency Management | Poetry | Professional dependency locking |
| LLM — Primary | Llama 3.1 8B via Ollama | Open source, runs locally, no API cost |
| Embeddings | nomic-embed-text via Ollama | Open source, local, free |
| LLM — Fallback | Anthropic Claude / OpenAI | Optional, for quality comparison only |
| Config Management | Pydantic Settings + YAML | Type-safe config, validated on startup |
| Code Quality | Ruff + pre-commit | Fast linting and formatting before every commit |

---

## Open Source Model Strategy

This project deliberately uses **open source models running locally** via
[Ollama](https://ollama.com) instead of closed API models. This means:

- **No API costs** during development or testing
- **No data leaving your machine** — complete privacy
- **Real hands-on experience** with model weights, quantization, and local inference
- **Fine-tuning capability** — you own the model and can adapt it to your data

### Models Used

| Model | Purpose | Parameters | Used in Phase |
|---|---|---|---|
| `llama3.1` | Meal parsing, insight generation, reasoning | 8B | 1, 2, 4 |
| `nomic-embed-text` | Text embeddings for RAG retrieval | 137M | 5 |
| `phi3` | Fine-tuning target on custom meal data | 3.8B | 8 |

Closed API models are configured as optional fallbacks in `.env` but the
entire platform runs without them.

---

## Project Structure

```
nutri-agent/
│
├── .env                          # Your secrets — never committed to GitHub
├── .env.example                  # Safe template for other developers
├── .gitignore                    # Protects secrets and build artifacts
├── .pre-commit-config.yaml       # Ruff linting runs before every commit
├── docker-compose.yml            # Runs PostgreSQL + backend as services
│
├── backend/
│   ├── Dockerfile                # Containerizes the Python backend
│   ├── config.yaml               # Non-secret application configuration
│   ├── pyproject.toml            # Poetry dependencies and project metadata
│   │
│   └── app/
│       ├── main.py               # FastAPI application entry point
│       │
│       ├── core/
│       │   └── config.py         # Loads .env and config.yaml with validation
│       │
│       ├── models/
│       │   └── database.py       # SQLAlchemy ORM table definitions
│       │
│       ├── api/
│       │   └── routes/           # API route handlers (built in Phase 6)
│       │
│       ├── services/             # Business logic layer
│       ├── agents/               # LLM agent implementations (Phase 2, 6)
│       ├── rag/                  # RAG pipeline components (Phase 5)
│       └── storage/              # Database access layer (Phase 3)
│
├── frontend/                     # UI (built in Phase 6)
├── docs/
│   └── diagrams/                 # Architecture and system diagrams
├── datasets/                     # Nutrition datasets (USDA FoodData Central etc.)
├── scripts/                      # Utility and data processing scripts
└── deployment/                   # Cloud deployment configuration
```

---

## Database Schema

The database is organized around four core tables:

```
users
  └── meals              (one user has many meals)
        └── food_items   (one meal has many food items)
              └── nutrition_facts  (one food item has one nutrition record)

insights               (linked to meals — AI-generated analysis per meal)
```

### nutrition_facts columns

| Category | Columns |
|---|---|
| Macros | calories, protein, fat, carbohydrates, fiber, sugar |
| Micros | sodium, potassium, calcium, iron, magnesium, zinc |
| Vitamins | vitamin_a, vitamin_c, vitamin_d, vitamin_b12 |
| Fat breakdown | saturated_fat, unsaturated_fat, omega_3 |
| Metadata | food_name, brand, source, cached_at |

Full schema is defined in `backend/app/models/database.py` using SQLAlchemy ORM.

The database runs PostgreSQL 16 with the `pgvector` extension enabled,
which allows storing and searching vector embeddings in the same database
used for all relational data. No separate vector database service is needed.

---

## Nutrition Data Strategy

Food nutrition data is retrieved through a three-layer fallback pipeline:

```
Food item identified
        ↓
Layer 1: USDA FoodData Central (local database)
  Best for raw ingredients — eggs, chicken, rice, vegetables
  Complete micronutrient data including amino acids and omega fatty acids
  Free, fully offline, government-verified
        ↓ (if not found)
Layer 2: Nutritionix API
  Best for branded and restaurant items — Starbucks, McDonald's, packaged goods
  Official menu and label nutrition data
  Free tier available
        ↓ (if not found)
Layer 3: Web Search Agent (LLM-powered fallback)
  Handles anything not covered by the databases above
  LLM searches the web, reads nutrition pages, extracts structured data
  Result is cached locally so each item is only searched once
        ↓
Result cached in local database
  Every retrieved nutrition record is stored permanently
  Over time the system builds its own nutrition knowledge base
  External lookups decrease as the cache grows
```

---

## Development Roadmap

| Phase | Name | Status | Skills Demonstrated |
|---|---|---|---|
| **Phase 0** | Foundation and Architecture | ✅ Complete | Docker, FastAPI, PostgreSQL, Poetry, project architecture |
| **Phase 1** | Meal Understanding Engine | 🔄 In Progress | LLMs, prompt engineering, structured output, Pydantic |
| **Phase 2** | Nutrition Retrieval Engine | ⏳ Planned | Tool calling, API integration, web search agents, caching |
| **Phase 3** | Storage Layer | ⏳ Planned | Database design, SQLAlchemy, Alembic migrations |
| **Phase 4** | Insight Engine | ⏳ Planned | Generative AI, prompt chaining, context management |
| **Phase 5** | RAG Knowledge Base | ⏳ Planned | RAG, embeddings, vector search, chunking, retrieval |
| **Phase 6** | API and Interface | ⏳ Planned | REST APIs, CORS, frontend integration, end-to-end |

### Future Phases (post-MVP)

| Phase | Name | Skills |
|---|---|---|
| Phase 7 | Nutrition Intelligence and Analytics | Time series, clustering, recommendation systems |
| Phase 8 | Fine-Tuning Pipeline | LoRA, QLoRA, Hugging Face PEFT, GPU optimization |
| Phase 9 | Evaluation Framework | RAGAS, DeepEval, precision, recall, hallucination detection |
| Phase 10 | Cloud Deployment | Docker, CI/CD, GitHub Actions, Railway, Vercel |

---

## Getting Started

### Prerequisites

Make sure you have all of these installed before continuing:

| Tool | Purpose | Download |
|---|---|---|
| Python 3.11+ | Runtime | [python.org](https://python.org) |
| Docker Desktop | Runs PostgreSQL locally | [docker.com](https://docker.com) |
| Poetry | Python dependency management | [python-poetry.org](https://python-poetry.org) |
| Ollama | Runs open source LLMs locally | [ollama.com](https://ollama.com) |
| Git | Version control | [git-scm.com](https://git-scm.com) |

Verify each one is installed:

```bash
python --version
docker --version
poetry --version
ollama --version
git --version
```

---

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/nutri-agent.git
cd nutri-agent
```

---

### 2. Set Up Environment Variables

```bash
# Windows
copy .env.example .env

# Mac / Linux
cp .env.example .env
```

Open `.env` in your editor. For local development with Ollama, no API keys
are required — all default values work out of the box.

See the [Environment Variables Reference](#environment-variables-reference)
section below for a full description of each variable.

---

### 3. Pull the Open Source Models

This downloads the models to your machine. One-time download, approximately 5GB total.

```bash
ollama pull llama3.1
ollama pull nomic-embed-text
```

Verify Llama is working:

```bash
ollama run llama3.1
```

Type anything and it should respond. Type `/bye` to exit.

---

### 4. Install Python Dependencies

```bash
cd backend
poetry install
```

This creates an isolated virtual environment and installs all packages
defined in `pyproject.toml`.

---

### 5. Start the Database

**Important:** Docker Desktop must be open and showing "running" in your
taskbar before this command will work.

```bash
# From the nutri-agent root directory
docker compose up postgres -d
```

The `-d` flag runs the database in the background so your terminal stays free.

Verify the database started successfully:

```bash
docker ps
```

You should see `nutriagent_db` with status `Up (healthy)`.

---

### 6. Start the Backend

```bash
cd backend
poetry run uvicorn app.main:app --reload
```

The `--reload` flag automatically restarts the server when you change code.

---

### 7. Verify Everything Works

Open your browser and visit each of these URLs:

| URL | Expected Response |
|---|---|
| `http://127.0.0.1:8000` | `{"message": "NutriAgent API is running"}` |
| `http://127.0.0.1:8000/health` | App name, version, environment status |
| `http://127.0.0.1:8000/docs` | Interactive API documentation (Swagger UI) |
| `http://127.0.0.1:8000/redoc` | Alternative API documentation (ReDoc) |

The `/docs` page is automatically generated by FastAPI from your code.
No extra setup required.

---

## Daily Development Workflow

Every time you sit down to work on this project, follow this sequence:

```
1. Open Docker Desktop
   Wait until the whale icon in your taskbar shows "Docker Desktop is running"

2. Open VS Code in the nutri-agent folder
   code .

3. Open the integrated terminal in VS Code
   Terminal menu → New Terminal

4. Start the database
   docker compose up postgres -d

5. Start the backend
   cd backend
   poetry run uvicorn app.main:app --reload

6. Open browser at http://127.0.0.1:8000
```

### Stopping Everything

```bash
# Stop the backend
Ctrl+C   (in the terminal running uvicorn)

# Stop the database
docker compose down
```

---

## Environment Variables Reference

All variables live in your `.env` file in the project root.
Never commit `.env` to GitHub — it is listed in `.gitignore`.

| Variable | Description | Default / Example |
|---|---|---|
| `APP_ENV` | Environment name | `development` |
| `DEBUG` | Enable debug mode and detailed errors | `true` |
| `SECRET_KEY` | App secret key for tokens | any long random string |
| `ANTHROPIC_API_KEY` | Anthropic API key — optional, fallback only | `not-needed-using-ollama` |
| `OPENAI_API_KEY` | OpenAI API key — optional, fallback only | `not-needed-using-ollama` |
| `OLLAMA_BASE_URL` | Address where Ollama is running | `http://localhost:11434` |
| `OLLAMA_MODEL` | Primary local LLM to use | `llama3.1` |
| `OLLAMA_EMBED_MODEL` | Embedding model for RAG | `nomic-embed-text` |
| `DATABASE_URL` | Full PostgreSQL connection string | `postgresql+asyncpg://nutriagent:nutriagent@localhost:5432/nutriagent` |
| `POSTGRES_USER` | Database username | `nutriagent` |
| `POSTGRES_PASSWORD` | Database password | `nutriagent` |
| `POSTGRES_DB` | Database name | `nutriagent` |

---

## Key Design Decisions

### Why open source models instead of closed APIs?

Using Llama 3.1 locally via Ollama means understanding what actually happens
when a model runs — quantization formats, VRAM usage, inference speed tradeoffs,
and prompt sensitivity. Calling an API abstracts all of that away. For a
portfolio project designed to demonstrate real AI engineering skills, that
abstraction is a disadvantage. Closed APIs are configured as optional fallbacks
for quality comparison but are never required.

### Why PostgreSQL + pgvector instead of a dedicated vector database?

Keeping relational meal data and vector embeddings in one database eliminates
an entire service from the stack. pgvector handles the retrieval scale of this
project comfortably, and using SQL for both structured queries and vector
similarity search is a more transferable skill than learning a proprietary
vector database interface. Chroma or Qdrant can be added later if the scale
demands it.

### Why FastAPI instead of Django or Flask?

FastAPI is async-native, generates OpenAPI documentation automatically from
type annotations, has Pydantic validation built in, and is the current
industry standard for Python AI backends. Django is better suited for
full-stack web apps with admin panels. Flask is too minimal for a project
of this complexity.

### Why Poetry instead of pip?

Poetry produces a `poetry.lock` file that guarantees identical installs
across different machines and operating systems. `pyproject.toml` is the
modern Python standard for project metadata. `pip` with `requirements.txt`
has no locking mechanism and leads to dependency conflicts over time.

### Why a monorepo structure?

All components — backend, frontend, agents, RAG pipeline, datasets, and
deployment — live in one repository. For a solo project this reduces
management overhead significantly. The folder structure enforces clear
separation between components without requiring separate repositories
and their associated coordination cost.

---

## Learning Objectives

This project is designed to build hands-on experience across the complete
AI engineering stack in deliberate progression:

```
Phase 0  →  Software architecture, Docker, project organization, Git workflow
Phase 1  →  LLM APIs, prompt engineering, structured outputs, Pydantic validation
Phase 2  →  Tool calling, web search agents, API integration, caching patterns
Phase 3  →  Database design, SQLAlchemy ORM, Alembic migrations, data modeling
Phase 4  →  Generative AI, prompt chaining, context window management
Phase 5  →  RAG pipeline, embeddings, vector databases, chunking, retrieval
Phase 6  →  REST API design, CORS, end-to-end integration, minimal frontend
Phase 8  →  Fine-tuning with LoRA and QLoRA, Hugging Face PEFT, GPU optimization
Phase 9  →  LLM evaluation, RAGAS framework, hallucination detection, benchmarking
Phase 10 →  Docker in production, CI/CD with GitHub Actions, cloud deployment
```

Each phase produces a working, testable component — not just exploratory code.

---

## Dependencies

Core dependencies are managed by Poetry and defined in `backend/pyproject.toml`.

| Package | Purpose |
|---|---|
| `fastapi` | Web framework |
| `uvicorn` | ASGI server |
| `pydantic` | Data validation |
| `pydantic-settings` | Environment variable loading |
| `sqlalchemy` | Database ORM |
| `asyncpg` | Async PostgreSQL driver |
| `alembic` | Database migration tool |
| `pgvector` | Vector operations for PostgreSQL |
| `pyyaml` | YAML config file parsing |
| `httpx` | Async HTTP client for API calls |
| `anthropic` | Anthropic API client (optional fallback) |
| `openai` | OpenAI API client (optional fallback) |
| `ollama` | Ollama Python client for local models |
| `python-dotenv` | .env file loading |

Development dependencies:

| Package | Purpose |
|---|---|
| `ruff` | Linting and formatting |
| `pytest` | Testing framework |
| `pytest-asyncio` | Async test support |
| `pre-commit` | Git hook management |

---

## Contributing

This is a personal portfolio project but contributions, suggestions, and
issue reports are welcome.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Run linting: `poetry run ruff check .`
5. Commit: `git commit -m "descriptive message"`
6. Push: `git push origin feature/your-feature-name`
7. Open a pull request

---

## License

MIT License

Copyright (c) 2026 Amir

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

*NutriAgent — Built by Amir as a flagship AI/ML portfolio project*