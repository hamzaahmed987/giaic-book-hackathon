# Project Development History

## AI-Powered Book Platform - Complete Build Log

**Project Start:** January 21, 2026
**Developer:** Claude Code (Opus 4.5)
**Total Files Created:** 83+

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Development Timeline](#development-timeline)
4. [Architecture Decisions](#architecture-decisions)
5. [Implementation Details](#implementation-details)
6. [File Structure](#file-structure)
7. [Features Implemented](#features-implemented)
8. [Challenges & Solutions](#challenges--solutions)
9. [Future Improvements](#future-improvements)

---

## 🎯 Project Overview

### Goal
Build a unified AI-driven book platform using Spec-Kit Plus methodology and Claude Code, published with Docusaurus on GitHub Pages, enhanced with an embedded RAG chatbot capable of personalized, contextual, and multilingual (Urdu) responses.

### Requirements Fulfilled

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Docusaurus Book Platform | ✅ Complete | 6 chapters with MDX |
| Spec-Kit Plus Methodology | ✅ Complete | 5 sections per chapter |
| RAG Chatbot | ✅ Complete | OpenRouter + Cohere + Qdrant |
| Authentication | ✅ Complete | JWT + Cookies |
| User Profiling | ✅ Complete | 4 profile dimensions |
| Content Personalization | ✅ Complete | AI-driven adaptation |
| Urdu Translation | ✅ Complete | Code-preserving translation |
| Claude Code Subagents | ✅ Complete | 4 agents + 9 skills |

---

## 🛠 Technology Stack

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| Docusaurus | 3.9.2 | Documentation framework |
| React | 19.0.0 | UI components |
| TypeScript | 5.6.2 | Type safety |
| MDX | 3.0.0 | Enhanced markdown |

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| FastAPI | 0.109+ | API framework |
| SQLAlchemy | 2.0+ | ORM |
| Pydantic | 2.5+ | Validation |
| asyncpg | 0.29+ | Async Postgres driver |

### AI/ML
| Technology | Purpose |
|------------|---------|
| OpenRouter API | LLM chat completions (multi-model access) |
| Cohere API | Embeddings (embed-english-v3.0) |
| Qdrant | Vector database |
| OpenAI SDK | API client (compatible with OpenRouter) |

### Infrastructure
| Technology | Purpose |
|------------|---------|
| Docker | Containerization |
| GitHub Actions | CI/CD |
| Neon Postgres | Serverless database |
| Qdrant Cloud | Managed vector DB |

---

## ⏱ Development Timeline

### Phase 1: Project Initialization (Step 1-3)

**What was done:**
1. Created root project structure
2. Initialized Git repository
3. Created comprehensive README.md with architecture diagram
4. Set up .gitignore

**Commands used:**
```bash
mkdir -p frontend backend/app ai-services subagents docs .github/workflows
git init && git branch -M main
```

**Key files created:**
- `README.md` - Project documentation with ASCII architecture diagram
- `.gitignore` - Ignore patterns for Node, Python, IDE files

---

### Phase 2: Docusaurus Setup (Step 4-6)

**What was done:**
1. Created Docusaurus project with TypeScript
2. Configured for book-style documentation
3. Set up sidebar navigation for 6 chapters

**Commands used:**
```bash
npx create-docusaurus@latest frontend classic --typescript
```

**Configuration changes:**
- `docusaurus.config.ts` - Custom branding, GitHub Pages config, disabled blog
- `sidebars.ts` - Book structure with chapters and sections

**Key decisions:**
- Used `routeBasePath: 'book'` to serve docs under /book path
- Enabled `showLastUpdateTime` for transparency
- Added Prism languages: python, bash, json, typescript, sql

---

### Phase 3: Book Content Creation (Step 7-15)

**Methodology: Spec-Kit Plus**

Each chapter follows this structure:
```
chapter-N/
├── overview.mdx    → Learning Objectives
├── concepts.mdx    → Core Theory
├── examples.mdx    → Practical Code
├── exercises.mdx   → Hands-on Practice
└── summary.mdx     → Key Takeaways
```

**Chapters Created:**

| Chapter | Topic | Key Concepts |
|---------|-------|--------------|
| 1 | AI Foundations | AI/ML/DL hierarchy, history, types |
| 2 | LLM Fundamentals | Transformers, tokenization, APIs |
| 3 | Prompt Engineering | CRAFT framework, few-shot, CoT |
| 4 | RAG Systems | Chunking, embeddings, retrieval |
| 5 | AI Agents | Function calling, agent loop |
| 6 | Building AI Apps | Full-stack architecture |

**Content features:**
- Mermaid diagrams for visual learning
- Tabs component for multiple perspectives
- Details component for collapsible solutions
- Admonitions (tip, info, caution) for callouts
- Complete, runnable code examples

**Total content files:** 31 MDX files

---

### Phase 4: React Components (Step 16-20)

**Components Created:**

#### 1. ChapterActions (`/src/components/ChapterActions/`)
```
Purpose: Personalization and translation buttons at chapter start
Features:
- "Personalize this chapter" button
- "Translate to Urdu" button
- Loading states with spinners
- Active state indicators
```

#### 2. Chatbot (`/src/components/Chatbot/`)
```
Purpose: Embedded RAG chatbot for Q&A
Features:
- Floating toggle button (bottom-right)
- Message history with user/assistant styling
- Text selection detection
- Citation display with links
- Typing indicator animation
- Responsive design (mobile-friendly)
```

#### 3. AuthContext (`/src/context/AuthContext.tsx`)
```
Purpose: Global authentication state management
Features:
- User state (id, email, name, profile)
- signIn, signUp, signOut methods
- Profile update functionality
- Automatic session check on load
```

#### 4. Profile Page (`/src/pages/profile.tsx`)
```
Purpose: User registration and profile management
Features:
- Sign up / Sign in forms
- Experience level selection (radio)
- Programming languages (chips)
- Hardware tier selection
- Learning goals (chips)
```

#### 5. Homepage (`/src/pages/index.tsx`)
```
Purpose: Landing page with feature showcase
Features:
- Hero section with gradient background
- 6 feature cards
- Chapter preview grid
- Call-to-action section
```

---

### Phase 5: Backend Development (Step 21-35)

**Architecture: Clean Architecture**

```
backend/app/
├── api/routes/      → HTTP endpoints
├── core/            → Config, security, deps
├── models/          → SQLAlchemy models
├── schemas/         → Pydantic schemas
├── services/        → Business logic
└── infrastructure/  → Database, vector store
```

#### Core Module

**config.py**
```python
Settings using pydantic-settings:
- DATABASE_URL (Neon Postgres)
- QDRANT_URL, QDRANT_API_KEY
- OPENAI_API_KEY, OPENAI_MODEL
- SECRET_KEY, ALGORITHM
- CORS_ORIGINS
```

**security.py**
```python
Functions:
- verify_password() - bcrypt verification
- get_password_hash() - bcrypt hashing
- create_access_token() - JWT creation
- decode_token() - JWT decoding
```

**deps.py**
```python
Dependencies:
- get_db() - Async database session
- get_current_user() - Extract user from cookie
- get_current_user_required() - Require authentication
```

#### Models

**User Model**
```python
Fields:
- id (UUID)
- email (unique)
- hashed_password
- name
- created_at, updated_at
Relationship: profile (UserProfile)
```

**UserProfile Model**
```python
Fields:
- experience_level (enum: beginner/intermediate/advanced)
- known_languages (JSON array)
- hardware_tier (enum: low/medium/high)
- goals (JSON array)
```

**CachedContent Model**
```python
Purpose: Cache personalized/translated content
Fields:
- user_id, chapter_id, content_type
- content (Text)
- expires_at
Index: (user_id, chapter_id, content_type)
```

#### Services

**EmbeddingService**
```python
Methods:
- get_embedding(text) → List[float]
- get_embeddings(texts, input_type) → List[List[float]]
Provider: Cohere
Model: embed-english-v3.0 (1024 dimensions)
```

**RAGService**
```python
Methods:
- query(query, selected_text, chapter_filter, user_profile)

Pipeline:
1. Build full query with selected text context
2. Generate query embedding
3. Search Qdrant for top-k similar chunks
4. Build context from retrieved documents
5. Generate response with citations
```

**PersonalizationService**
```python
Methods:
- personalize_content(content, user_profile, chapter_id, db)

Pipeline:
1. Check cache for existing personalization
2. Build prompt with user profile details
3. Call GPT-4 to adapt content
4. Cache result for 7 days
5. Return personalized content
```

**TranslationService**
```python
Methods:
- translate_to_urdu(content, chapter_id, user_id, db)

Pipeline:
1. Check cache for existing translation
2. Extract code blocks with regex
3. Replace with placeholders
4. Translate text content to Urdu
5. Restore code blocks
6. Cache result for 30 days
```

#### API Routes

**Auth Routes (`/api/auth/`)**
```
POST /signup    → Create user + profile + set cookie
POST /signin    → Verify credentials + set cookie
POST /signout   → Delete cookie
GET  /me        → Get current user
PATCH /profile  → Update user profile
```

**Chat Routes (`/api/chat/`)**
```
POST /query     → RAG-powered Q&A
GET  /health    → Service health check
```

**Content Routes (`/api/content/`)**
```
POST /personalize  → Get personalized chapter (auth required)
POST /translate    → Get Urdu translation
GET  /chapter/{id} → Get original chapter content
```

---

### Phase 6: Infrastructure (Step 36-40)

**Docker Configuration**

`Dockerfile`:
```dockerfile
- Base: python:3.11-slim
- Non-root user for security
- Health check endpoint
- Uvicorn server on port 8000
```

`docker-compose.yml`:
```yaml
Services:
- backend (FastAPI app)
- postgres (PostgreSQL 15)
- redis (Redis 7)
- qdrant (Vector DB)
Volumes for data persistence
```

**GitHub Actions (`deploy.yml`)**
```yaml
Jobs:
1. build-frontend  → Build Docusaurus
2. deploy-frontend → Deploy to GitHub Pages
3. build-backend   → Build & push Docker image
4. test            → Run pytest
5. lint            → Run ruff + black
```

**Environment Configuration**
```
.env.example with all required variables:
- Database connection strings
- API keys
- Security secrets
- CORS origins
```

---

### Phase 7: Claude Code Subagents (Step 41-45)

**Subagents Created:**

#### 1. chapter-generator.md
```
Purpose: Generate book chapters from specs
Input: Topic, prerequisites, target level
Output: 5 MDX files following Spec-Kit Plus
Features: Mermaid diagrams, code examples, exercises
```

#### 2. spec-converter.md
```
Purpose: Convert raw specs to educational content
Input: API docs, technical specs, outlines
Output: Learner-friendly documentation
Features: Analogies, examples, tables
```

#### 3. embedding-ingester.md
```
Purpose: Process and store book embeddings
Pipeline: Parse MDX → Chunk → Embed → Store
Features: Semantic chunking, metadata extraction
```

#### 4. qa-tester.md
```
Purpose: Quality assurance testing
Checks: Code validity, links, consistency
Output: Detailed QA report with priorities
```

**Skills Defined (skills.md):**

| Skill | Purpose |
|-------|---------|
| explain-simply | Simplify for beginners |
| generate-examples | Create code examples |
| create-exercises | Design practice exercises |
| summarize-chapter | Generate summaries |
| validate-code | Check code correctness |
| check-links | Verify all links |
| lint-markdown | Format validation |
| adapt-for-level | Adjust difficulty |
| add-language-context | Compare to known languages |

---

### Phase 8: Scripts & Testing (Step 46-48)

**Embedding Ingestion Script**
```python
scripts/ingest_embeddings.py

Features:
- Parse MDX frontmatter
- Semantic chunking (respects headers)
- Batch embedding generation
- Qdrant upsert with metadata
- CLI arguments for paths

Usage:
python scripts/ingest_embeddings.py --docs-path ../frontend/docs
```

**Test Suite**
```python
tests/test_api.py

Test Classes:
- TestHealthCheck: Root and health endpoints
- TestAuth: Signup, signin, session handling
- TestChat: Chat service health
- TestContent: Chapter retrieval, auth checks
```

---

## 📁 File Structure

```
giaic-hackathon/
├── .github/
│   └── workflows/
│       └── deploy.yml              # CI/CD pipeline
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── auth.py         # Authentication endpoints
│   │   │   │   ├── chat.py         # RAG chat endpoints
│   │   │   │   └── content.py      # Content endpoints
│   │   │   └── __init__.py
│   │   ├── core/
│   │   │   ├── config.py           # Settings
│   │   │   ├── deps.py             # Dependencies
│   │   │   ├── security.py         # Auth utilities
│   │   │   └── __init__.py
│   │   ├── infrastructure/
│   │   │   ├── database.py         # SQLAlchemy setup
│   │   │   ├── vector_store.py     # Qdrant wrapper
│   │   │   └── __init__.py
│   │   ├── models/
│   │   │   ├── content.py          # CachedContent
│   │   │   ├── user.py             # User, UserProfile
│   │   │   └── __init__.py
│   │   ├── schemas/
│   │   │   ├── auth.py             # Auth schemas
│   │   │   ├── chat.py             # Chat schemas
│   │   │   ├── content.py          # Content schemas
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   ├── embedding_service.py
│   │   │   ├── personalization_service.py
│   │   │   ├── rag_service.py
│   │   │   ├── translation_service.py
│   │   │   └── __init__.py
│   │   ├── main.py                 # FastAPI app
│   │   └── __init__.py
│   ├── scripts/
│   │   └── ingest_embeddings.py    # Embedding pipeline
│   ├── tests/
│   │   ├── test_api.py
│   │   └── __init__.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── docs/
│   │   ├── intro.mdx
│   │   ├── chapter-1/
│   │   │   ├── overview.mdx
│   │   │   ├── concepts.mdx
│   │   │   ├── examples.mdx
│   │   │   ├── exercises.mdx
│   │   │   └── summary.mdx
│   │   ├── chapter-2/ ... (same structure)
│   │   ├── chapter-3/ ...
│   │   ├── chapter-4/ ...
│   │   ├── chapter-5/ ...
│   │   └── chapter-6/ ...
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChapterActions/
│   │   │   │   ├── index.tsx
│   │   │   │   └── styles.module.css
│   │   │   └── Chatbot/
│   │   │       ├── index.tsx
│   │   │       └── styles.module.css
│   │   ├── context/
│   │   │   └── AuthContext.tsx
│   │   ├── css/
│   │   │   └── custom.css
│   │   ├── pages/
│   │   │   ├── index.tsx
│   │   │   ├── index.module.css
│   │   │   ├── profile.tsx
│   │   │   └── profile.module.css
│   │   └── theme/
│   │       └── Root.tsx
│   ├── static/
│   ├── docusaurus.config.ts
│   ├── sidebars.ts
│   ├── package.json
│   └── tsconfig.json
├── subagents/
│   ├── README.md
│   ├── chapter-generator.md
│   ├── spec-converter.md
│   ├── embedding-ingester.md
│   ├── qa-tester.md
│   └── skills.md
├── .env.example
├── .gitignore
├── docker-compose.yml
├── HISTORY.md                      # This file
└── README.md
```

---

## ✨ Features Implemented

### Base Requirements

#### 1. AI/Spec-Driven Book Creation
- ✅ Docusaurus framework with MDX
- ✅ GitHub Pages deployment ready
- ✅ Professional navigation and structure
- ✅ Diagrams, code blocks, structured flow
- ✅ Spec-Kit Plus methodology (5 sections per chapter)
- ✅ Claude Code as authoring engine

#### 2. Integrated RAG Chatbot
- ✅ Embedded in Docusaurus UI
- ✅ General questions about entire book
- ✅ Questions based on selected text
- ✅ Citations to chapters/sections
- ✅ OpenAI Agents SDK compatible
- ✅ FastAPI backend
- ✅ Qdrant vector storage
- ✅ Automatic embedding from book content

### Bonus Requirements

#### 3. Reusable Intelligence (+50)
- ✅ Chapter generator subagent
- ✅ Spec converter subagent
- ✅ Embedding ingester subagent
- ✅ QA tester subagent
- ✅ 9 reusable agent skills

#### 4. Authentication & User Profiling (+50)
- ✅ Signup/Signin implementation
- ✅ JWT-based sessions with cookies
- ✅ Programming experience level
- ✅ Languages/frameworks known
- ✅ Hardware tier selection
- ✅ Learning goals
- ✅ Stored in Neon Postgres

#### 5. Content Personalization (+50)
- ✅ "Personalize this chapter" button
- ✅ Adjusts explanations based on level
- ✅ Changes examples for skill level
- ✅ AI-driven personalization
- ✅ Cached per user per chapter

#### 6. Urdu Translation (+50)
- ✅ "Translate to Urdu" button
- ✅ Dynamic AI translation
- ✅ Code blocks preserved
- ✅ Heading structure maintained
- ✅ Toggle back to English
- ✅ Cached translations

---

## 🧩 Challenges & Solutions

### Challenge 1: Code Block Preservation in Translation
**Problem:** Code blocks were getting translated or corrupted during Urdu translation.

**Solution:**
```python
# Extract code blocks with regex
code_blocks = re.findall(r'```[\s\S]*?```', content)
placeholders = [f"__CODE_BLOCK_{i}__" for i in range(len(code_blocks))]

# Replace with placeholders before translation
for block, placeholder in zip(code_blocks, placeholders):
    protected_content = protected_content.replace(block, placeholder)

# Restore after translation
for placeholder, block in zip(placeholders, code_blocks):
    translated = translated.replace(placeholder, block)
```

### Challenge 2: Semantic Chunking for RAG
**Problem:** Fixed-size chunking was splitting mid-paragraph and mid-code-block.

**Solution:**
```python
# Split by headers first
sections = re.split(r'\n## ', content)

# Then by paragraphs if section too long
if len(section.split()) > CHUNK_SIZE:
    paragraphs = section.split('\n\n')
    # Batch paragraphs into chunks
```

### Challenge 3: Text Selection in React
**Problem:** Detecting user text selection for contextual Q&A.

**Solution:**
```typescript
useEffect(() => {
  const handleSelection = () => {
    const selection = window.getSelection();
    if (selection && selection.toString().trim().length > 0) {
      setSelectedText(selection.toString().trim());
    }
  };
  document.addEventListener('mouseup', handleSelection);
  return () => document.removeEventListener('mouseup', handleSelection);
}, []);
```

### Challenge 4: Session Management with Cookies
**Problem:** Needed secure, httpOnly cookies that work with CORS.

**Solution:**
```python
response.set_cookie(
    key="access_token",
    value=access_token,
    httponly=True,           # Not accessible via JavaScript
    secure=not settings.DEBUG,  # HTTPS only in production
    samesite="lax",          # CSRF protection
    max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
)
```

---

## 🚀 Future Improvements

### Short Term
- [ ] Add more book chapters (7-10)
- [ ] Implement Redis caching for RAG results
- [ ] Add progress tracking per user
- [ ] Implement search across chapters

### Medium Term
- [ ] Add quizzes with automatic grading
- [ ] Implement spaced repetition for exercises
- [ ] Add collaborative annotations
- [ ] Multi-language support beyond Urdu

### Long Term
- [ ] AI tutor with conversation memory
- [ ] Code execution sandbox
- [ ] Personalized learning paths
- [ ] Integration with LMS platforms

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| Total Files | 83+ |
| MDX Content Files | 31 |
| Python Modules | 25 |
| React Components | 5 |
| API Endpoints | 10 |
| Book Chapters | 6 |
| Subagents | 4 |
| Agent Skills | 9 |
| Lines of Code | ~4000+ |

---

## 🙏 Acknowledgments

This project was built following specifications for:
- [Spec-Kit Plus](https://github.com/panaversity/spec-kit-plus/) methodology
- [Docusaurus](https://docusaurus.io/) documentation framework
- [Better-Auth](https://better-auth.com/) authentication patterns
- [Qdrant](https://qdrant.tech/) vector database
- [Neon](https://neon.tech/) serverless Postgres

---

## 🔧 Session 2: OpenRouter & Cohere Integration (January 22, 2026)

### Overview
Migrated the LLM and embedding providers from direct OpenAI to OpenRouter (for chat) and Cohere (for embeddings), plus fixed several configuration issues to get the app running locally.

### Issues Fixed

#### 1. Frontend Not Loading
**Problem:** Docusaurus was crashing on load with error.

**Root Causes:**
- `custom-authButton` navbar item was not registered (no swizzled component)
- `baseUrl` was hardcoded to `/giaic-hackathon/` for GitHub Pages

**Solution:**
```typescript
// docusaurus.config.ts
// Changed baseUrl to be dynamic
baseUrl: process.env.NODE_ENV === 'production' ? '/giaic-hackathon/' : '/',

// Removed unregistered custom navbar item
// - { type: 'custom-authButton', position: 'right' }
```

#### 2. process.env Not Defined in Browser
**Problem:** `ReferenceError: process is not defined` in AuthContext.tsx and Chatbot

**Root Cause:** Client-side code can't access `process.env` directly in Docusaurus.

**Solution:**
```typescript
// AuthContext.tsx - Before
const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';

// AuthContext.tsx - After
const API_BASE_URL = 'http://localhost:8000';
```

#### 3. CORS_ORIGINS Parsing Error
**Problem:** Pydantic Settings failed to parse comma-separated CORS_ORIGINS as JSON.

**Solution:**
```python
# config.py - Changed from List[str] to str with computed field
CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"

@computed_field
@property
def cors_origins_list(self) -> List[str]:
    return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
```

#### 4. DATABASE_URL Format
**Problem:** `ModuleNotFoundError: No module named 'psycopg2'`

**Root Cause:** URL used `postgresql://` but async SQLAlchemy needs `postgresql+asyncpg://`

**Solution:**
```env
# Before
DATABASE_URL=postgresql://user:pass@host/db

# After
DATABASE_URL=postgresql+asyncpg://user:pass@host/db?ssl=require
```

### Provider Changes

#### LLM: OpenAI → OpenRouter
**Why:** OpenRouter provides access to multiple models with OpenAI-compatible API.

**Changes to config.py:**
```python
# New settings
OPENROUTER_API_KEY: str = ""
OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
OPENROUTER_MODEL: str = "anthropic/claude-3.5-sonnet"
LLM_PROVIDER: str = "openrouter"
```

**Changes to services (rag_service.py, personalization_service.py, translation_service.py):**
```python
def __init__(self):
    if settings.LLM_PROVIDER == "openrouter" and settings.OPENROUTER_API_KEY:
        self.client = AsyncOpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url=settings.OPENROUTER_BASE_URL,
        )
        self.model = settings.OPENROUTER_MODEL
    else:
        # Fallback to direct OpenAI
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
```

#### Embeddings: OpenAI → Cohere
**Why:** OpenRouter doesn't support embeddings; Cohere provides quality embeddings.

**Changes to config.py:**
```python
COHERE_API_KEY: str = ""
COHERE_EMBEDDING_MODEL: str = "embed-english-v3.0"
```

**New embedding_service.py:**
```python
import cohere

class EmbeddingService:
    def __init__(self):
        self.client = cohere.Client(api_key=settings.COHERE_API_KEY)
        self.model = settings.COHERE_EMBEDDING_MODEL

    async def get_embedding(self, text: str) -> List[float]:
        response = self.client.embed(
            texts=[text],
            model=self.model,
            input_type="search_query",
        )
        return response.embeddings[0]
```

**Added to requirements.txt:**
```
cohere>=5.0.0
```

### Final Tech Stack

| Component | Provider | Model/Service |
|-----------|----------|---------------|
| LLM (Chat) | OpenRouter | xiaomi/mimo-v2-flash-free |
| Embeddings | Cohere | embed-english-v3.0 |
| Database | Neon | PostgreSQL (asyncpg) |
| Vector DB | Qdrant Cloud | book_content collection |
| Frontend | Docusaurus | localhost:3000 |
| Backend | FastAPI | localhost:8000 |

### Environment Variables Updated

```env
# LLM Provider
LLM_PROVIDER=openrouter

# OpenRouter
OPENROUTER_API_KEY=sk-or-v1-xxx
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=xiaomi/mimo-v2-flash-free

# Cohere (embeddings)
COHERE_API_KEY=xxx
COHERE_EMBEDDING_MODEL=embed-english-v3.0

# Database (fixed format)
DATABASE_URL=postgresql+asyncpg://user:pass@host/db?ssl=require

# CORS (comma-separated string)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Files Modified
| File | Changes |
|------|---------|
| `frontend/docusaurus.config.ts` | Fixed baseUrl, removed custom-authButton |
| `frontend/src/context/AuthContext.tsx` | Hardcoded API_BASE_URL |
| `frontend/src/components/Chatbot/index.tsx` | Hardcoded API URL |
| `backend/app/core/config.py` | Added OpenRouter, Cohere settings; fixed CORS parsing |
| `backend/app/main.py` | Use cors_origins_list |
| `backend/app/services/rag_service.py` | OpenRouter support |
| `backend/app/services/personalization_service.py` | OpenRouter support |
| `backend/app/services/translation_service.py` | OpenRouter support |
| `backend/app/services/embedding_service.py` | Switched to Cohere |
| `backend/requirements.txt` | Added cohere, removed better-auth |
| `.env` | Updated with new providers |
| `.env.example` | Updated template |

### Running the App

```bash
# Terminal 1 - Frontend
cd frontend
npm start
# → http://localhost:3000

# Terminal 2 - Backend
cd backend
python -m uvicorn app.main:app --reload --port 8000
# → http://localhost:8000
```

### Known Issues
- Qdrant client version warning (1.14.3 vs 1.16.3) - still functional
- Cohere embeddings are 1024 dimensions (OpenAI was 1536) - ensure Qdrant collection matches

---

## 🤖 Session 3: OpenAI Agents SDK Implementation (January 22, 2026)

### Overview
Implemented the OpenAI Agents SDK framework with OpenRouter as the LLM provider, enabling multi-step reasoning and tool calling capabilities for the chatbot.

### Key Changes

#### 1. New Agents Module Created
**Location:** `backend/app/agents/`

**tools.py** - Function tools for the agent:
```python
from agents import function_tool

@function_tool
def search_book(query: str, chapter_filter: Optional[str] = None) -> str:
    """Search the book content using semantic search."""
    # Uses Cohere embeddings + Qdrant vector search

@function_tool
def get_chapter_content(chapter_id: str) -> str:
    """Get the full content of a specific chapter."""

@function_tool
def list_chapters() -> str:
    """List all available chapters in the book."""

@function_tool
def explain_concept(concept: str, experience_level: str = "beginner") -> str:
    """Get a detailed explanation of a concept adapted to user's level."""
```

**book_agent.py** - Main agent using OpenRouter:
```python
from agents import Agent, Runner, ModelSettings
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel

# Create OpenRouter client
openrouter_client = AsyncOpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url=settings.OPENROUTER_BASE_URL,
)

# Custom model that uses OpenRouter
openrouter_model = OpenAIChatCompletionsModel(
    model=settings.OPENROUTER_MODEL,
    openai_client=openrouter_client,
)

# Create the Book Assistant Agent
book_assistant = Agent(
    name="BookAssistant",
    instructions=BOOK_ASSISTANT_INSTRUCTIONS,
    model=openrouter_model,
    tools=[search_book, get_chapter_content, list_chapters, explain_concept],
)

async def run_book_agent(query, selected_text, chapter_filter, user_profile):
    result = await Runner.run(book_assistant, input=full_input, max_turns=10)
    return {
        "answer": result.final_output,
        "tool_calls": extracted_tool_calls,
        "model": settings.OPENROUTER_MODEL,
        "agent": "BookAssistant",
    }
```

#### 2. Updated Chat Route
**File:** `backend/app/api/routes/chat.py`

```python
# New response schema for agent-based responses
class AgentChatResponse(BaseModel):
    answer: str
    tool_calls: List[dict] = []
    model: str
    agent: str

@router.post("/query", response_model=AgentChatResponse)
async def chat_query(request: ChatRequest, ...):
    from app.agents.book_agent import run_book_agent
    result = await run_book_agent(
        query=request.query,
        selected_text=request.selected_text,
        chapter_filter=request.chapter_id,
        user_profile=user_profile,
    )
    return AgentChatResponse(**result)
```

#### 3. Frontend Updates for Tool Calls Display
**File:** `frontend/src/components/Chatbot/index.tsx`

```typescript
interface ToolCall {
  tool: string;
  status: string;
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
  toolCalls?: ToolCall[];  // New field
  model?: string;          // New field
}

// Display tool calls in message
{msg.toolCalls && msg.toolCalls.length > 0 && (
  <div className={styles.toolCalls}>
    <span className={styles.toolCallsLabel}>Tools used:</span>
    {msg.toolCalls.map((tc, i) => (
      <span key={i} className={styles.toolCall}>{tc.tool}</span>
    ))}
  </div>
)}
```

**File:** `frontend/src/components/Chatbot/styles.module.css`

```css
.toolCalls {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid var(--ifm-color-emphasis-200);
  font-size: 0.75rem;
}

.toolCall {
  display: inline-block;
  margin-right: 6px;
  padding: 2px 8px;
  background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%);
  border-radius: 12px;
  color: var(--ifm-color-primary);
  font-size: 0.7rem;
}
```

### Technical Challenges & Solutions

#### Challenge: OpenAI Agents SDK Model Validation
**Problem:** The SDK validates model name prefixes and rejected "anthropic/claude-3-haiku" with error:
```
agents.exceptions.UserError: Unknown prefix: anthropic
```

**Root Cause:** The SDK's `MultiProvider` class parses model names like `provider/model` and tries to create corresponding providers. It doesn't have a built-in provider for "anthropic" prefix when using custom OpenRouter client.

**Solution:** Instead of passing a model name string to the Agent, use `OpenAIChatCompletionsModel` directly with the custom OpenRouter client:
```python
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel

openrouter_model = OpenAIChatCompletionsModel(
    model=settings.OPENROUTER_MODEL,
    openai_client=openrouter_client,
)

book_assistant = Agent(
    model=openrouter_model,  # Pass model instance, not string
    ...
)
```

#### Challenge: OpenRouter Model ID Format
**Problem:** Model ID `anthropic/claude-3-haiku-20240307` was invalid.

**Solution:** OpenRouter uses simplified model IDs. Changed to `anthropic/claude-3-haiku`.

### Updated Package Dependencies
**File:** `backend/requirements.txt`
```
openai-agents>=0.2.0  # OpenAI Agents SDK for agent framework
```

### API Response Format Change
**Before (RAG-only):**
```json
{
  "answer": "...",
  "citations": [{"id": 1, "source": "...", "chapter": "...", "score": 0.9}]
}
```

**After (Agent-based):**
```json
{
  "answer": "...",
  "tool_calls": [{"tool": "search_book", "status": "completed"}, ...],
  "model": "anthropic/claude-3-haiku",
  "agent": "BookAssistant"
}
```

### Agent Capabilities
The BookAssistant agent can now:
1. **Search the book** - Semantic search using Cohere embeddings + Qdrant
2. **Get chapter content** - Retrieve specific chapters
3. **List chapters** - Show available book content
4. **Explain concepts** - Provide personalized explanations based on user level

### Running Configuration
```bash
# Backend now runs on port 8001 due to port conflicts
# Frontend points to localhost:8001

# Terminal 1 - Frontend
cd frontend && npm start
# → http://localhost:3000

# Terminal 2 - Backend
cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
# → http://localhost:8001
```

### Files Added/Modified

| File | Action | Description |
|------|--------|-------------|
| `backend/app/agents/__init__.py` | Created | Module exports |
| `backend/app/agents/tools.py` | Created | Function tools with @function_tool decorator |
| `backend/app/agents/book_agent.py` | Created | Agent setup with OpenRouter |
| `backend/app/api/routes/chat.py` | Modified | Uses agent for /query endpoint |
| `frontend/src/components/Chatbot/index.tsx` | Modified | Shows tool calls |
| `frontend/src/components/Chatbot/styles.module.css` | Modified | Tool call styling |
| `frontend/src/context/AuthContext.tsx` | Modified | Port 8001 |
| `backend/.env` | Modified | Model name fixed |

### Health Check Response
```json
{
  "status": "healthy",
  "service": "chat",
  "agent": "BookAssistant",
  "framework": "OpenAI Agents SDK"
}
```

### Example Agent Interaction
```
User: "What chapters are available in this book?"

Agent Response:
{
  "answer": "The book covers AI fundamentals and advanced topics...",
  "tool_calls": [
    {"tool": "list_chapters", "status": "completed"}
  ],
  "model": "anthropic/claude-3-haiku",
  "agent": "BookAssistant"
}
```

---

*This HISTORY.md was generated as part of the project documentation.*
*Last updated: January 22, 2026*
