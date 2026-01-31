# MyAnimeList Custom Client

A personalized web client for MyAnimeList (MAL) that allows users to manage their anime lists with extended functionality, such as attaching custom multimedia content (images, GIFs, videos) to series entries.

## 🚀 Overview

This project uses a **Backend for Frontend (BFF) / Proxy** architecture. The backend acts as an intelligent intermediary that merges official MAL data with local custom data.

### Key Features
- **Official MAL Integration**: Authenticate via OAuth 2.0 and manage your lists.
- **Enriched Entries**: Attach custom media to your favorite series.
- **FastAPI Backend**: Efficient data fusion and session management.
- **Vue.js Frontend**: Modern and responsive user interface.

## 🛠️ Tech Stack

- **Backend**: Python 3.11 + FastAPI
- **Dependency Management**: Poetry
- **Frontend**: Vue.js
- **Database**: SQLAlchemy + SQLite (Dev)
- **Containerization**: Docker & Docker Compose

## 📂 Project Structure

```text
my-mal-client/
├── backend/            # FastAPI Application
│   ├── app/            # Source code
│   │   └── main.py     # Entry point
│   ├── Dockerfile      # Backend container definition
│   └── pyproject.toml  # Poetry dependencies
├── frontend/           # Vue.js Application
├── docker-compose.yml  # Multi-container orchestration
└── README.md           # Project documentation
```

## 🚦 Getting Started

### Prerequisites
- Docker and Docker Compose installed.

   git clone https://github.com/retaLazyCodes/mal-client.git
   cd mal-client
   ```

2. **Start the services**:
   
   docker-compose up --build -d
   ```

3. **Verify the installation**:
   Access the API at `http://localhost:8000/`.

## 📜 API Documentation

Once the backend is running, you can explore the interactive API documentation:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🏗️ API Gateway Aggregation

1. **Frontend** requests data for a specific anime from the **Backend**.
2. **Backend** fetches official data from the **MAL API**.
3. **Backend** queries the **Local Database** for custom user media.
4. **Backend** merges both sources into a single JSON object.
5. **Frontend** displays the enriched data to the user.
