# Personal Chatbot

A personal chatbot for daily tasks built with **FastAPI** (clean architecture backend), **SQLAlchemy**, **Hugging Face LLM models**, and a **React frontend**. This project follows enterprise-grade architecture patterns and will be developed progressively.

## 🎯 Project Overview

This project aims to build an intelligent personal assistant chatbot that can:
- Handle natural language conversations
- Manage daily tasks and reminders
- Process structured commands (create task, list tasks, etc.)
- Maintain conversation history and context
- Use vector databases for semantic search and memory

## 🏗️ Architecture

This project follows a **layered architecture** (N-Tier) design pattern. See [FastAPI Layers Guide](src/Learn/FastAPI_Layers.md) for detailed architecture documentation.

### System Design Overview

![ChatGPT-like Chat System with Memory](src/Images/ChatGPT-like%20Chat%20System%20with%20Memory.png)

### System Design Layers

The project is organized into the following layers:

#### API Layer
- **[+]** API Gateway
- **[+]** Rate Limiter
- **[+]** Controller
- **[+]** DTO (Data Transfer Objects)
- **[ ]** Validation (Enhanced)
- **[+]** Router
- **[ ]** Token Usage Tracker

#### Business Logic Layer
- **[+]** Chatbot Processing
- **[+]** Query Type Detection
- **[+]** LLM Integration
- **[ ]** Task Management
- **[ ]** Intent Classification

#### Data Layer
- **[+]** Database Models (SQLAlchemy)
- **[+]** DTOs
- **[ ]** Repository Pattern
- **[ ]** Migrations (Alembic)

#### Memory Layer
- **[ ]** Response Cache
- **[+]** Vector Database (for semantic search)
- **[ ]** Conversation Memory
- **[ ]** Long-term Memory Storage

## 📁 Project Structure

```
personal-chatbot/
├── src/
│   ├── api/              # API Layer (Router, Controller, Middleware)
│   │   ├── main.py       # FastAPI application entry point
│   │   ├── router.py     # API route definitions
│   │   ├── controller.py # Request/response handling
│   │   └── ratelimiter.py
│   ├── business/         # Business Logic Layer
│   │   ├── chatbot.py    # Core chatbot processing
│   │   ├── model.py      # LLM model integration
│   │   └── vectordb.py   # Vector database operations
│   ├── data/             # Data Layer
│   │   ├── dto.py        # Data Transfer Objects
│   │   └── database.py   # Database configuration
│   ├── Learn/            # Learning resources and documentation
│   │   ├── FastAPI_Layers.md
│   │   ├── CONTROLLER_GUIDE.md
│   │   └── README.md
│   └── Images/           # Architecture diagrams
├── README.md
└── .gitignore
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- FastAPI
- SQLAlchemy
- Hugging Face Transformers
- React (for frontend - coming soon)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd personal-chatbot

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn src.api.main:app --reload
```

## 📚 Learning Resources

This project includes comprehensive learning materials in the `src/Learn/` directory:

- **[FastAPI Layers Guide](src/Learn/FastAPI_Layers.md)** - Complete architecture explanation
- **[Controller Guide](src/Learn/CONTROLLER_GUIDE.md)** - Step-by-step controller implementation guide

## 🔄 Development Progress

### Completed ✅
- API Gateway setup
- Rate Limiter
- Router layer
- Controller layer
- DTO definitions
- Basic chatbot processing
- Query type detection
- Vector database integration

### In Progress 🚧
- Enhanced validation
- Token usage tracking
- Task management features
- Repository pattern implementation

### Planned 📋
- Response caching
- Conversation memory
- Long-term memory storage
- React frontend
- Authentication & authorization
- Database migrations

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI
- **Database ORM**: SQLAlchemy
- **LLM**: Hugging Face Transformers
- **Vector Database**: (TBD - Chroma/PGVector)
- **Frontend**: React (planned)
- **Architecture**: Clean Architecture / N-Tier Architecture

## 📝 API Endpoints

### Chat Endpoints
- `POST /api/v1/chat` - Send a chat message
- `GET /api/v1/history` - Retrieve chat history

### Health Check
- `GET /health` - Health check endpoint
- `GET /` - Welcome message

## 🤝 Contributing

This project is being developed progressively. Contributions and suggestions are welcome!

## 📄 License

[Add your license here]

---

**Note**: This project follows clean architecture principles and is designed for learning and production use. See the [Learning Resources](src/Learn/README.md) for detailed guides on each component.
