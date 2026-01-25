# AI-Powered Book Platform

A comprehensive AI-driven book platform built with Docusaurus, FastAPI, and advanced RAG capabilities.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AI-Powered Book Platform                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    FRONTEND (Docusaurus)                            │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────────────────┐ │   │
│  │  │ Book     │ │ Chapters │ │ User     │ │ Embedded RAG Chatbot   │ │   │
│  │  │ Navigation│ │ MDX      │ │ Profile  │ │ - General Q&A          │ │   │
│  │  └──────────┘ └──────────┘ └──────────┘ │ - Selected Text Q&A    │ │   │
│  │                                          │ - Citations            │ │   │
│  │  ┌──────────────────────────────────────┴────────────────────────┐ │   │
│  │  │ Features: Personalization | Urdu Translation | Auth           │ │   │
│  │  └───────────────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    BACKEND (FastAPI)                                │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                │   │
│  │  │ Auth API     │ │ Chat API     │ │ Content API  │                │   │
│  │  │ (Better-Auth)│ │ (RAG)        │ │ (Personalize)│                │   │
│  │  └──────────────┘ └──────────────┘ └──────────────┘                │   │
│  │                          │                                          │   │
│  │  ┌───────────────────────┴───────────────────────┐                 │   │
│  │  │              AI Services Layer                 │                 │   │
│  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐         │                 │   │
│  │  │  │OpenAI   │ │Embedding│ │Translation│        │                 │   │
│  │  │  │Agents   │ │Service  │ │Service   │         │                 │   │
│  │  │  └─────────┘ └─────────┘ └─────────┘         │                 │   │
│  │  └───────────────────────────────────────────────┘                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                          │                   │                              │
│                          ▼                   ▼                              │
│  ┌────────────────────────────┐ ┌────────────────────────────┐            │
│  │   Neon Postgres            │ │   Qdrant Cloud             │            │
│  │   - Users                  │ │   - Book Embeddings        │            │
│  │   - Sessions               │ │   - Semantic Search        │            │
│  │   - User Profiles          │ │   - RAG Retrieval          │            │
│  │   - Cached Content         │ │                            │            │
│  └────────────────────────────┘ └────────────────────────────┘            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 📚 Features

### Core Features
- **📖 AI-Generated Book Content** - Using Spec-Kit Plus methodology
- **💬 Embedded RAG Chatbot** - Context-aware Q&A with citations
- **🔍 Smart Search** - Semantic search across all book content

### Bonus Features
- **🔐 Authentication** - Secure signup/signin with Better-Auth
- **👤 User Profiling** - Personalized experience based on user background
- **✨ Content Personalization** - AI-adapts content to user skill level
- **🌐 Urdu Translation** - Dynamic translation preserving code blocks

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Docusaurus 3.x |
| Backend | FastAPI |
| Database | Neon Serverless Postgres |
| Vector DB | Qdrant Cloud |
| Auth | Better-Auth |
| AI/LLM | OpenAI Agents SDK |
| Deployment | GitHub Pages (Frontend), Docker (Backend) |

## 📁 Project Structure

```
giaic-hackathon/
├── frontend/                 # Docusaurus site
│   ├── docs/                # Book chapters (MDX)
│   ├── src/
│   │   ├── components/      # React components
│   │   │   └── Chatbot/     # Embedded RAG chatbot
│   │   └── pages/           # Custom pages
│   └── docusaurus.config.js
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── api/             # API routes
│   │   ├── core/            # Config, security
│   │   ├── models/          # Database models
│   │   ├── schemas/         # Pydantic schemas
│   │   └── services/        # Business logic
│   └── tests/
├── ai-services/             # AI service modules
│   ├── rag/                 # RAG pipeline
│   ├── embeddings/          # Embedding generation
│   ├── personalization/     # Content personalization
│   └── translation/         # Urdu translation
├── subagents/               # Claude Code subagents
└── docs/                    # Project documentation
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Docker (optional)

### Frontend Setup
```bash
cd frontend
npm install
# Create .env file with API configuration
echo "REACT_APP_API_BASE_URL=http://localhost:8000" > .env
npm start
```

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Port Configuration
- **Backend API**: Runs on `http://localhost:8000` by default
- **Frontend**: Runs on `http://localhost:3000` by default
- **Chatbot Integration**: Connects to backend API at `http://localhost:8000`

### Environment Variables
Create `.env` files in both `frontend/` and `backend/` directories:

**backend/.env**
```
DATABASE_URL=postgresql://...@neon.tech/...
QDRANT_URL=https://...qdrant.io
QDRANT_API_KEY=...
OPENAI_API_KEY=...
BETTER_AUTH_SECRET=...
```

## 📖 Book Structure (Spec-Kit Plus)

Each chapter follows the Spec-Kit Plus methodology:
1. **Objective** - Clear learning goals
2. **Concepts** - Core theoretical concepts
3. **Examples** - Practical code examples
4. **Exercises** - Hands-on practice
5. **Summary** - Key takeaways

## 🤖 Claude Code Subagents

| Subagent | Purpose |
|----------|---------|
| `chapter-generator` | Generate book chapters from specs |
| `spec-converter` | Convert specs to structured content |
| `embedding-ingester` | Process and store embeddings |
| `qa-tester` | Quality assurance testing |

## 📦 Deployment

### Frontend (GitHub Pages)
```bash
cd frontend
npm run build
npm run deploy
```

### Backend (Docker)
```bash
cd backend
docker build -t book-platform-api .
docker run -p 8000:8000 book-platform-api
```

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- [Spec-Kit Plus](https://github.com/panaversity/spec-kit-plus/) - Methodology
- [Docusaurus](https://docusaurus.io/) - Documentation framework
- [Better-Auth](https://better-auth.com/) - Authentication
- [Qdrant](https://qdrant.tech/) - Vector database
- [Neon](https://neon.tech/) - Serverless Postgres
