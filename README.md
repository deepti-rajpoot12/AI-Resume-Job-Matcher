# AI Resume & Job Matcher

An intelligent, full-stack AI Resume & Job Matcher that evaluates resume relevance against target job descriptions, extracts strengths and improvement areas, formulates personalized interview preparation exercises, and generates RAG-grounded career roadmap plans.

---

## 1. Project Overview

The **AI Resume & Job Matcher** addresses the lack of feedback that applicants face when applying for technical roles. Standard Applicant Tracking Systems (ATS) reject resumes without explanation, leaving candidates unaware of their skill gaps. 

This application extracts text from resume PDFs and compares it against target job descriptions using the Google Gemini model. It calculates matching score stats, highlights strengths, generates tailored interview practice questions, and offers RAG-grounded career guidance based on curated development files.

---

## 2. Key Features

*   **Resume PDF Text Extraction**: Reads selectable PDFs in-memory without persistence, protecting privacy.
*   **Gemini-Powered Match Scores**: Calculates an alignment score (0-100%) showing the overall match.
*   **Skill Gap Detection**: Classifies resume items into matching skills (green) and missing gaps (amber).
*   **Strengths & Improvements**: Generates explicit observations and bulleted action steps to improve.
*   **Targeted Interview Practice**: Drafts key behavioral and technical questions based on the candidate's actual profile and gaps.
*   **RAG Career Guidance**: Retrieves structured career recommendations from a local vector knowledge repository.
*   **Actionable Roadmaps**: Builds detailed career roadmaps containing learning paths, recommended topics, specific practice projects, and study effort estimations.
*   **Analysis History**: Preserves previous analyses in a local database for visual comparison.
*   **Progress Tracking**: Evaluates changes in match score percentages and reduction in skill gaps over time.

---

## 3. Technology Stack

*   **Frontend**: React, Vite, Custom CSS (Responsive Grid Layouts).
*   **Backend**: FastAPI, PyMuPDF (PDF text extraction), Python-Multipart.
*   **Vector Database (RAG)**: ChromaDB (Local Persistent Client).
*   **Embeddings Model**: Sentence-Transformers (`all-MiniLM-L6-v2` loaded locally).
*   **Generative AI**: Google Gemini Developer API (`google-genai>=2.3.0` targeting `gemini-3.6-flash`).
*   **History Database**: SQLite3 (Local file-based database).

---

## 4. Architecture

```
  +-----------------------------------------------------------------------------------+
  |                                 REACT FRONTEND                                    |
  |  - Dashboard View (Match Metrics, Skill Pills, Strengths, Interview prep)        |
  |  - History & Progress Compare Card                                                |
  +--------------------+------------------------------------------^------------------+
                       |                                          |
        POST /api/analyze | POST /api/career-guidance              | Response JSON
                       |                                          |
  +--------------------+------------------------------------------+------------------+
  |                                 FASTAPI BACKEND                                   |
  |                                                                                   |
  |  +---------------------------+              +----------------------------------+  |
  |  |      RESUME PARSER        |              |          RAG SEARCH Engine       |  |
  |  |  (PyMuPDF in-memory text) |              |  (Query Chroma & deduplicate)    |  |
  |  +-------------+-------------+              +----------------^-----------------+  |
  |                |                                             |                    |
  |                v                                             | Query Embeddings   |
  |  +---------------------------+              +----------------+-----------------+  |
  |  |      GEMINI CLIENT        |              |        SENTENCE TRANSFORMERS     |  |
  |  |  (Structured JSON Output) <--------------+  (Local 'all-MiniLM-L6-v2' model)|  |
  |  +-------------+-------------+              +----------------+-----------------+  |
  |                |                                             |                    |
  |                v                                             v                    |
  |  +---------------------------+              +----------------------------------+  |
  |  |      HISTORY STORE        |              |          CHROMADB STORE          |  |
  |  |   (SQLite3 Database)      |              |   (Career Knowledge Collection)  |  |
  |  +---------------------------+              +----------------------------------+  |
  +-----------------------------------------------------------------------------------+
```

---

## 5. Project Structure

```
AI-Resume-Job-Matcher/
│
├── backend/
│   ├── app/
│   │   ├── models/                # Pydantic schemas (analysis, roadmap, history)
│   │   ├── prompts/               # Versioned system instructions & context builder
│   │   ├── routes/                # FastAPI routers (health, analysis, career, history)
│   │   ├── services/              # Core business services (LLM, RAG, SQLite, PDF parser)
│   │   └── main.py                # Server entry point & CORS configuration
│   │
│   ├── data/
│   │   ├── chroma/                # Local persistent vector store databases (gitignored)
│   │   ├── knowledge/             # Local Markdown guide resources for RAG ingestion
│   │   └── history.sqlite3        # Local SQLite database (gitignored)
│   │
│   ├── tests/                     # Unit test suites and scenario evaluations
│   ├── .env.example               # Placeholder backend environment setup
│   └── requirements.txt           # Python library dependencies
│
├── docs/
│   └── AI_ARCHITECTURE.md         # Extended developer architectural handbook
│
├── frontend/
│   ├── src/
│   │   ├── components/            # Visual React dashboard widgets
│   │   ├── services/              # API communications client
│   │   ├── App.jsx                # Main controller React component
│   │   ├── index.css              # Custom styling rules
│   │   └── main.jsx               # React main loader
│   │
│   ├── package.json               # Frontend package dependencies
│   └── vite.config.js             # Vite loader configuration
│
└── .gitignore                     # Repository file exclusion rules
```

---

## 6. Environment Setup

Copy `backend/.env.example` to `backend/.env` and replace the placeholder API key with a valid Gemini Developer key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.6-flash
```

---

## 7. Installation

### Backend Setup
1. Open a terminal and navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   *   **Windows**:
       ```bash
       python -m venv venv
       venv\Scripts\activate
       ```
   *   **macOS/Linux**:
       ```bash
       python3 -m venv venv
       source venv/bin/activate
       ```
3. Install package dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Seed the vector database with RAG career knowledge files:
   ```bash
   python -m app.services.ingestion
   ```

### Frontend Setup
1. Open a separate terminal and navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```

---

## 8. Running the Backend

Ensure the Python virtual environment is active in the `backend` directory, then start the server:
```bash
uvicorn app.main:app --reload
```
The API server will run at `http://localhost:8000`.

---

## 9. Running the Frontend

Navigate to the `frontend` directory, then start the development server:
```bash
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 10. API Endpoints

*   `GET /health`: Checks server liveness. Returns `{"status": "ok"}`.
*   `POST /api/analyze`: Extracts resume text, matches against a job description, and saves the initial analysis.
*   `POST /api/career-guidance`: Combines current analysis, job description, and retrieved RAG data to build a roadmap.
*   `GET /api/history`: Returns all history summaries.
*   `GET /api/history/{analysis_id}`: Fetches complete details of an analysis, including roadmaps.
*   `DELETE /api/history/{analysis_id}`: Deletes a saved run.

---

## 11. AI Architecture

*   **Model**: Gemini 3.6 Flash.
*   **Structured Outputs**: The API enforces response formatting using Pydantic JSON schemas. Gemini receives strict instructions to output schema-compliant structures directly, avoiding parsing overhead and string cleanup issues.
*   **System Prompts**: System instructions are decoupled from route controllers (`backend/app/prompts/`). Prompts clearly define strict evaluation rules (e.g., rejecting certifications or roles not supported by explicit candidate resume evidence).

---

## 12. RAG Architecture

*   **Embeddings Engine**: Utilizes sentence-transformers `all-MiniLM-L6-v2` locally.
*   **Retrieval flow**: 
    1. Extracts the candidate's top missing skills (gaps).
    2. Searches ChromaDB for semantic learning guides matching each gap.
    3. Deduplicates retrieved passages.
    4. Limits retrieval to the top 6 most relevant items.
    5. Injects context blocks directly into the Gemini career guidance prompt.

---

## 13. Career Plan

The application guides candidates through a structured learning path:
1.  **Priorities**: Targets skill gaps ordered by job relevance and prerequisites.
2.  **Explanations**: Contextualizes why each skill is necessary for the targeted job.
3.  **Pathing**: Sequences the learning timeline step-by-step.
4.  **Practical Exercises**: Provides structured practice projects.
5.  **Interview Focus**: Highlights common interview topics for each gap.
6.  **Resource Verification**: Sanitizes resource links, displaying only verified URLs matching a whitelist of trusted domains (Python, React, TypeScript, SQL, AWS, Kubernetes, Azure, GCP, etc.).

---

## 14. History & Progress

*   **SQLite Storage**: Retains local history offline.
*   **Visual Differential**: Evaluates the latest analysis score and missing skills against the preceding scan in the database, displaying score shifts and gap reductions.

---

## 15. Testing

To run the backend tests:
1. Navigate to the `backend` folder.
2. Run the command:
   ```bash
   python -m unittest discover -s tests
   ```

To test the frontend build:
1. Navigate to the `frontend` folder.
2. Run the command:
   ```bash
   npm run build
   ```

---

## 16. Future Improvements

*   **Docker Containerization**: Package the frontend, backend, and Chroma services in a unified container.
*   **Expanded PDF Extraction**: Support for parsing scanned/image-based resumes using OCR tools.
*   **Additional File Types**: Support parsing resumes in `.docx` formats.
*   **Extended Knowledge Directory**: Incorporate more specialized frameworks in the local RAG knowledge files.
