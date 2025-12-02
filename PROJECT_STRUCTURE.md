# Project Structure & Architecture

This document outlines the file structure and technical architecture of the **Gemini Character Generator** web application.

## 📂 Directory Structure

```text
create_ai_character/
├── backend/                  # Python FastAPI Backend
│   ├── main.py               # API Server Entrypoint
│   ├── character_engine.py   # Core AI Logic (Gemini/Imagen/Veo)
│   └── requirements.txt      # Backend Dependencies
├── frontend/                 # Next.js Frontend
│   ├── app/                  # App Router Pages
│   │   ├── page.tsx          # Landing Page
│   │   ├── layout.tsx        # Root Layout
│   │   └── create/           # Wizard Interface
│   │       └── page.tsx      # Main Creation Logic
│   ├── lib/                  # Utilities
│   │   └── api.ts            # API Client (Axios)
│   ├── public/               # Static Assets
│   └── ...                   # Config files (tailwind, next.config, etc.)
├── characters/               # Generated Character Data (JSON/MD/Images)
├── prompts/                  # System Prompts for AI
│   ├── 01_character_designer.md
│   ├── 02_story_writer.md
│   └── ...
├── start_app.sh              # Startup Script (Runs both servers)
└── .env                      # Environment Variables (API Keys)
```

## 🏗️ System Architecture

The application follows a modern **Client-Server** architecture, separating the interactive UI from the heavy AI processing logic.

```mermaid
graph TD
    subgraph Frontend [Next.js Frontend (Port 3000)]
        UI[User Interface] --> |User Input| Wizard[Wizard Logic]
        Wizard --> |API Calls| Client[API Client (lib/api.ts)]
    end

    subgraph Backend [FastAPI Backend (Port 8000)]
        API[API Endpoints (main.py)] --> |Request| Engine[Character Engine]
        Engine --> |Read| Prompts[System Prompts]
        Engine --> |Read/Write| Storage[File System (characters/)]
    end

    subgraph AI_Services [Google AI Ecosystem]
        Engine --> |Text Generation| Gemini[Gemini 3.0 Pro]
        Engine --> |Image Generation| Imagen[Imagen 3]
        Engine --> |Video Generation| Veo[Veo (Experimental)]
    end

    Client <--> |JSON/HTTP| API
```

## 🧩 Key Components

### 1. Backend (`backend/`)
*   **`main.py`**: The FastAPI server that exposes REST endpoints (`/api/init`, `/api/generate`). It handles HTTP requests, CORS, and serves static files from the `characters/` directory.
*   **`character_engine.py`**: The core "brain" of the application. It encapsulates all logic for interacting with Google's AI models (Gemini, Imagen, Veo). It handles prompt loading, API calls, and file saving.

### 2. Frontend (`frontend/`)
*   **`app/page.tsx`**: The landing page where users enter the initial character name and description.
*   **`app/create/page.tsx`**: The main "Wizard" interface. It manages the state of the creation process (steps, context, generated output) and communicates with the backend.
*   **`lib/api.ts`**: A type-safe wrapper around `axios` for making requests to the backend.

### 3. Data Storage (`characters/`)
*   All generated content is stored locally in the `characters/` directory.
*   Each character has its own folder containing Markdown files (profile, story), JSON files (prompts), and media files (images, videos).

## 🛠️ Tech Stack

*   **Frontend**: Next.js 14, React 18, Tailwind CSS, Framer Motion, Lucide React
*   **Backend**: Python 3.8+, FastAPI, Uvicorn, Google Generative AI SDK
*   **AI Models**: Gemini 3.0 Pro (Text), Gemini 3.0 Pro Image / Imagen 3 (Image), Veo (Video)
