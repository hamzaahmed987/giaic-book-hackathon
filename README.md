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
│  │  │           │ │          │ │          │ │ - Selected Text Q&A    │ │   │
│  │  │           │ │          │ │          │ │ - Citations            │ │   │
│  │  │           │ │          │ │          │ │ - Personalization      │ │   │
│  │  └──────────┴ └──────────┴ └──────────┴ └────────────────────────┘ │   │
│  │  ┌─────────────────────────────────────────────────────────────────┐ │ │
│  │  │ Features: Personalization | Urdu Translation | Auth             │ │ │
│  │  └─────────────────────────────────────────────────────────────────┘ │ │
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
│  │  │  │Agents   │ │Service  │ │Service   │        │                 │   │
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
| Deployment | Vercel (Frontend & Backend) |

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
├── backend/                  # FastAPI backend (Vercel-optimized)
│   ├── app/
│   │   ├── api/             # API routes
│   │   ├── core/            # Config, security
│   │   ├── models/          # Database models
│   │   ├── schemas/         # Pydantic schemas
│   │   └── services/        # Business logic
│   ├── vercel.json          # Vercel configuration
│   └── requirements.txt
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

### Frontend Setup
```bash
cd frontend
npm install
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
OPENROUTER_API_KEY=...
SECRET_KEY=your-super-secret-key-change-in-production
```

## 📦 Vercel Deployment

### Frontend Deployment
1. Push your code to a GitHub repository
2. Go to [Vercel](https://vercel.com) and connect your GitHub account
3. Import your frontend repository
4. Set build command to `npm run build` and output directory to `build`
5. Add environment variables in Vercel dashboard:
   - `API_BASE_URL`: URL of your deployed backend (e.g., `https://your-backend.vercel.app/api`)

### Backend Deployment
1. Push your code to a GitHub repository
2. Go to [Vercel](https://vercel.com) and connect your GitHub account
3. Import your backend repository
4. Vercel will automatically detect the Python project and use the `vercel.json` configuration
5. Add environment variables in Vercel dashboard:
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `QDRANT_URL`: Your Qdrant cloud instance URL
   - `QDRANT_API_KEY`: Your Qdrant API key
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `SECRET_KEY`: A strong secret key for JWT tokens

### Configuration Notes
- The backend is optimized for Vercel serverless functions with connection pooling adjustments
- Database migrations should be run separately during deployment (not in the application startup)
- External services (PostgreSQL, Qdrant, Redis) remain as external dependencies

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

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- [Spec-Kit Plus](https://github.com/panaversity/spec-kit-plus/) - Methodology
- [Docusaurus](https://docusaurus.io/) - Documentation framework
- [Better-Auth](https://better-auth.com/) - Authentication
- [Qdrant](https://qdrant.tech/) - Vector database
- [Neon](https://neon.tech/) - Serverless Postgres
- [Vercel](https://vercel.com/) - Deployment platform